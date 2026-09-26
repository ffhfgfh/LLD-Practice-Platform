from rest_framework import serializers
from core.models import (
    LLDProblem,
    ProblemRequirement,
    PracticeAttempt,
    Solution,
    ClassDesign,
    Evaluation,
    FeedbackItem
)

class ProblemRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemRequirement
        fields = ['id', 'req_code', 'title', 'description', 'category', 'keywords', 'is_advanced', 'order']


class LLDProblemListSerializer(serializers.ModelSerializer):
    requirements_count = serializers.SerializerMethodField()
    attempts_count = serializers.SerializerMethodField()
    latest_score = serializers.SerializerMethodField()
    latest_attempt_id = serializers.SerializerMethodField()

    class Meta:
        model = LLDProblem
        fields = [
            'id', 'slug', 'title', 'difficulty', 'estimated_time_minutes', 'tags', 'summary',
            'requirements_count', 'attempts_count', 'latest_score', 'latest_attempt_id',
            'created_at'
        ]

    def get_requirements_count(self, obj):
        return obj.requirements.count()

    def get_attempts_count(self, obj):
        return obj.attempts.count()

    def get_latest_score(self, obj):
        latest = obj.attempts.filter(status='COMPLETED', evaluation__isnull=False).order_by('-started_at').first()
        if latest and hasattr(latest, 'evaluation'):
            return latest.evaluation.overall_score
        return None

    def get_latest_attempt_id(self, obj):
        latest = obj.attempts.order_by('-started_at').first()
        return str(latest.id) if latest else None


class LLDProblemDetailSerializer(serializers.ModelSerializer):
    requirements = ProblemRequirementSerializer(many=True, read_only=True)
    attempts_count = serializers.SerializerMethodField()
    latest_attempt_id = serializers.SerializerMethodField()

    class Meta:
        model = LLDProblem
        fields = [
            'id', 'slug', 'title', 'difficulty', 'estimated_time_minutes', 'tags', 'summary',
            'problem_statement', 'constraints', 'expected_design_considerations',
            'hints', 'requirements', 'attempts_count', 'latest_attempt_id',
            'created_at'
        ]

    def get_attempts_count(self, obj):
        return obj.attempts.count()

    def get_latest_attempt_id(self, obj):
        latest = obj.attempts.order_by('-started_at').first()
        return str(latest.id) if latest else None


class ClassDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassDesign
        fields = [
            'id', 'name', 'responsibility', 'attributes', 'methods',
            'relationships', 'interfaces_implemented', 'is_interface', 'is_abstract', 'order'
        ]


class SolutionSerializer(serializers.ModelSerializer):
    classes = ClassDesignSerializer(many=True, read_only=True)

    class Meta:
        model = Solution
        fields = [
            'id', 'summary', 'assumptions_and_tradeoffs',
            'design_patterns_used', 'mermaid_diagram', 'classes', 'created_at', 'updated_at'
        ]


class FeedbackItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackItem
        fields = [
            'id', 'category', 'source', 'confidence', 'severity',
            'title', 'message', 'target_entity', 'suggestion', 'why_it_matters'
        ]


class EvaluationSerializer(serializers.ModelSerializer):
    feedback_items = FeedbackItemSerializer(many=True, read_only=True)

    class Meta:
        model = Evaluation
        fields = [
            'id', 'evaluator_type', 'overall_score', 'overall_summary',
            'strengths', 'design_issues', 'missing_requirements', 'solid_violations',
            'coupling_concerns', 'extensibility_suggestions', 'edge_cases_analysis',
            'actionable_recommendations', 'refactoring_plan', 'improvement_areas',
            'category_scores', 'is_fallback', 'error_message', 'evaluated_at',
            'feedback_items'
        ]


class PracticeAttemptSerializer(serializers.ModelSerializer):
    problem = LLDProblemDetailSerializer(read_only=True)
    solution = SolutionSerializer(read_only=True)
    evaluation = EvaluationSerializer(read_only=True)
    is_mutable = serializers.BooleanField(read_only=True)

    class Meta:
        model = PracticeAttempt
        fields = [
            'id', 'problem', 'attempt_number', 'status', 'started_at',
            'submitted_at', 'last_saved_at', 'solution', 'evaluation', 'is_mutable'
        ]


class AttemptHistoryItemSerializer(serializers.ModelSerializer):
    overall_score = serializers.SerializerMethodField()
    evaluator_type = serializers.SerializerMethodField()
    class_count = serializers.SerializerMethodField()
    solution_summary = serializers.SerializerMethodField()

    class Meta:
        model = PracticeAttempt
        fields = [
            'id', 'attempt_number', 'status', 'started_at',
            'submitted_at', 'overall_score', 'evaluator_type', 'class_count', 'solution_summary'
        ]

    def get_overall_score(self, obj):
        if hasattr(obj, 'evaluation'):
            return obj.evaluation.overall_score
        return None

    def get_evaluator_type(self, obj):
        if hasattr(obj, 'evaluation'):
            return obj.evaluation.evaluator_type
        return None

    def get_class_count(self, obj):
        if hasattr(obj, 'solution'):
            return obj.solution.classes.count()
        return 0

    def get_solution_summary(self, obj):
        if hasattr(obj, 'solution'):
            return obj.solution.summary
        return ""


class ProblemWithHistorySerializer(serializers.ModelSerializer):
    attempts = AttemptHistoryItemSerializer(many=True, read_only=True)
    total_attempts = serializers.SerializerMethodField()
    best_score = serializers.SerializerMethodField()
    latest_attempt = serializers.SerializerMethodField()

    class Meta:
        model = LLDProblem
        fields = [
            'id', 'slug', 'title', 'difficulty', 'estimated_time_minutes', 'tags', 'summary',
            'attempts', 'total_attempts', 'best_score', 'latest_attempt'
        ]

    def get_total_attempts(self, obj):
        return obj.attempts.count()

    def get_best_score(self, obj):
        scores = [
            a.evaluation.overall_score
            for a in obj.attempts.all()
            if hasattr(a, 'evaluation') and a.evaluation and a.evaluation.overall_score is not None
        ]
        return max(scores) if scores else None

    def get_latest_attempt(self, obj):
        latest = obj.attempts.order_by('-started_at').first()
        if latest:
            return AttemptHistoryItemSerializer(latest).data
        return None
