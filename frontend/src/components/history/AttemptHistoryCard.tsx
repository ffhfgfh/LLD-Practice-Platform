import React from 'react';
import { Link } from 'react-router-dom';
import { ProblemWithHistory, AttemptHistoryItem } from '../../types';
import { Card } from '../common/Card';
import { Badge } from '../common/Badge';
import { Button } from '../common/Button';
import { ArrowRight, RotateCcw, Eye, Layers, GitCompare, Calendar } from 'lucide-react';

interface AttemptHistoryCardProps {
  problemHistory: ProblemWithHistory;
  onTryAgain: (problemId: string) => void;
  onCompare: (problem: ProblemWithHistory) => void;
  isStarting?: boolean;
}

export const AttemptHistoryCard: React.FC<AttemptHistoryCardProps> = ({
  problemHistory,
  onTryAgain,
  onCompare,
  isStarting = false,
}) => {
  return (
    <Card className="border-slate-800/80 bg-slate-900/60 overflow-hidden space-y-4">
      {/* Problem Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pb-3 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Badge variant="difficulty" difficulty={problemHistory.difficulty} />
            <span className="text-xs text-slate-500 font-mono">
              {problemHistory.attempts.length} {problemHistory.attempts.length === 1 ? 'attempt' : 'attempts'}
            </span>
          </div>
          <Link
            to={`/problems/${problemHistory.slug}`}
            className="text-lg font-bold text-white hover:text-indigo-400 transition-colors"
          >
            {problemHistory.title}
          </Link>
        </div>

        <div className="flex items-center gap-2">
          {problemHistory.attempts.length > 1 && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => onCompare(problemHistory)}
              leftIcon={<GitCompare className="h-3.5 w-3.5 text-indigo-400" />}
              className="text-xs"
            >
              Compare Attempts
            </Button>
          )}

          <Button
            variant="primary"
            size="sm"
            onClick={() => onTryAgain(problemHistory.id)}
            isLoading={isStarting}
            leftIcon={<RotateCcw className="h-3.5 w-3.5" />}
            className="text-xs"
          >
            Try Again
          </Button>
        </div>
      </div>

      {/* Attempts Table/List */}
      {problemHistory.attempts.length === 0 ? (
        <p className="text-xs text-slate-500 italic py-2">No attempts yet. Click 'Try Again' to start practice.</p>
      ) : (
        <div className="space-y-2">
          {problemHistory.attempts.map((att) => (
            <div
              key={att.id}
              className="rounded-lg border border-slate-800/80 bg-slate-950/40 p-3 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 hover:border-slate-700 transition-colors"
            >
              <div className="flex items-center gap-3">
                <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
                  Attempt #{att.attempt_number}
                </span>

                <Badge variant="status" status={att.status} />

                {att.overall_score !== null && (
                  <Badge variant="score" score={att.overall_score} />
                )}

                <span className="text-xs text-slate-500 flex items-center gap-1 font-mono">
                  <Layers className="h-3 w-3" /> {att.class_count} classes
                </span>
              </div>

              <div className="flex items-center gap-4 text-xs text-slate-400 w-full sm:w-auto justify-between sm:justify-end">
                <div className="flex items-center gap-1 text-[11px] text-slate-500">
                  <Calendar className="h-3 w-3" />
                  <span>{new Date(att.started_at).toLocaleDateString()}</span>
                </div>

                {att.status === 'DRAFT' ? (
                  <Link
                    to={`/practice/${att.id}`}
                    className="inline-flex items-center gap-1 text-xs font-semibold text-indigo-400 hover:text-indigo-300"
                  >
                    <span>Resume Draft</span>
                    <ArrowRight className="h-3 w-3" />
                  </Link>
                ) : (
                  <Link
                    to={`/attempts/${att.id}/feedback`}
                    className="inline-flex items-center gap-1 text-xs font-semibold text-emerald-400 hover:text-emerald-300"
                  >
                    <span>View Feedback</span>
                    <ArrowRight className="h-3 w-3" />
                  </Link>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
};
