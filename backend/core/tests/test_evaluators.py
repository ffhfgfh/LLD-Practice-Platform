import pytest
from core.domain.enums import Difficulty, AttemptStatus, EvaluationCategory, FeedbackSeverity, FeedbackSource, ConfidenceLevel
from core.domain.models import (
    DomainProblem,
    DomainRequirement,
    DomainSolution,
    DomainClassDesign,
    DomainAttribute,
    DomainMethod,
    DomainRelationship,
    DomainEvaluationResult
)
from core.domain.interfaces import SolutionEvaluator, SubmissionValidator, FeedbackGenerator
from core.services.evaluators.rule_based import RuleBasedEvaluator
from core.services.evaluators.composite_evaluator import CompositeEvaluator
from core.services.evaluators.ai_evaluator import AIEvaluator
from core.services.submission_validator import DefaultSubmissionValidator
from core.services.feedback_generator import StandardFeedbackGenerator

@pytest.fixture
def sample_problem():
    return DomainProblem(
        id="prob-1",
        slug="parking-lot",
        title="Parking Lot System",
        difficulty=Difficulty.MEDIUM,
        estimated_time_minutes=45,
        tags=["#StrategyPattern", "#ObserverPattern"],
        summary="Design parking lot",
        problem_statement="Full parking lot problem",
        constraints=["5000 spots", "Thread safe"],
        expected_design_considerations=["Strategy pattern for allocation", "Observer pattern for display"],
        hints=["Hint 1"],
        requirements=[
            DomainRequirement(
                id="req-1",
                req_code="REQ-1",
                title="Multi-Vehicle Support",
                description="Support Car, Bike, Truck",
                category="CORE_ENTITY",
                keywords=["Vehicle", "Car", "Bike", "Truck"],
                is_advanced=False
            ),
            DomainRequirement(
                id="req-2",
                req_code="REQ-2",
                title="Spot Allocation Strategy",
                description="Allocate spots intelligently",
                category="ALGORITHMIC",
                keywords=["AllocationStrategy", "ParkingSpot", "allocateSpot"],
                is_advanced=True
            )
        ]
    )

@pytest.fixture
def sample_good_solution():
    return DomainSolution(
        summary="A modular parking lot system using Strategy and Factory patterns to decouple parking allocation and fee calculation.",
        assumptions_and_tradeoffs="Assumed single entrance barrier per gate with atomic spot reservations using mutex locks for concurrency.",
        design_patterns_used=["Strategy", "Factory", "Observer"],
        mermaid_diagram="classDiagram\n    ParkingLot *-- ParkingFloor\n    ParkingFloor *-- ParkingSpot\n",
        classes=[
            DomainClassDesign(
                id="c1",
                name="ParkingLot",
                responsibility="Central facade managing parking lot infrastructure and delegating gate events.",
                methods=[DomainMethod(name="getAvailableSpots", return_type="int", params="")]
            ),
            DomainClassDesign(
                id="c2",
                name="ParkingSpot",
                responsibility="Represents a physical parking spot and manages its current occupancy status.",
                attributes=[DomainAttribute(name="id", type="string"), DomainAttribute(name="isOccupied", type="boolean")],
                methods=[DomainMethod(name="occupy", return_type="void"), DomainMethod(name="vacate", return_type="void")]
            ),
            DomainClassDesign(
                id="c3",
                name="Vehicle",
                responsibility="Abstract base class for all vehicle categories.",
                is_abstract=True
            ),
            DomainClassDesign(
                id="c4",
                name="Car",
                responsibility="Represents a compact automobile vehicle entity.",
                relationships=[DomainRelationship(target="Vehicle", type="INHERITANCE")]
            ),
            DomainClassDesign(
                id="c5",
                name="AllocationStrategy",
                responsibility="Interface defining algorithm for finding and assigning optimal parking spots.",
                is_interface=True,
                methods=[DomainMethod(name="allocateSpot", return_type="ParkingSpot", params="Vehicle v")]
            ),
            DomainClassDesign(
                id="c6",
                name="NearestSpotStrategy",
                responsibility="Concrete strategy finding closest parking spot to entrance gate.",
                interfaces_implemented=["AllocationStrategy"],
                methods=[DomainMethod(name="allocateSpot", return_type="ParkingSpot", params="Vehicle v")]
            )
        ]
    )

def test_rule_based_evaluator_deep_categories(sample_problem, sample_good_solution):
    evaluator = RuleBasedEvaluator()
    result = evaluator.evaluate(sample_good_solution, sample_problem)

    assert isinstance(result, DomainEvaluationResult)
    assert result.overall_score >= 70
    assert len(result.strengths) > 0
    assert len(result.refactoring_plan) > 0
    # Check that feedback items carry HIGH confidence and why_it_matters explanation
    assert all(item.confidence == ConfidenceLevel.HIGH for item in result.feedback_items)
    assert any(item.why_it_matters is not None for item in result.feedback_items)

def test_submission_validator_invariants(sample_problem, sample_good_solution):
    validator: SubmissionValidator = DefaultSubmissionValidator()
    
    # Valid solution
    errors = validator.validate(sample_good_solution, sample_problem)
    assert len(errors) == 0

    # Invalid empty responsibility
    bad_solution = DomainSolution(
        summary="Short flow explanation summary over 20 chars.",
        assumptions_and_tradeoffs="",
        classes=[DomainClassDesign(id="c1", name="ParkingLot", responsibility="vague")]
    )
    errors = validator.validate(bad_solution, sample_problem)
    assert any("Single Responsibility explanation" in e for e in errors)

def test_feedback_generator(sample_problem):
    generator: FeedbackGenerator = StandardFeedbackGenerator()
    raw = {
        "feedback_items": [
            {
                "category": "responsibility_assignment",
                "source": "AI_SUGGESTION",
                "severity": "WARNING",
                "title": "God Class",
                "message": "Too many methods",
                "why_it_matters": "Violates SRP."
            }
        ]
    }
    items = generator.generate_feedback(raw)
    assert len(items) == 1
    assert items[0].source == FeedbackSource.AI_SUGGESTION
    assert items[0].confidence == ConfidenceLevel.MEDIUM
    assert items[0].why_it_matters == "Violates SRP."


def test_custom_evaluator_substitution(sample_problem, sample_good_solution):
    """
    Tests the SolutionEvaluator interface contract (Change Test 2).
    Verifies that a custom/human evaluator can be substituted cleanly without altering the practice pipeline.
    """
    class HumanExpertEvaluator(SolutionEvaluator):
        def evaluate(self, solution: DomainSolution, problem: DomainProblem) -> DomainEvaluationResult:
            return DomainEvaluationResult(
                evaluator_type="HUMAN_EXPERT",
                overall_score=95,
                overall_summary="Expert human reviewer evaluation.",
                category_scores={"object_oriented_modeling": {"score": 9, "max_score": 10, "rationale": "Great OO models"}},
                strengths=["Excellent adherence to SRP and Strategy pattern."],
                improvement_areas=["Consider adding distributed locking for high concurrency."],
                feedback_items=[]
            )

    evaluator: SolutionEvaluator = HumanExpertEvaluator()
    result = evaluator.evaluate(sample_good_solution, sample_problem)
    assert result.overall_score == 95
    assert "SRP" in result.strengths[0]


def test_composite_evaluator_graceful_fallback_on_ai_failure(sample_problem, sample_good_solution):
    """
    Verifies that CompositeEvaluator falls back cleanly to deterministic RuleBasedEvaluator
    if the AI evaluation component fails or raises an error.
    """
    class BrokenAIEvaluator(SolutionEvaluator):
        provider = "deepseek"
        def evaluate(self, solution: DomainSolution, problem: DomainProblem) -> DomainEvaluationResult:
            raise RuntimeError("External AI API connection timed out or returned HTTP 500.")

    composite = CompositeEvaluator(
        rule_evaluator=RuleBasedEvaluator(),
        ai_evaluator=BrokenAIEvaluator()
    )

    result = composite.evaluate(sample_good_solution, sample_problem)
    assert isinstance(result, DomainEvaluationResult)
    assert result.overall_score >= 50
    assert result.is_fallback is True
    assert "unavailable" in result.error_message.lower()
    assert len(result.strengths) > 0
    assert any(item.confidence == ConfidenceLevel.HIGH for item in result.feedback_items)

