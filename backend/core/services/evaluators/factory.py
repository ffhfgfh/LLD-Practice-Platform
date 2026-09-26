from typing import Optional
from django.conf import settings
from core.domain.interfaces import SolutionEvaluator
from core.services.evaluators.rule_based import RuleBasedEvaluator
from core.services.evaluators.ai_evaluator import AIEvaluator
from core.services.evaluators.composite_evaluator import CompositeEvaluator

def get_evaluator(evaluator_type: Optional[str] = None) -> SolutionEvaluator:
    """
    Factory method to instantiate a SolutionEvaluator.
    Supports 'rule_based', 'gemini', 'openai', or 'composite' (default).
    """
    eval_type = (evaluator_type or getattr(settings, 'EVALUATOR_TYPE', 'composite')).lower()

    if eval_type == "rule_based" or eval_type == "deterministic":
        return RuleBasedEvaluator()
    elif eval_type == "gemini":
        return AIEvaluator(provider="gemini")
    elif eval_type == "openai":
        return AIEvaluator(provider="openai")
    elif eval_type == "composite":
        return CompositeEvaluator()
    else:
        return CompositeEvaluator()
