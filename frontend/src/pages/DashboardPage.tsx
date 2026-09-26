import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { DashboardData } from '../types';
import { StatCard } from '../components/common/StatCard';
import { Card } from '../components/common/Card';
import { Badge } from '../components/common/Badge';
import { Button } from '../components/common/Button';
import { ProblemCard } from '../components/problems/ProblemCard';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorAlert } from '../components/common/ErrorAlert';
import {
  BookOpen,
  CheckCircle2,
  Layers,
  Award,
  ArrowRight,
  Sparkles,
  Terminal,
  RotateCcw,
  Compass,
  FileCode,
  ShieldCheck,
} from 'lucide-react';

export const DashboardPage: React.FC = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [startingProblemId, setStartingProblemId] = useState<string | null>(null);
  const navigate = useNavigate();

  const fetchDashboard = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await api.getDashboard();
      setData(res);
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || 'Failed to load dashboard.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  const handleStartPractice = async (problemId: string) => {
    try {
      setStartingProblemId(problemId);
      const attempt = await api.createAttempt(problemId);
      navigate(`/practice/${attempt.id}`);
    } catch (err: any) {
      alert('Failed to start attempt: ' + (err?.response?.data?.detail || err?.message));
    } finally {
      setStartingProblemId(null);
    }
  };

  if (loading) return <LoadingSpinner message="Loading dashboard statistics..." />;
  if (error) return <ErrorAlert message={error} onRetry={fetchDashboard} />;
  if (!data) return null;

  return (
    <div className="space-y-10">
      {/* Hero Section */}
      <section className="relative rounded-3xl border border-slate-800 bg-gradient-to-b from-indigo-950/40 via-slate-900 to-slate-900/90 p-8 sm:p-12 overflow-hidden shadow-2xl">
        <div className="absolute -right-20 -top-20 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 max-w-3xl space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold">
            <Sparkles className="h-3.5 w-3.5" />
            <span>Interactive Low-Level Design Practice & Feedback</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight leading-tight">
            Master Object-Oriented & Low-Level Design.
          </h1>

          <p className="text-base sm:text-lg text-slate-300 leading-relaxed">
            Practice canonical LLD interview problems, design classes, responsibilities, and diagrams,
            receive explainable feedback across 9 design dimensions, and iteratively improve your architecture.
          </p>

          {/* Learner Journey Steps */}
          <div className="pt-4 grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs font-mono">
            <div className="p-2.5 rounded-lg bg-slate-950/50 border border-slate-800 text-slate-300 flex items-center gap-2">
              <span className="text-indigo-400 font-bold">01.</span> Choose Problem
            </div>
            <div className="p-2.5 rounded-lg bg-slate-950/50 border border-slate-800 text-slate-300 flex items-center gap-2">
              <span className="text-indigo-400 font-bold">02.</span> Design Solution
            </div>
            <div className="p-2.5 rounded-lg bg-slate-950/50 border border-slate-800 text-slate-300 flex items-center gap-2">
              <span className="text-indigo-400 font-bold">03.</span> Get Feedback
            </div>
            <div className="p-2.5 rounded-lg bg-slate-950/50 border border-slate-800 text-slate-300 flex items-center gap-2">
              <span className="text-indigo-400 font-bold">04.</span> Retry & Improve
            </div>
          </div>

          <div className="pt-4 flex items-center gap-3 flex-wrap">
            <Link
              to="/problems"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-sm shadow-lg shadow-indigo-500/25 transition-all hover:scale-[1.02]"
            >
              <Terminal className="h-4 w-4" />
              <span>Explore All Problems</span>
              <ArrowRight className="h-4 w-4" />
            </Link>

            <Link
              to="/attempts"
              className="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-sm border border-slate-700 transition-colors"
            >
              <RotateCcw className="h-4 w-4 text-slate-400" />
              <span>Review Past Attempts</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Analytics Stats Grid */}
      <section className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Problems Practiced"
          value={`${data.stats.problems_practiced} / ${data.stats.total_problems}`}
          subtitle={`${Math.round((data.stats.problems_practiced / Math.max(1, data.stats.total_problems)) * 100)}% coverage`}
          icon={<BookOpen className="h-6 w-6" />}
          color="indigo"
        />
        <StatCard
          title="Total Practice Attempts"
          value={data.stats.total_attempts}
          subtitle="Includes revisions"
          icon={<Layers className="h-6 w-6" />}
          color="sky"
        />
        <StatCard
          title="Completed Evaluations"
          value={data.stats.completed_evaluations}
          subtitle="Assessed submissions"
          icon={<CheckCircle2 className="h-6 w-6" />}
          color="emerald"
        />
        <StatCard
          title="Average Score"
          value={data.stats.average_score > 0 ? `${data.stats.average_score}/100` : 'N/A'}
          subtitle="Across all attempts"
          icon={<Award className="h-6 w-6" />}
          color="amber"
        />
      </section>

      {/* Main Dashboard Content: Recommended & Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left 2 Cols: Recommended Problems */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-white tracking-tight">
                Recommended Problems
              </h2>
              <p className="text-xs text-slate-400">
                Core Low-Level Design challenges with full requirement specifications.
              </p>
            </div>

            <Link
              to="/problems"
              className="text-xs font-semibold text-indigo-400 hover:text-indigo-300 flex items-center gap-1"
            >
              <span>View all ({data.stats.total_problems})</span>
              <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {data.recommended_problems.map((problem) => (
              <ProblemCard
                key={problem.id}
                problem={problem}
                onStartPractice={handleStartPractice}
                isStarting={startingProblemId === problem.id}
              />
            ))}
          </div>
        </div>

        {/* Right 1 Col: Recent Attempts */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-white tracking-tight">
              Recent Attempts
            </h2>
            <Link
              to="/attempts"
              className="text-xs font-semibold text-indigo-400 hover:text-indigo-300 flex items-center gap-1"
            >
              <span>History</span>
              <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>

          {data.recent_attempts.length === 0 ? (
            <Card className="text-center py-8">
              <Compass className="h-8 w-8 text-slate-600 mx-auto mb-2" />
              <p className="text-sm font-semibold text-slate-300">No attempts yet</p>
              <p className="text-xs text-slate-500 mt-1 mb-4">
                Pick a problem from the catalog to start your first design attempt.
              </p>
              <Link to="/problems">
                <Button size="sm" variant="outline">
                  Browse Problems
                </Button>
              </Link>
            </Card>
          ) : (
            <div className="space-y-2.5">
              {data.recent_attempts.map((att) => (
                <Card key={att.id} className="p-3.5 border-slate-800 hover:border-slate-700 transition-colors">
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <div className="flex items-center gap-1.5 mb-1">
                        <Badge variant="difficulty" difficulty={att.problem_difficulty} />
                        <span className="text-[11px] font-mono text-indigo-300 font-semibold">
                          Attempt #{att.attempt_number}
                        </span>
                      </div>
                      <h4 className="font-bold text-sm text-white line-clamp-1">
                        {att.problem_title}
                      </h4>
                    </div>

                    <div className="text-right shrink-0">
                      {att.overall_score !== null ? (
                        <Badge variant="score" score={att.overall_score} />
                      ) : (
                        <Badge variant="status" status={att.status} />
                      )}
                    </div>
                  </div>

                  <div className="mt-3 pt-2 border-t border-slate-800/80 flex items-center justify-between text-xs">
                    <span className="text-slate-500 text-[11px]">
                      {new Date(att.started_at).toLocaleDateString()}
                    </span>

                    {att.status === 'DRAFT' ? (
                      <Link
                        to={`/practice/${att.id}`}
                        className="font-semibold text-indigo-400 hover:text-indigo-300 inline-flex items-center gap-1"
                      >
                        <span>Resume</span>
                        <ArrowRight className="h-3 w-3" />
                      </Link>
                    ) : (
                      <Link
                        to={`/attempts/${att.id}/feedback`}
                        className="font-semibold text-emerald-400 hover:text-emerald-300 inline-flex items-center gap-1"
                      >
                        <span>Feedback</span>
                        <ArrowRight className="h-3 w-3" />
                      </Link>
                    )}
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
