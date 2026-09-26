from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from core.domain.enums import (
    Difficulty,
    AttemptStatus,
    EvaluationCategory,
    FeedbackSource,
    ConfidenceLevel,
    FeedbackSeverity,
    RelationshipType
)

@dataclass
class DomainRequirement:
    id: str
    req_code: str
    title: str
    description: str
    category: str
    keywords: List[str] = field(default_factory=list)
    is_advanced: bool = False
    order: int = 0

@dataclass
class DomainProblem:
    id: str
    slug: str
    title: str
    difficulty: Difficulty
    estimated_time_minutes: int
    tags: List[str]
    summary: str
    problem_statement: str
    constraints: List[str] = field(default_factory=list)
    expected_design_considerations: List[str] = field(default_factory=list)
    hints: List[str] = field(default_factory=list)
    requirements: List[DomainRequirement] = field(default_factory=list)

@dataclass
class DomainAttribute:
    name: str
    type: str = "string"
    visibility: str = "private"

@dataclass
class DomainMethod:
    name: str
    return_type: str = "void"
    params: str = ""
    visibility: str = "public"

@dataclass
class DomainRelationship:
    target: str
    type: str = "ASSOCIATION"
    multiplicity: str = "1"
    description: str = ""

@dataclass
class DomainClassDesign:
    id: Optional[str]
    name: str
    responsibility: str
    attributes: List[DomainAttribute] = field(default_factory=list)
    methods: List[DomainMethod] = field(default_factory=list)
    relationships: List[DomainRelationship] = field(default_factory=list)
    interfaces_implemented: List[str] = field(default_factory=list)
    is_interface: bool = False
    is_abstract: bool = False
    order: int = 0

@dataclass
class DomainSolution:
    summary: str
    assumptions_and_tradeoffs: str
    design_patterns_used: List[str] = field(default_factory=list)
    mermaid_diagram: str = ""
    classes: List[DomainClassDesign] = field(default_factory=list)

@dataclass
class DomainFeedbackItem:
    category: EvaluationCategory
    source: FeedbackSource
    severity: FeedbackSeverity
    confidence: ConfidenceLevel
    title: str
    message: str
    target_entity: Optional[str] = None
    suggestion: Optional[str] = None
    why_it_matters: Optional[str] = None

@dataclass
class CategoryScore:
    category: EvaluationCategory
    score: int  # 0 to 10
    max_score: int = 10
    rationale: str = ""

@dataclass
class DomainEvaluationResult:
    evaluator_type: str
    overall_score: int  # 0 to 100
    overall_summary: str
    strengths: List[str] = field(default_factory=list)
    design_issues: List[str] = field(default_factory=list)
    missing_requirements: List[str] = field(default_factory=list)
    solid_violations: List[str] = field(default_factory=list)
    coupling_concerns: List[str] = field(default_factory=list)
    extensibility_suggestions: List[str] = field(default_factory=list)
    edge_cases_analysis: List[str] = field(default_factory=list)
    actionable_recommendations: List[str] = field(default_factory=list)
    refactoring_plan: List[str] = field(default_factory=list)
    improvement_areas: List[str] = field(default_factory=list)
    category_scores: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    feedback_items: List[DomainFeedbackItem] = field(default_factory=list)
    is_fallback: bool = False
    error_message: Optional[str] = None
    raw_response: Optional[str] = None
