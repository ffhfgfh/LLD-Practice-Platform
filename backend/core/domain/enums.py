from enum import Enum

class Difficulty(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

class AttemptStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    EVALUATING = "EVALUATING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class EvaluationCategory(str, Enum):
    REQUIREMENTS_COVERAGE = "requirements_coverage"
    RESPONSIBILITY_ASSIGNMENT = "responsibility_assignment"
    ABSTRACTION_AND_INTERFACES = "abstraction_and_interfaces"
    SOLID_PRINCIPLES = "solid_principles"
    COUPLING_AND_COHESION = "coupling_and_cohesion"
    EXTENSIBILITY = "extensibility"
    DESIGN_PATTERNS = "design_patterns"
    EDGE_CASES = "edge_cases"
    OVERALL_EXPLANATION = "overall_explanation"
    REFACTORING_PLAN = "refactoring_plan"

CATEGORY_TITLES = {
    EvaluationCategory.REQUIREMENTS_COVERAGE: "Requirements & Use Cases Coverage",
    EvaluationCategory.RESPONSIBILITY_ASSIGNMENT: "Responsibility Assignment (SRP)",
    EvaluationCategory.ABSTRACTION_AND_INTERFACES: "Abstraction & Interfaces",
    EvaluationCategory.SOLID_PRINCIPLES: "SOLID Principles Breakdown",
    EvaluationCategory.COUPLING_AND_COHESION: "Coupling & Cohesion Concerns",
    EvaluationCategory.EXTENSIBILITY: "Extensibility & Open/Closed Design",
    EvaluationCategory.DESIGN_PATTERNS: "Design Patterns Applicability",
    EvaluationCategory.EDGE_CASES: "Edge Cases, Concurrency & Failures",
    EvaluationCategory.OVERALL_EXPLANATION: "Architectural Explanation & Flow",
    EvaluationCategory.REFACTORING_PLAN: "Recommended Step-by-Step Refactoring",
}

class FeedbackSource(str, Enum):
    DETERMINISTIC = "DETERMINISTIC"
    AI_SUGGESTION = "AI_SUGGESTION"
    HYBRID = "HYBRID"

class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"      # 100% deterministic rule / AST / structural fact
    MEDIUM = "MEDIUM"  # High-confidence heuristic / AI reasoning
    LOW = "LOW"        # Exploratory design idea / subjective alternative

class FeedbackSeverity(str, Enum):
    POSITIVE = "POSITIVE"
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

class RelationshipType(str, Enum):
    ASSOCIATION = "ASSOCIATION"      # uses / knows (-->)
    AGGREGATION = "AGGREGATION"      # has-a (weak ownership o--)
    COMPOSITION = "COMPOSITION"      # has-a (exclusive ownership *--)
    INHERITANCE = "INHERITANCE"      # is-a (--|>)
    IMPLEMENTATION = "IMPLEMENTATION"# implements (..|>)
