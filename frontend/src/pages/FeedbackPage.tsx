import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { PracticeAttempt } from '../types';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorAlert } from '../components/common/ErrorAlert';
import { Button } from '../components/common/Button';
import { EvaluationScoreCard } from '../components/evaluation/EvaluationScoreCard';
import { CategoryScoreGrid } from '../components/evaluation/CategoryScoreCard';
import { StrengthsWeaknessesSection } from '../components/evaluation/StrengthsWeaknessesSection';
import { DeepCategorizedFeedbackSection } from '../components/evaluation/DeepCategorizedFeedbackSection';
import { ActionableRecommendationsSection } from '../components/evaluation/ActionableRecommendationsSection';
import { FeedbackItemsList } from '../components/evaluation/FeedbackItemsList';
import { SubmissionSnapshotModal } from '../components/evaluation/SubmissionSnapshotModal';
import { ArrowLeft, RotateCcw, RefreshCw, GitCompare } from 'lucide-react';

export const FeedbackPage: React.FC = () => {
  const { attemptId } = useParams<{ attemptId: string }>();
  const navigate = useNavigate();

  const [attempt, setAttempt] = useState<PracticeAttempt | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isSnapshotOpen, setIsSnapshotOpen] = useState(false);
  const [isRetrying, setIsRetrying] = useState(false);

  const fetchAttempt = async () => {
    if (!attemptId) return;
    try {
      setLoading(true);
      setError(null);
      const data = await api.getAttempt(attemptId);
      setAttempt(data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || 'Failed to load evaluation.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAttempt();
  }, [attemptId]);

  const handleTryAgain = async () => {
    if (!attempt) return;
    try {
      setIsRetrying(true);
      const newAttempt = await api.createAttempt(attempt.problem.id);
      navigate(`/practice/${newAttempt.id}`);
    } catch (err: any) {
      alert('Failed to start new attempt: ' + (err?.response?.data?.detail || err?.message));
    } finally {
      setIsRetrying(false);
    }
  };

  const handleRetryEvaluation = async () => {
    if (!attemptId) return;
    try {
      setLoading(true);
      const reEvaluated = await api.retryEvaluation(attemptId);
      setAttempt(reEvaluated);
    } catch (err: any) {
      alert('Evaluation retry failed: ' + (err?.response?.data?.detail || err?.message));
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner message="Loading evaluation results and architectural feedback..." />;
  if (error) return <ErrorAlert message={error} onRetry={fetchAttempt} />;
  if (!attempt) return null;

  const evaluation = attempt.evaluation;

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Navigation Header */}
      <div className="flex items-center justify-between">
        <Link
          to={`/problems/${attempt.problem.slug}`}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Back to Problem Requirements</span>
        </Link>

        <div className="flex items-center gap-3">
          <Link
            to="/attempts"
            className="text-xs font-semibold text-slate-400 hover:text-indigo-400 transition-colors flex items-center gap-1"
          >
            <GitCompare className="h-3.5 w-3.5" />
            <span>Attempt History & Progression</span>
          </Link>
        </div>
      </div>

      {/* Main Score & Summary Card */}
      {evaluation ? (
        <EvaluationScoreCard
          evaluation={evaluation}
          problemTitle={attempt.problem.title}
          attemptNumber={attempt.attempt_number}
          status={attempt.status}
          onTryAgain={handleTryAgain}
          onViewSnapshot={() => setIsSnapshotOpen(true)}
          isRetrying={isRetrying}
        />
      ) : (
        <div className="rounded-2xl border border-amber-500/30 bg-amber-500/10 p-6 text-center space-y-3">
          <h3 className="text-lg font-bold text-amber-300">Evaluation Pending or Failed</h3>
          <p className="text-sm text-slate-300">
            This attempt does not have completed evaluation results. You can re-trigger evaluation below.
          </p>
          <Button
            variant="primary"
            onClick={handleRetryEvaluation}
            leftIcon={<RefreshCw className="h-4 w-4" />}
          >
            Run Evaluation Now
          </Button>
        </div>
      )}

      {/* Strengths & Overview Growth Areas */}
      {evaluation && (
        <StrengthsWeaknessesSection
          strengths={evaluation.strengths || []}
          improvementAreas={evaluation.improvement_areas || []}
        />
      )}

      {/* Deep Categorized Design Analyses & Step-by-Step Refactoring */}
      {evaluation && (
        <DeepCategorizedFeedbackSection
          designIssues={evaluation.design_issues}
          missingRequirements={evaluation.missing_requirements}
          solidViolations={evaluation.solid_violations}
          couplingConcerns={evaluation.coupling_concerns}
          extensibilitySuggestions={evaluation.extensibility_suggestions}
          edgeCasesAnalysis={evaluation.edge_cases_analysis}
          refactoringPlan={evaluation.refactoring_plan}
        />
      )}

      {/* Actionable Concrete Recommendations */}
      {evaluation && (
        <ActionableRecommendationsSection
          recommendations={evaluation.actionable_recommendations || []}
        />
      )}

      {/* Category Breakdown Grid (9 dimensions) */}
      {evaluation && (
        <CategoryScoreGrid
          categoryScores={evaluation.category_scores || {}}
        />
      )}

      {/* Filterable Feedback Items (Deterministic vs AI with Confidence) */}
      {evaluation && (
        <FeedbackItemsList
          items={evaluation.feedback_items || []}
        />
      )}

      {/* Bottom Try Again Call to Action */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <h4 className="text-base font-bold text-white">Iterate & Improve</h4>
          <p className="text-xs text-slate-400 mt-0.5">
            Apply the refactoring suggestions above in a new attempt to refine your design architecture.
          </p>
        </div>
        <Button
          variant="primary"
          onClick={handleTryAgain}
          isLoading={isRetrying}
          leftIcon={<RotateCcw className="h-4 w-4" />}
          className="font-bold text-sm shadow-indigo-500/25"
        >
          Try Again (Attempt #{attempt.attempt_number + 1})
        </Button>
      </div>

      {/* Solution Snapshot Modal */}
      <SubmissionSnapshotModal
        isOpen={isSnapshotOpen}
        onClose={() => setIsSnapshotOpen(false)}
        solution={attempt.solution}
        problemTitle={attempt.problem.title}
      />
    </div>
  );
};
