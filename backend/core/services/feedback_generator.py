from typing import List, Dict, Any
from core.domain.interfaces import FeedbackGenerator
from core.domain.enums import (
    EvaluationCategory,
    FeedbackSource,
    ConfidenceLevel,
    FeedbackSeverity
)
from core.domain.models import DomainFeedbackItem

class StandardFeedbackGenerator(FeedbackGenerator):
    """
    Synthesizes and categorizes raw evaluator outputs into standardized DomainFeedbackItems.
    """

    def generate_feedback(self, raw_data: Dict[str, Any]) -> List[DomainFeedbackItem]:
        items: List[DomainFeedbackItem] = []
        raw_items = raw_data.get("feedback_items", [])

        for r in raw_items:
            # Parse category
            cat_str = r.get("category", EvaluationCategory.OVERALL_EXPLANATION.value)
            try:
                cat_enum = EvaluationCategory(cat_str)
            except ValueError:
                cat_enum = EvaluationCategory.OVERALL_EXPLANATION

            # Parse source & confidence
            source_str = r.get("source", FeedbackSource.DETERMINISTIC.value)
            try:
                source_enum = FeedbackSource(source_str)
            except ValueError:
                source_enum = FeedbackSource.DETERMINISTIC

            conf_str = r.get("confidence", ConfidenceLevel.HIGH.value if source_enum == FeedbackSource.DETERMINISTIC else ConfidenceLevel.MEDIUM.value)
            try:
                conf_enum = ConfidenceLevel(conf_str)
            except ValueError:
                conf_enum = ConfidenceLevel.HIGH if source_enum == FeedbackSource.DETERMINISTIC else ConfidenceLevel.MEDIUM

            # Parse severity
            sev_str = r.get("severity", FeedbackSeverity.INFO.value)
            try:
                sev_enum = FeedbackSeverity(sev_str)
            except ValueError:
                sev_enum = FeedbackSeverity.INFO

            items.append(DomainFeedbackItem(
                category=cat_enum,
                source=source_enum,
                confidence=conf_enum,
                severity=sev_enum,
                title=r.get("title", "Design Observation"),
                message=r.get("message", ""),
                target_entity=r.get("target_entity"),
                suggestion=r.get("suggestion"),
                why_it_matters=r.get("why_it_matters")
            ))

        return items
