import uuid
from django.db import models
from django.utils import timezone
from core.domain.enums import (
    Difficulty,
    AttemptStatus,
    EvaluationCategory,
    FeedbackSource,
    ConfidenceLevel,
    FeedbackSeverity,
    RelationshipType
)

class LLDProblem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    difficulty = models.CharField(
        max_length=20,
        choices=[(d.value, d.value) for d in Difficulty],
        default=Difficulty.MEDIUM.value
    )
    estimated_time_minutes = models.PositiveIntegerField(default=45, help_text="Estimated time in minutes")
    tags = models.JSONField(default=list, blank=True, help_text="Tags like #Strategy, #StatePattern, #Concurrency")
    summary = models.TextField(help_text="Short overview for problem cards")
    problem_statement = models.TextField(help_text="Full markdown problem description")
    constraints = models.JSONField(default=list, help_text="List of constraints")
    expected_design_considerations = models.JSONField(
        default=list,
        help_text="Design considerations expected from learner"
    )
    hints = models.JSONField(default=list, help_text="Progressive hints")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} ({self.difficulty} - ~{self.estimated_time_minutes}m)"

    def to_domain(self):
        from core.domain.models import DomainProblem
        return DomainProblem(
            id=str(self.id),
            slug=self.slug,
            title=self.title,
            difficulty=Difficulty(self.difficulty),
            estimated_time_minutes=self.estimated_time_minutes,
            tags=self.tags or [],
            summary=self.summary,
            problem_statement=self.problem_statement,
            constraints=self.constraints or [],
            expected_design_considerations=self.expected_design_considerations or [],
            hints=self.hints or [],
            requirements=[req.to_domain() for req in self.requirements.all().order_by('order')]
        )


class ProblemRequirement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    problem = models.ForeignKey(LLDProblem, related_name='requirements', on_delete=models.CASCADE)
    req_code = models.CharField(max_length=20, help_text="e.g. REQ-1, REQ-2")
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, default="FUNCTIONAL")
    keywords = models.JSONField(default=list, help_text="Keywords/entity names for deterministic checks")
    is_advanced = models.BooleanField(default=False, help_text="True if progressive/advanced requirement")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'req_code']
        unique_together = ('problem', 'req_code')

    def __str__(self):
        return f"[{self.problem.title}] {self.req_code}: {self.title}"

    def to_domain(self):
        from core.domain.models import DomainRequirement
        return DomainRequirement(
            id=str(self.id),
            req_code=self.req_code,
            title=self.title,
            description=self.description,
            category=self.category,
            keywords=self.keywords or [],
            is_advanced=self.is_advanced,
            order=self.order
        )


class PracticeAttempt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    problem = models.ForeignKey(LLDProblem, related_name='attempts', on_delete=models.CASCADE)
    attempt_number = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=[(s.value, s.value) for s in AttemptStatus],
        default=AttemptStatus.DRAFT.value
    )
    started_at = models.DateTimeField(default=timezone.now)
    submitted_at = models.DateTimeField(null=True, blank=True)
    last_saved_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-started_at']
        unique_together = ('problem', 'attempt_number')

    def __str__(self):
        return f"{self.problem.title} - Attempt #{self.attempt_number} ({self.status})"

    @property
    def is_mutable(self) -> bool:
        """Attempts are mutable only while in DRAFT status."""
        return self.status == AttemptStatus.DRAFT.value


class Solution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attempt = models.OneToOneField(PracticeAttempt, related_name='solution', on_delete=models.CASCADE)
    summary = models.TextField(blank=True, default="", help_text="High level architecture & flow")
    assumptions_and_tradeoffs = models.TextField(blank=True, default="", help_text="Design trade-offs and assumptions")
    design_patterns_used = models.JSONField(default=list, blank=True)
    mermaid_diagram = models.TextField(blank=True, default="", help_text="Mermaid classDiagram syntax")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Solution for {self.attempt}"

    def to_domain(self):
        from core.domain.models import DomainSolution
        return DomainSolution(
            summary=self.summary or "",
            assumptions_and_tradeoffs=self.assumptions_and_tradeoffs or "",
            design_patterns_used=self.design_patterns_used or [],
            mermaid_diagram=self.mermaid_diagram or "",
            classes=[c.to_domain() for c in self.classes.all().order_by('order')]
        )


class ClassDesign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    solution = models.ForeignKey(Solution, related_name='classes', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    responsibility = models.TextField(help_text="Single Responsibility explanation")
    attributes = models.JSONField(default=list, blank=True, help_text="[{name, type, visibility}]")
    methods = models.JSONField(default=list, blank=True, help_text="[{name, returnType, params, visibility}]")
    relationships = models.JSONField(default=list, blank=True, help_text="[{target, type, multiplicity, description}]")
    interfaces_implemented = models.JSONField(default=list, blank=True, help_text="List of interface names")
    is_interface = models.BooleanField(default=False)
    is_abstract = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        type_str = "interface" if self.is_interface else ("abstract class" if self.is_abstract else "class")
        return f"{type_str} {self.name}"

    def to_domain(self):
        from core.domain.models import (
            DomainClassDesign,
            DomainAttribute,
            DomainMethod,
            DomainRelationship
        )
        return DomainClassDesign(
            id=str(self.id),
            name=self.name,
            responsibility=self.responsibility or "",
            attributes=[
                DomainAttribute(
                    name=a.get('name', ''),
                    type=a.get('type', 'string'),
                    visibility=a.get('visibility', 'private')
                ) for a in (self.attributes or [])
            ],
            methods=[
                DomainMethod(
                    name=m.get('name', ''),
                    return_type=m.get('return_type', m.get('returnType', 'void')),
                    params=m.get('params', ''),
                    visibility=m.get('visibility', 'public')
                ) for m in (self.methods or [])
            ],
            relationships=[
                DomainRelationship(
                    target=r.get('target', ''),
                    type=r.get('type', 'ASSOCIATION'),
                    multiplicity=r.get('multiplicity', '1'),
                    description=r.get('description', '')
                ) for r in (self.relationships or [])
            ],
            interfaces_implemented=self.interfaces_implemented or [],
            is_interface=self.is_interface,
            is_abstract=self.is_abstract,
            order=self.order
        )


class Evaluation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attempt = models.OneToOneField(PracticeAttempt, related_name='evaluation', on_delete=models.CASCADE)
    evaluator_type = models.CharField(max_length=50, default="COMPOSITE")
    overall_score = models.IntegerField(default=0, help_text="0-100 overall score")
    overall_summary = models.TextField()
    strengths = models.JSONField(default=list, help_text="List of positive findings")
    design_issues = models.JSONField(default=list, help_text="Key design issues detected")
    missing_requirements = models.JSONField(default=list, help_text="Requirements missing explicit classes")
    solid_violations = models.JSONField(default=list, help_text="Specific SOLID principle violations")
    coupling_concerns = models.JSONField(default=list, help_text="Coupling, cohesion & God class concerns")
    extensibility_suggestions = models.JSONField(default=list, help_text="Extensibility critique")
    edge_cases_analysis = models.JSONField(default=list, help_text="Concurrency & failure edge cases")
    actionable_recommendations = models.JSONField(default=list, help_text="Concrete actionable steps")
    refactoring_plan = models.JSONField(default=list, help_text="Step-by-step recommended refactoring plan")
    improvement_areas = models.JSONField(default=list, help_text="List of areas needing work")
    category_scores = models.JSONField(default=dict, help_text="Breakdown by EvaluationCategory")
    raw_ai_response = models.TextField(null=True, blank=True)
    is_fallback = models.BooleanField(default=False)
    error_message = models.TextField(null=True, blank=True)
    evaluated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Evaluation for {self.attempt} - Score: {self.overall_score}/100"


class FeedbackItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    evaluation = models.ForeignKey(Evaluation, related_name='feedback_items', on_delete=models.CASCADE)
    category = models.CharField(
        max_length=50,
        choices=[(c.value, c.value) for c in EvaluationCategory]
    )
    source = models.CharField(
        max_length=30,
        choices=[(s.value, s.value) for s in FeedbackSource],
        default=FeedbackSource.DETERMINISTIC.value
    )
    confidence = models.CharField(
        max_length=20,
        choices=[(c.value, c.value) for c in ConfidenceLevel],
        default=ConfidenceLevel.HIGH.value
    )
    severity = models.CharField(
        max_length=20,
        choices=[(s.value, s.value) for s in FeedbackSeverity],
        default=FeedbackSeverity.INFO.value
    )
    title = models.CharField(max_length=255)
    message = models.TextField(help_text="Detailed explanation of reasoning")
    target_entity = models.CharField(max_length=150, null=True, blank=True)
    suggestion = models.TextField(null=True, blank=True, help_text="Concrete suggestion")
    why_it_matters = models.TextField(null=True, blank=True, help_text="Interview & architectural relevance")

    class Meta:
        ordering = ['category', 'severity']

    def __str__(self):
        return f"[{self.source} - {self.confidence} - {self.severity}] {self.title}"
