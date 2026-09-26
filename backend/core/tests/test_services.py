import pytest
from django.utils import timezone
from rest_framework.exceptions import ValidationError, NotFound

from core.models import LLDProblem, ProblemRequirement, PracticeAttempt, Solution, ClassDesign, Evaluation
from core.domain.enums import AttemptStatus, Difficulty
from core.services.attempt_service import AttemptService
from core.services.evaluation_service import EvaluationService

@pytest.mark.django_db
class TestAttemptService:
    @pytest.fixture(autouse=True)
    def setup_problem(self):
        self.problem = LLDProblem.objects.create(
            slug="parking-lot-test",
            title="Parking Lot Test",
            difficulty=Difficulty.MEDIUM.value,
            summary="A test parking lot problem",
            problem_statement="Problem statement markdown",
            constraints=["Constraint 1"],
            expected_design_considerations=["Consideration 1"],
            hints=["Hint 1"]
        )
        ProblemRequirement.objects.create(
            problem=self.problem,
            req_code="REQ-1",
            title="Vehicle Hierarchy",
            description="Support various vehicles",
            keywords=["Vehicle", "Car", "Truck"],
            order=1
        )

    def test_create_attempt_increments_attempt_number(self):
        attempt1 = AttemptService.create_attempt(str(self.problem.id))
        assert attempt1.attempt_number == 1
        assert attempt1.status == AttemptStatus.DRAFT.value
        assert hasattr(attempt1, 'solution')

        attempt2 = AttemptService.create_attempt(str(self.problem.id))
        assert attempt2.attempt_number == 2
        assert attempt2.problem.id == self.problem.id

    def test_save_draft_updates_solution_and_classes(self):
        attempt = AttemptService.create_attempt(str(self.problem.id))
        
        draft_data = {
            "solution": {
                "summary": "This is a comprehensive parking lot design summary explaining high level flows.",
                "assumptions_and_tradeoffs": "Assuming single entry gate per floor.",
                "design_patterns_used": ["Strategy", "Factory"],
                "mermaid_diagram": "classDiagram\n    ParkingLot *-- Spot\n",
                "classes": [
                    {
                        "name": "ParkingLot",
                        "responsibility": "Coordinates overall parking operations.",
                        "is_interface": False,
                        "is_abstract": False,
                        "attributes": [{"name": "id", "type": "string", "visibility": "private"}],
                        "methods": [{"name": "parkVehicle", "returnType": "Ticket", "params": "Vehicle v", "visibility": "public"}],
                        "relationships": [{"target": "Spot", "type": "COMPOSITION", "multiplicity": "1..*"}]
                    },
                    {
                        "name": "Spot",
                        "responsibility": "Represents single parking spot.",
                        "is_interface": False,
                        "is_abstract": False,
                        "attributes": [],
                        "methods": [],
                        "relationships": []
                    }
                ]
            }
        }

        updated = AttemptService.save_draft(str(attempt.id), draft_data)
        assert updated.solution.summary == "This is a comprehensive parking lot design summary explaining high level flows."
        assert updated.solution.classes.count() == 2
        assert updated.solution.classes.first().name == "ParkingLot"

    def test_cannot_save_draft_on_submitted_attempt(self):
        attempt = AttemptService.create_attempt(str(self.problem.id))
        attempt.status = AttemptStatus.SUBMITTED.value
        attempt.save()

        with pytest.raises(ValidationError) as excinfo:
            AttemptService.save_draft(str(attempt.id), {"solution": {"summary": "New summary"}})
        assert "immutable" in str(excinfo.value)

    def test_validate_for_submission_catches_empty_solution(self):
        attempt = AttemptService.create_attempt(str(self.problem.id))
        errors = AttemptService.validate_for_submission(attempt)
        assert len(errors) > 0
        assert any("At least one class" in e for e in errors)
        assert any("summary" in e for e in errors)

    def test_submit_attempt_runs_evaluation_and_completes(self):
        attempt = AttemptService.create_attempt(str(self.problem.id))
        AttemptService.save_draft(str(attempt.id), {
            "solution": {
                "summary": "Full design architecture explaining vehicle entry, spot allocation, and payment.",
                "assumptions_and_tradeoffs": "Standard concurrency assumptions.",
                "design_patterns_used": ["Strategy"],
                "mermaid_diagram": "classDiagram\n    ParkingLot *-- Vehicle\n",
                "classes": [
                    {
                        "name": "ParkingLot",
                        "responsibility": "Orchestrates parking operations and floor management.",
                        "methods": [{"name": "parkVehicle", "returnType": "void", "params": "Vehicle v"}],
                        "relationships": []
                    },
                    {
                        "name": "Vehicle",
                        "responsibility": "Domain model for incoming vehicles.",
                        "is_abstract": True
                    }
                ]
            }
        })

        submitted = AttemptService.submit_attempt(str(attempt.id), evaluator_type="rule_based")
        assert submitted.status == AttemptStatus.COMPLETED.value
        assert submitted.submitted_at is not None
        assert hasattr(submitted, 'evaluation')
        assert submitted.evaluation.overall_score > 0
        assert submitted.evaluation.feedback_items.count() > 0

    def test_cannot_submit_already_submitted_attempt(self):
        attempt = AttemptService.create_attempt(str(self.problem.id))
        attempt.status = AttemptStatus.COMPLETED.value
        attempt.save()

        with pytest.raises(ValidationError) as excinfo:
            AttemptService.submit_attempt(str(attempt.id))
        assert "already been submitted" in str(excinfo.value)

    def test_retry_evaluation_updates_existing_attempt(self):
        attempt = AttemptService.create_attempt(str(self.problem.id))
        AttemptService.save_draft(str(attempt.id), {
            "solution": {
                "summary": "Parking lot design summary with minimum twenty characters.",
                "classes": [{"name": "ParkingLot", "responsibility": "Coordinates overall parking system."}]
            }
        })
        submitted = AttemptService.submit_attempt(str(attempt.id), evaluator_type="rule_based")
        first_score = submitted.evaluation.overall_score

        # Retry evaluation
        re_evaluated = AttemptService.retry_evaluation(str(attempt.id), evaluator_type="rule_based")
        assert re_evaluated.status == AttemptStatus.COMPLETED.value
        assert re_evaluated.evaluation.overall_score == first_score

    def test_try_again_creates_new_independent_attempt_preserving_history(self):
        # Attempt 1
        att1 = AttemptService.create_attempt(str(self.problem.id))
        AttemptService.save_draft(str(att1.id), {
            "solution": {
                "summary": "First attempt summary with minimum twenty characters.",
                "classes": [{"name": "ParkingLot", "responsibility": "First attempt class."}]
            }
        })
        att1_submitted = AttemptService.submit_attempt(str(att1.id), evaluator_type="rule_based")
        assert att1_submitted.attempt_number == 1
        assert att1_submitted.status == AttemptStatus.COMPLETED.value

        # Attempt 2 (Try Again)
        att2 = AttemptService.create_attempt(str(self.problem.id))
        assert att2.id != att1.id
        assert att2.attempt_number == 2
        assert att2.status == AttemptStatus.DRAFT.value

        # Verify Attempt 1 remains intact
        att1_refetched = PracticeAttempt.objects.get(id=att1.id)
        assert att1_refetched.status == AttemptStatus.COMPLETED.value
        assert att1_refetched.solution.summary == "First attempt summary with minimum twenty characters."

