import uuid
from typing import Dict, Any, List, Optional
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError, NotFound

from core.models import (
    LLDProblem,
    PracticeAttempt,
    Solution,
    ClassDesign,
    Evaluation
)
from core.domain.enums import AttemptStatus
from core.domain.interfaces import SubmissionValidator
from core.services.submission_validator import DefaultSubmissionValidator
from core.services.evaluation_service import EvaluationService

class AttemptService:
    """
    Application service managing practice attempts, draft persistence, submission, and validation.
    Enforces business rules such as attempt immutability after submission and validator pluggability.
    """
    validator: SubmissionValidator = DefaultSubmissionValidator()

    @classmethod
    def create_attempt(cls, problem_id: str) -> PracticeAttempt:
        problem = None
        try:
            val = uuid.UUID(str(problem_id))
            problem = LLDProblem.objects.get(id=val)
        except (ValueError, LLDProblem.DoesNotExist):
            try:
                problem = LLDProblem.objects.get(slug=problem_id)
            except LLDProblem.DoesNotExist:
                raise NotFound(f"Problem '{problem_id}' not found.")

        with transaction.atomic():
            max_attempt = PracticeAttempt.objects.filter(problem=problem).order_by('-attempt_number').first()
            next_num = (max_attempt.attempt_number + 1) if max_attempt else 1

            attempt = PracticeAttempt.objects.create(
                problem=problem,
                attempt_number=next_num,
                status=AttemptStatus.DRAFT.value,
                started_at=timezone.now()
            )

            Solution.objects.create(
                attempt=attempt,
                summary="",
                assumptions_and_tradeoffs="",
                design_patterns_used=[],
                mermaid_diagram=""
            )

            return attempt

    @classmethod
    def save_draft(cls, attempt_id: str, data: Dict[str, Any]) -> PracticeAttempt:
        try:
            attempt = PracticeAttempt.objects.select_related('problem', 'solution').get(id=attempt_id)
        except (PracticeAttempt.DoesNotExist, ValueError):
            raise NotFound(f"Attempt '{attempt_id}' not found.")

        if not attempt.is_mutable:
            raise ValidationError(
                f"Cannot modify attempt in '{attempt.status}' state. Submitted attempts are immutable. Use 'Try Again' to start a new attempt."
            )

        solution_data = data.get('solution', {})
        classes_data = solution_data.get('classes', [])

        with transaction.atomic():
            solution = attempt.solution
            if 'summary' in solution_data:
                solution.summary = solution_data.get('summary', '')
            if 'assumptions_and_tradeoffs' in solution_data:
                solution.assumptions_and_tradeoffs = solution_data.get('assumptions_and_tradeoffs', '')
            if 'design_patterns_used' in solution_data:
                solution.design_patterns_used = solution_data.get('design_patterns_used', [])
            if 'mermaid_diagram' in solution_data:
                solution.mermaid_diagram = solution_data.get('mermaid_diagram', '')
            
            solution.save()

            if classes_data is not None:
                solution.classes.all().delete()
                for idx, c_data in enumerate(classes_data):
                    ClassDesign.objects.create(
                        solution=solution,
                        name=c_data.get('name', '').strip(),
                        responsibility=c_data.get('responsibility', '').strip(),
                        attributes=c_data.get('attributes', []),
                        methods=c_data.get('methods', []),
                        relationships=c_data.get('relationships', []),
                        interfaces_implemented=c_data.get('interfaces_implemented', []),
                        is_interface=c_data.get('is_interface', False),
                        is_abstract=c_data.get('is_abstract', False),
                        order=c_data.get('order', idx)
                    )

            attempt.last_saved_at = timezone.now()
            attempt.save(update_fields=['last_saved_at'])

        return attempt

    @classmethod
    def validate_for_submission(cls, attempt: PracticeAttempt) -> List[str]:
        solution = getattr(attempt, 'solution', None)
        if not solution:
            return ["No solution found for this attempt."]

        domain_solution = solution.to_domain()
        domain_problem = attempt.problem.to_domain()

        return cls.validator.validate(domain_solution, domain_problem)

    @classmethod
    def submit_attempt(cls, attempt_id: str, evaluator_type: Optional[str] = None) -> PracticeAttempt:
        try:
            attempt = PracticeAttempt.objects.select_related('problem', 'solution').get(id=attempt_id)
        except (PracticeAttempt.DoesNotExist, ValueError):
            raise NotFound(f"Attempt '{attempt_id}' not found.")

        if attempt.status in [AttemptStatus.SUBMITTED.value, AttemptStatus.EVALUATING.value, AttemptStatus.COMPLETED.value]:
            raise ValidationError(
                f"Attempt has already been submitted (status: {attempt.status}). Use 'Try Again' to create a new attempt."
            )

        validation_errors = cls.validate_for_submission(attempt)
        if validation_errors:
            raise ValidationError({"validation_errors": validation_errors})

        # Transition to SUBMITTED
        attempt.status = AttemptStatus.SUBMITTED.value
        attempt.submitted_at = timezone.now()
        attempt.save(update_fields=['status', 'submitted_at'])

        # Orchestrate evaluation
        EvaluationService.evaluate_attempt(attempt, evaluator_type=evaluator_type)
        attempt.refresh_from_db()
        return attempt

    @classmethod
    def retry_evaluation(cls, attempt_id: str, evaluator_type: Optional[str] = None) -> PracticeAttempt:
        try:
            attempt = PracticeAttempt.objects.select_related('problem', 'solution').get(id=attempt_id)
        except (PracticeAttempt.DoesNotExist, ValueError):
            raise NotFound(f"Attempt '{attempt_id}' not found.")

        if attempt.status == AttemptStatus.DRAFT.value:
            raise ValidationError("Cannot evaluate an unsubmitted draft. Please submit your solution first.")

        EvaluationService.evaluate_attempt(attempt, evaluator_type=evaluator_type)
        attempt.refresh_from_db()
        return attempt
