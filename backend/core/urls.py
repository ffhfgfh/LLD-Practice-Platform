from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    ProblemViewSet,
    AttemptViewSet,
    EvaluationViewSet,
    history_view,
    dashboard_view
)

router = DefaultRouter()
router.register(r'problems', ProblemViewSet, basename='problem')
router.register(r'attempts', AttemptViewSet, basename='attempt')
router.register(r'evaluations', EvaluationViewSet, basename='evaluation')

urlpatterns = [
    path('history/', history_view, name='history'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('', include(router.urls)),
]
