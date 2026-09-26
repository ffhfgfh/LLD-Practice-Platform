import uuid
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from django.db.models import Count, Max, Q

from core.models import (
    LLDProblem,
    PracticeAttempt,
    Evaluation
)
from core.serializers import (
    LLDProblemListSerializer,
    LLDProblemDetailSerializer,
    PracticeAttemptSerializer,
    EvaluationSerializer,
    ProblemWithHistorySerializer,
    AttemptHistoryItemSerializer
)
from core.services.attempt_service import AttemptService
from core.domain.enums import AttemptStatus

class ProblemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing and retrieving LLD problems.
    """
    queryset = LLDProblem.objects.all().prefetch_related('requirements', 'attempts')
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LLDProblemDetailSerializer
        return LLDProblemListSerializer

    def get_object(self):
        lookup = self.kwargs.get('pk')
        try:
            # Try UUID lookup
            val = uuid.UUID(lookup)
            return LLDProblem.objects.prefetch_related('requirements', 'attempts').get(id=val)
        except (ValueError, LLDProblem.DoesNotExist):
            # Try slug lookup
            try:
                return LLDProblem.objects.prefetch_related('requirements', 'attempts').get(slug=lookup)
            except LLDProblem.DoesNotExist:
                raise NotFound(f"Problem '{lookup}' not found.")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        difficulty = request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty.upper())

        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(summary__icontains=search) |
                Q(problem_statement__icontains=search)
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AttemptViewSet(viewsets.ViewSet):
    """
    API endpoint for managing practice attempts, saving drafts, submitting, and triggering evaluation.
    """

    def retrieve(self, request, pk=None):
        try:
            attempt = PracticeAttempt.objects.select_related(
                'problem', 'solution', 'evaluation'
            ).prefetch_related(
                'problem__requirements',
                'solution__classes',
                'evaluation__feedback_items'
            ).get(id=pk)
        except (PracticeAttempt.DoesNotExist, ValueError):
            raise NotFound(f"Attempt '{pk}' not found.")

        serializer = PracticeAttemptSerializer(attempt)
        return Response(serializer.data)

    def create(self, request):
        problem_id = request.data.get('problem_id')
        if not problem_id:
            raise ValidationError({'problem_id': 'This field is required.'})

        attempt = AttemptService.create_attempt(problem_id)
        # Fetch fresh with relations
        attempt = PracticeAttempt.objects.select_related('problem', 'solution').prefetch_related('problem__requirements', 'solution__classes').get(id=attempt.id)
        serializer = PracticeAttemptSerializer(attempt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Save draft updates to an attempt."""
        attempt = AttemptService.save_draft(pk, request.data)
        attempt = PracticeAttempt.objects.select_related(
            'problem', 'solution', 'evaluation'
        ).prefetch_related(
            'problem__requirements',
            'solution__classes',
            'evaluation__feedback_items'
        ).get(id=attempt.id)
        serializer = PracticeAttemptSerializer(attempt)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        return self.update(request, pk=pk)

    @action(detail=True, methods=['post'], url_path='save')
    def save_draft(self, request, pk=None):
        """Explicit save draft action endpoint."""
        return self.update(request, pk=pk)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Validate and submit the attempt for evaluation."""
        evaluator_type = request.data.get('evaluator_type')
        attempt = AttemptService.submit_attempt(pk, evaluator_type=evaluator_type)
        attempt = PracticeAttempt.objects.select_related(
            'problem', 'solution', 'evaluation'
        ).prefetch_related(
            'problem__requirements',
            'solution__classes',
            'evaluation__feedback_items'
        ).get(id=attempt.id)
        serializer = PracticeAttemptSerializer(attempt)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def evaluate(self, request, pk=None):
        """Retry evaluation on an existing attempt."""
        evaluator_type = request.data.get('evaluator_type')
        attempt = AttemptService.retry_evaluation(pk, evaluator_type=evaluator_type)
        attempt = PracticeAttempt.objects.select_related(
            'problem', 'solution', 'evaluation'
        ).prefetch_related(
            'problem__requirements',
            'solution__classes',
            'evaluation__feedback_items'
        ).get(id=attempt.id)
        serializer = PracticeAttemptSerializer(attempt)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EvaluationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing evaluation details.
    """
    queryset = Evaluation.objects.select_related('attempt', 'attempt__problem').prefetch_related('feedback_items')
    serializer_class = EvaluationSerializer


@api_view(['GET'])
def history_view(request):
    """
    Returns all problems grouped with their past attempts.
    """
    problems = LLDProblem.objects.prefetch_related(
        'attempts', 'attempts__evaluation', 'attempts__solution'
    ).all()

    serializer = ProblemWithHistorySerializer(problems, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def dashboard_view(request):
    """
    Returns high-level learner statistics and recent activity for the dashboard.
    """
    total_problems = LLDProblem.objects.count()
    total_attempts = PracticeAttempt.objects.count()
    completed_evaluations = PracticeAttempt.objects.filter(status=AttemptStatus.COMPLETED.value).count()
    
    # Practiced problems = problems with at least 1 attempt
    practiced_problem_ids = PracticeAttempt.objects.values_list('problem_id', flat=True).distinct()
    problems_practiced = len(practiced_problem_ids)

    # Average score
    completed_evals = Evaluation.objects.filter(overall_score__gt=0)
    avg_score = 0
    if completed_evals.exists():
        avg_score = int(round(sum(e.overall_score for e in completed_evals) / completed_evals.count()))

    # Recent attempts
    recent_attempts_qs = PracticeAttempt.objects.select_related(
        'problem', 'evaluation'
    ).order_by('-started_at')[:5]
    
    recent_attempts = []
    for att in recent_attempts_qs:
        recent_attempts.append({
            "id": str(att.id),
            "problem_id": str(att.problem.id),
            "problem_title": att.problem.title,
            "problem_difficulty": att.problem.difficulty,
            "attempt_number": att.attempt_number,
            "status": att.status,
            "overall_score": att.evaluation.overall_score if hasattr(att, 'evaluation') and att.evaluation else None,
            "started_at": att.started_at,
            "submitted_at": att.submitted_at
        })

    # Recommended problems (unattempted or lowest score)
    unattempted = LLDProblem.objects.exclude(id__in=practiced_problem_ids)[:3]
    recommended_serializer = LLDProblemListSerializer(unattempted, many=True)

    return Response({
        "stats": {
            "total_problems": total_problems,
            "problems_practiced": problems_practiced,
            "total_attempts": total_attempts,
            "completed_evaluations": completed_evaluations,
            "average_score": avg_score
        },
        "recent_attempts": recent_attempts,
        "recommended_problems": recommended_serializer.data
    })
