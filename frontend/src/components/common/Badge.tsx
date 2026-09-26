import React from 'react';
import { Difficulty, AttemptStatus, FeedbackSeverity, FeedbackSource, ConfidenceLevel } from '../../types';
import { ShieldCheck, Sparkles, HelpCircle } from 'lucide-react';

interface BadgeProps {
  children?: React.ReactNode;
  variant?: 'default' | 'difficulty' | 'status' | 'severity' | 'source' | 'confidence' | 'score' | 'tag';
  difficulty?: Difficulty;
  status?: AttemptStatus;
  severity?: FeedbackSeverity;
  source?: FeedbackSource;
  confidence?: ConfidenceLevel;
  score?: number;
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'default',
  difficulty,
  status,
  severity,
  source,
  confidence,
  score,
  className = '',
}) => {
  if (variant === 'difficulty' && difficulty) {
    const map = {
      EASY: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
      MEDIUM: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
      HARD: 'bg-rose-500/10 text-rose-400 border-rose-500/20',
    };
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold border ${map[difficulty] || ''} ${className}`}>
        {difficulty}
      </span>
    );
  }

  if (variant === 'status' && status) {
    const map = {
      DRAFT: 'bg-slate-500/10 text-slate-400 border-slate-500/20',
      SUBMITTED: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
      EVALUATING: 'bg-purple-500/10 text-purple-400 border-purple-500/20 animate-pulse',
      COMPLETED: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
      FAILED: 'bg-rose-500/10 text-rose-400 border-rose-500/20',
    };
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${map[status] || ''} ${className}`}>
        {status}
      </span>
    );
  }

  if (variant === 'severity' && severity) {
    const map = {
      POSITIVE: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30',
      INFO: 'bg-sky-500/15 text-sky-400 border-sky-500/30',
      WARNING: 'bg-amber-500/15 text-amber-400 border-amber-500/30',
      CRITICAL: 'bg-rose-500/15 text-rose-400 border-rose-500/30',
    };
    return (
      <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold uppercase tracking-wider border ${map[severity] || ''} ${className}`}>
        {severity}
      </span>
    );
  }

  if (variant === 'source' && source) {
    const isDet = source === 'DETERMINISTIC';
    return (
      <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-semibold border ${
        isDet ? 'bg-teal-500/15 text-teal-300 border-teal-500/30' : 'bg-indigo-500/15 text-indigo-300 border-indigo-500/30'
      } ${className}`}>
        {isDet ? (
          <>
            <ShieldCheck className="h-3 w-3 text-teal-400" />
            <span>Rule-Based Check</span>
          </>
        ) : (
          <>
            <Sparkles className="h-3 w-3 text-indigo-400" />
            <span>AI Reasoning</span>
          </>
        )}
      </span>
    );
  }

  if (variant === 'confidence' && confidence) {
    const map = {
      HIGH: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
      MEDIUM: 'bg-indigo-500/10 text-indigo-300 border-indigo-500/20',
      LOW: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
    };
    return (
      <span className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider border ${map[confidence]} ${className}`}>
        {confidence} Confidence
      </span>
    );
  }

  if (variant === 'tag') {
    return (
      <span className={`inline-flex items-center px-2 py-0.5 rounded-md text-[11px] font-mono bg-slate-800/80 text-slate-300 border border-slate-700/60 ${className}`}>
        {children}
      </span>
    );
  }

  if (variant === 'score' && score !== undefined) {
    let colorClass = 'bg-rose-500/10 text-rose-400 border-rose-500/20';
    if (score >= 80) colorClass = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
    else if (score >= 60) colorClass = 'bg-amber-500/10 text-amber-400 border-amber-500/20';

    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-black border ${colorClass} ${className}`}>
        {score}/100
      </span>
    );
  }

  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-slate-800 text-slate-300 border border-slate-700 ${className}`}>
      {children}
    </span>
  );
};
