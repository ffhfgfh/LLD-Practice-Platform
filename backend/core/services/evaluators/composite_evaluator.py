import logging
from typing import Optional
from core.domain.interfaces import SolutionEvaluator
from core.domain.enums import FeedbackSource, ConfidenceLevel
from core.domain.models import (
    DomainSolution,
    DomainProblem,
    DomainEvaluationResult,
    DomainFeedbackItem
)
from core.services.evaluators.rule_based import RuleBasedEvaluator
from core.services.evaluators.ai_evaluator import AIEvaluator

logger = logging.getLogger(__name__)

class CompositeEvaluator(SolutionEvaluator):
    """
    Composite evaluator combining deterministic rule checks with AI qualitative reasoning.
    Gracefully falls back to rule-based evaluation if the AI service fails or is unconfigured.
    """

    def __init__(self, rule_evaluator: Optional[RuleBasedEvaluator] = None, ai_evaluator: Optional[AIEvaluator] = None):
        self.rule_evaluator = rule_evaluator or RuleBasedEvaluator()
        self.ai_evaluator = ai_evaluator or AIEvaluator()

    def evaluate(self, solution: DomainSolution, problem: DomainProblem) -> DomainEvaluationResult:
        # Step 1: Always execute deterministic evaluation first
        deterministic_result = self.rule_evaluator.evaluate(solution, problem)

        # Check if AI evaluation is possible
        if self.ai_evaluator.provider == "none":
            deterministic_result.evaluator_type = "RULE_BASED"
            return deterministic_result

        # Step 2: Try AI evaluation with graceful fallback
        try:
            ai_result = self.ai_evaluator.evaluate(solution, problem)
            return self._merge_results(deterministic_result, ai_result)
        except Exception as e:
            logger.warning(f"AI evaluation failed, falling back to rule-based evaluation: {str(e)}")
            deterministic_result.is_fallback = True
            deterministic_result.error_message = f"AI Evaluator was unavailable ({str(e)}). Full deterministic structural evaluation was completed."
            deterministic_result.evaluator_type = "RULE_BASED_FALLBACK"
            return deterministic_result

    def _merge_results(self, det: DomainEvaluationResult, ai: DomainEvaluationResult) -> DomainEvaluationResult:
        blended_overall_score = int(round(0.4 * det.overall_score + 0.6 * ai.overall_score))

        # Merge category scores
        merged_category_scores = {}
        for cat, det_cat_data in det.category_scores.items():
            ai_cat_data = ai.category_scores.get(cat, {})
            det_score = det_cat_data.get("score", 7)
            ai_score = ai_cat_data.get("score", det_score)
            blended_score = int(round(0.4 * det_score + 0.6 * ai_score))

            combined_rationale = (
                f"[Deterministic Check]: {det_cat_data.get('rationale', '')} "
                f"[AI Qualitative Insight]: {ai_cat_data.get('rationale', '')}"
            ).strip()

            merged_category_scores[cat] = {
                "title": det_cat_data.get("title", cat),
                "criterion": det_cat_data.get("criterion", det_cat_data.get("title", cat)),
                "score": blended_score,
                "max_score": 10,
                "evidence": ai_cat_data.get("evidence") or det_cat_data.get("evidence", ""),
                "concern": ai_cat_data.get("concern") or det_cat_data.get("concern", ""),
                "suggestion": ai_cat_data.get("suggestion") or det_cat_data.get("suggestion", ""),
                "confidence": ai_cat_data.get("confidence") or det_cat_data.get("confidence", "HIGH"),
                "rationale": combined_rationale
            }

        # Deduplicate and combine deep categories
        combined_strengths = list(dict.fromkeys(ai.strengths + det.strengths))[:7]
        combined_design_issues = list(dict.fromkeys(getattr(ai, 'design_issues', []) + det.design_issues))[:6]
        combined_missing_reqs = list(dict.fromkeys(getattr(ai, 'missing_requirements', []) + det.missing_requirements))[:6]
        combined_solid_viols = list(dict.fromkeys(getattr(ai, 'solid_violations', []) + det.solid_violations))[:6]
        combined_coupling = list(dict.fromkeys(getattr(ai, 'coupling_concerns', []) + det.coupling_concerns))[:6]
        combined_extensibility = list(dict.fromkeys(getattr(ai, 'extensibility_suggestions', []) + det.extensibility_suggestions))[:6]
        combined_edge_cases = list(dict.fromkeys(getattr(ai, 'edge_cases_analysis', []) + det.edge_cases_analysis))[:6]
        combined_recommendations = list(dict.fromkeys(ai.actionable_recommendations + det.actionable_recommendations))[:7]
        combined_refactoring_plan = list(dict.fromkeys(getattr(ai, 'refactoring_plan', []) + det.refactoring_plan))[:6]
        combined_improvements = list(dict.fromkeys(ai.improvement_areas + det.improvement_areas))[:7]

        # Combine feedback items (deterministic high confidence + AI qualitative suggestions)
        all_feedback_items = []
        for item in det.feedback_items:
            all_feedback_items.append(item)
        for item in ai.feedback_items:
            all_feedback_items.append(item)

        overall_summary = f"{ai.overall_summary}\n\n(Deterministic structural verification confirmed {len(det.feedback_items)} automated rule findings with 100% confidence)."

        return DomainEvaluationResult(
            evaluator_type="COMPOSITE",
            overall_score=blended_overall_score,
            overall_summary=overall_summary,
            strengths=combined_strengths,
            design_issues=combined_design_issues,
            missing_requirements=combined_missing_reqs,
            solid_violations=combined_solid_viols,
            coupling_concerns=combined_coupling,
            extensibility_suggestions=combined_extensibility,
            edge_cases_analysis=combined_edge_cases,
            actionable_recommendations=combined_recommendations,
            refactoring_plan=combined_refactoring_plan,
            improvement_areas=combined_improvements,
            category_scores=merged_category_scores,
            feedback_items=all_feedback_items,
            is_fallback=False,
            raw_response=ai.raw_response
        )
