import React from 'react';
import { Evaluation, AttemptStatus } from '../../types';
import { Card } from '../common/Card';
import { Badge } from '../common/Badge';
import { Button } from '../common/Button';
import { Award, RotateCcw, AlertTriangle, Eye, ShieldCheck, Sparkles } from 'lucide-react';

interface EvaluationScoreCardProps {
  evaluation: Evaluation;
  problemTitle: string;
  attemptNumber: number;
  status: AttemptStatus;
  onTryAgain: () => void;
  onViewSnapshot: () => void;
  isRetrying?: boolean;
}

export const EvaluationScoreCard: React.FC<EvaluationScoreCardProps> = ({
  evaluation,
  problemTitle,
  attemptNumber,
  status,
  onTryAgain,
  onViewSnapshot,
  isRetrying = false,
}) => {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10';
    if (score >= 60) return 'text-amber-400 border-amber-500/30 bg-amber-500/10';
    return 'text-rose-400 border-rose-500/30 bg-rose-500/10';
  };

  const getEvaluatorLabel = (type: string) => {
    if (type === 'COMPOSITE') return 'Composite (Deterministic + AI)';
    if (type.startsWith('AI_')) return `AI Evaluator (${type.replace('AI_', '')})`;
    if (type === 'RULE_BASED_FALLBACK') return 'Deterministic (AI Offline Fallback)';
    return 'Deterministic Rule-Based';
  };

  return (
    <div className="space-y-4">
      {/* Fallback Notice if AI failed */}
      {evaluation.is_fallback && (
        <div className="rounded-xl border border-amber-500/30 bg-amber-500/10 p-4 flex items-start gap-3">
          <AlertTriangle className="h-5 w-5 text-amber-400 shrink-0 mt-0.5" />
          <div className="text-sm">
            <p className="font-semibold text-amber-300">Deterministic Evaluation Mode</p>
            <p className="text-amber-200/80 mt-0.5">
              {evaluation.error_message || 'AI service was unavailable or unconfigured. Full deterministic structural evaluation was completed successfully.'}
            </p>
          </div>
        </div>
      )}

      {/* Main Score Banner */}
      <Card className="bg-gradient-to-br from-slate-900 via-slate-900/90 to-indigo-950/40 border-slate-800">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            <div className="flex items-center gap-2.5 flex-wrap">
              <span className="text-xs font-mono font-semibold px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                Attempt #{attemptNumber}
              </span>
              <Badge variant="status" status={status} />
              <span className="text-xs font-medium px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700 flex items-center gap-1.5">
                {evaluation.evaluator_type === 'COMPOSITE' ? (
                  <Sparkles className="h-3 w-3 text-indigo-400" />
                ) : (
                  <ShieldCheck className="h-3 w-3 text-teal-400" />
                )}
                {getEvaluatorLabel(evaluation.evaluator_type)}
              </span>
            </div>

            <h2 className="text-2xl font-extrabold text-white tracking-tight">
              Evaluation for {problemTitle}
            </h2>

            <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-line">
              {evaluation.overall_summary}
            </p>
          </div>

          {/* Score & Actions */}
          <div className="flex flex-col sm:flex-row md:flex-col items-center gap-4 shrink-0 w-full md:w-auto">
            <div className={`h-28 w-28 rounded-2xl border-2 flex flex-col items-center justify-center shadow-lg ${getScoreColor(evaluation.overall_score)}`}>
              <span className="text-3xl font-black tracking-tight">{evaluation.overall_score}</span>
              <span className="text-[10px] uppercase font-bold tracking-widest text-slate-400 mt-0.5">out of 100</span>
            </div>

            <div className="flex flex-col gap-2 w-full">
              <Button
                variant="primary"
                onClick={onTryAgain}
                isLoading={isRetrying}
                leftIcon={<RotateCcw className="h-4 w-4" />}
                className="w-full text-xs font-bold"
              >
                Try Again (New Attempt)
              </Button>

              <Button
                variant="outline"
                onClick={onViewSnapshot}
                leftIcon={<Eye className="h-4 w-4" />}
                className="w-full text-xs"
              >
                Review Submitted Solution
              </Button>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};
