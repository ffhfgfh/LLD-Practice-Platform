import logging
from typing import Optional
from django.db import transaction
from django.utils import timezone

from core.models import (
    PracticeAttempt,
    Evaluation,
    FeedbackItem
)
from core.domain.enums import AttemptStatus
from core.domain.interfaces import SolutionEvaluator
from core.services.evaluators.factory import get_evaluator

logger = logging.getLogger(__name__)

class EvaluationService:
    """
    Application service orchestrating evaluation execution, feedback persistence,
    and attempt state transitions.
    """

    @classmethod
    def evaluate_attempt(
        cls,
        attempt: PracticeAttempt,
        evaluator: Optional[SolutionEvaluator] = None,
        evaluator_type: Optional[str] = None
    ) -> Evaluation:
        """
        Executes evaluation on an attempt's solution and records detailed feedback.
        """
        attempt.status = AttemptStatus.EVALUATING.value
        attempt.save(update_fields=['status'])

        domain_problem = attempt.problem.to_domain()
        domain_solution = attempt.solution.to_domain()

        active_evaluator = evaluator or get_evaluator(evaluator_type)

        try:
            domain_result = active_evaluator.evaluate(domain_solution, domain_problem)

            with transaction.atomic():
                if hasattr(attempt, 'evaluation'):
                    attempt.evaluation.delete()

                evaluation = Evaluation.objects.create(
                    attempt=attempt,
                    evaluator_type=domain_result.evaluator_type,
                    overall_score=domain_result.overall_score,
                    overall_summary=domain_result.overall_summary,
                    strengths=domain_result.strengths,
                    design_issues=getattr(domain_result, 'design_issues', []),
                    missing_requirements=getattr(domain_result, 'missing_requirements', []),
                    solid_violations=getattr(domain_result, 'solid_violations', []),
                    coupling_concerns=getattr(domain_result, 'coupling_concerns', []),
                    extensibility_suggestions=getattr(domain_result, 'extensibility_suggestions', []),
                    edge_cases_analysis=getattr(domain_result, 'edge_cases_analysis', []),
                    actionable_recommendations=domain_result.actionable_recommendations,
                    refactoring_plan=getattr(domain_result, 'refactoring_plan', []),
                    improvement_areas=domain_result.improvement_areas,
                    category_scores=domain_result.category_scores,
                    raw_ai_response=domain_result.raw_response,
                    is_fallback=domain_result.is_fallback,
                    error_message=domain_result.error_message,
                    evaluated_at=timezone.now()
                )

                feedback_objs = [
                    FeedbackItem(
                        evaluation=evaluation,
                        category=item.category.value if hasattr(item.category, 'value') else str(item.category),
                        source=item.source.value if hasattr(item.source, 'value') else str(item.source),
                        confidence=item.confidence.value if hasattr(item.confidence, 'value') else str(getattr(item, 'confidence', 'HIGH')),
                        severity=item.severity.value if hasattr(item.severity, 'value') else str(item.severity),
                        title=item.title,
                        message=item.message,
                        target_entity=item.target_entity,
                        suggestion=item.suggestion,
                        why_it_matters=getattr(item, 'why_it_matters', None)
                    )
                    for item in domain_result.feedback_items
                ]
                FeedbackItem.objects.bulk_create(feedback_objs)

                attempt.status = AttemptStatus.COMPLETED.value
                attempt.save(update_fields=['status'])

                return evaluation

        except Exception as e:
            logger.error(f"Fatal evaluation error on attempt {attempt.id}: {str(e)}", exc_info=True)
            attempt.status = AttemptStatus.FAILED.value
            attempt.save(update_fields=['status'])

            with transaction.atomic():
                if hasattr(attempt, 'evaluation'):
                    attempt.evaluation.delete()

                evaluation = Evaluation.objects.create(
                    attempt=attempt,
                    evaluator_type="FAILED",
                    overall_score=0,
                    overall_summary="Evaluation could not be completed due to an unexpected processing error.",
                    strengths=[],
                    design_issues=["Processing exception during evaluation."],
                    missing_requirements=[],
                    solid_violations=[],
                    coupling_concerns=[],
                    extensibility_suggestions=[],
                    edge_cases_analysis=[],
                    actionable_recommendations=["Click 'Retry Evaluation' to re-run the evaluation service."],
                    refactoring_plan=["Retry evaluation or review class formatting."],
                    improvement_areas=["Please check your solution formatting and try submitting again."],
                    category_scores={},
                    is_fallback=True,
                    error_message=str(e),
                    evaluated_at=timezone.now()
                )

            return evaluation
