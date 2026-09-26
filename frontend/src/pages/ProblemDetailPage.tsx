import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { LLDProblemDetail } from '../types';
import { Badge } from '../components/common/Badge';
import { Button } from '../components/common/Button';
import { Card } from '../components/common/Card';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorAlert } from '../components/common/ErrorAlert';
import { RequirementsList } from '../components/problems/RequirementsList';
import {
  ConstraintsSection,
  DesignConsiderationsSection,
  HintsSection,
} from '../components/problems/ProblemDetailsSections';
import {
  BookOpen,
  ArrowLeft,
  Terminal,
  Clock,
  Tag,
  CheckCircle2,
} from 'lucide-react';

export const ProblemDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [problem, setProblem] = useState<LLDProblemDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isStarting, setIsStarting] = useState(false);
  const navigate = useNavigate();

  const fetchProblem = async () => {
    if (!id) return;
    try {
      setLoading(true);
      setError(null);
      const data = await api.getProblem(id);
      setProblem(data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || 'Problem not found.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProblem();
  }, [id]);

  const handleStartAttempt = async () => {
    if (!problem) return;
    try {
      setIsStarting(true);
      const attempt = await api.createAttempt(problem.id);
      navigate(`/practice/${attempt.id}`);
    } catch (err: any) {
      alert('Failed to start attempt: ' + (err?.response?.data?.detail || err?.message));
    } finally {
      setIsStarting(false);
    }
  };

  if (loading) return <LoadingSpinner message="Loading problem specifications..." />;
  if (error) return <ErrorAlert message={error} onRetry={fetchProblem} />;
  if (!problem) return null;

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Back button */}
      <div>
        <Link
          to="/problems"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Back to All Problems</span>
        </Link>
      </div>

      {/* Header Banner */}
      <div className="rounded-3xl border border-slate-800 bg-gradient-to-r from-slate-900 via-slate-900 to-indigo-950/40 p-6 sm:p-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 shadow-xl">
        <div className="space-y-2.5 max-w-2xl">
          <div className="flex items-center gap-2.5 flex-wrap">
            <Badge variant="difficulty" difficulty={problem.difficulty} />
            <span className="inline-flex items-center gap-1 text-xs font-mono text-slate-300 px-2.5 py-0.5 rounded-full bg-slate-800 border border-slate-700">
              <Clock className="h-3.5 w-3.5 text-indigo-400" />
              Target Time: ~{problem.estimated_time_minutes || 45} mins
            </span>
            <span className="text-xs text-slate-400 font-mono">
              {problem.requirements.length} Requirements
            </span>
          </div>

          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            {problem.title}
          </h1>

          <p className="text-sm text-slate-300 leading-relaxed">
            {problem.summary}
          </p>

          {/* Tags */}
          {problem.tags && problem.tags.length > 0 && (
            <div className="flex items-center gap-1.5 flex-wrap pt-1">
              {problem.tags.map((tag, idx) => (
                <Badge key={idx} variant="tag">
                  {tag}
                </Badge>
              ))}
            </div>
          )}
        </div>

        {/* Start Practice CTA */}
        <div className="flex flex-col sm:flex-row md:flex-col gap-3 shrink-0 w-full md:w-auto">
          <Button
            variant="primary"
            size="lg"
            onClick={handleStartAttempt}
            isLoading={isStarting}
            leftIcon={<Terminal className="h-5 w-5" />}
            className="w-full text-sm font-bold shadow-indigo-500/25"
          >
            Start Practice Attempt
          </Button>

          {problem.latest_attempt_id && (
            <Link to={`/practice/${problem.latest_attempt_id}`}>
              <Button variant="outline" size="md" className="w-full text-xs">
                Resume Recent Attempt
              </Button>
            </Link>
          )}
        </div>
      </div>

      {/* Problem Statement Markdown */}
      <Card className="space-y-3">
        <h3 className="text-base font-bold text-white tracking-tight border-b border-slate-800 pb-2 flex items-center gap-2">
          <BookOpen className="h-4 w-4 text-indigo-400" />
          Problem Overview & Context
        </h3>
        <div className="text-sm text-slate-300 leading-relaxed whitespace-pre-line space-y-2 font-sans">
          {problem.problem_statement}
        </div>
      </Card>

      {/* Functional Requirements separated into Phase 1 (Core) vs Phase 2 (Advanced) */}
      <div className="space-y-3">
        <h3 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
          <CheckCircle2 className="h-4 w-4 text-emerald-400" />
          Progressive Functional Requirements ({problem.requirements.length})
        </h3>
        <RequirementsList requirements={problem.requirements} />
      </div>

      {/* Constraints & Design Considerations */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <ConstraintsSection constraints={problem.constraints} />
        <DesignConsiderationsSection considerations={problem.expected_design_considerations} />
      </div>

      {/* Progressive Hints */}
      <HintsSection hints={problem.hints} />

      {/* Sticky Bottom CTA */}
      <div className="pt-6 border-t border-slate-800 flex items-center justify-between flex-wrap gap-4">
        <div className="text-xs text-slate-400">
          Ready to design the solution? Model classes, define single responsibilities, and generate your class diagram.
        </div>
        <Button
          variant="primary"
          onClick={handleStartAttempt}
          isLoading={isStarting}
          leftIcon={<Terminal className="h-4 w-4" />}
          className="text-sm font-bold"
        >
          Start Practice Attempt
        </Button>
      </div>
    </div>
  );
};
