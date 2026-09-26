from abc import ABC, abstractmethod
from typing import List
from core.domain.models import (
    DomainSolution,
    DomainProblem,
    DomainEvaluationResult,
    DomainFeedbackItem
)

class SubmissionValidator(ABC):
    """
    Contract for validating candidate solution before submission.
    Ensures domain invariants (e.g. non-empty classes, responsibilities, summaries) are met.
    """
    @abstractmethod
    def validate(self, solution: DomainSolution, problem: DomainProblem) -> List[str]:
        pass

class FeedbackGenerator(ABC):
    """
    Contract for formatting and synthesizing raw evaluation signals into categorized feedback items.
    """
    @abstractmethod
    def generate_feedback(self, raw_data: dict) -> List[DomainFeedbackItem]:
        pass

class SolutionEvaluator(ABC):
    """
    Abstract strategy contract for evaluating Low-Level Design solutions.
    Implementations include RuleBasedEvaluator, AIEvaluator, HumanReviewEvaluator, CompositeEvaluator.
    """
    @abstractmethod
    def evaluate(self, solution: DomainSolution, problem: DomainProblem) -> DomainEvaluationResult:
        pass
