from abc import ABC, abstractmethod
from core.domain.interfaces import SolutionEvaluator
from core.domain.models import DomainSolution, DomainProblem, DomainEvaluationResult

class EvaluatorException(Exception):
    """Base exception for evaluation failures."""
    pass

class AIProviderException(EvaluatorException):
    """Exception raised when an LLM provider fails or is misconfigured."""
    pass

class InvalidEvaluationOutputException(EvaluatorException):
    """Exception raised when evaluator output cannot be parsed into DomainEvaluationResult."""
    pass
