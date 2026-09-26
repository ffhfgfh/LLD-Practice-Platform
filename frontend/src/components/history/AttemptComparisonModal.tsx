import React, { useState } from 'react';
import { ProblemWithHistory } from '../../types';
import { Button } from '../common/Button';
import { Badge } from '../common/Badge';
import { X, TrendingUp, Layers, CheckCircle2, ArrowRight, ArrowUpRight, ArrowDownRight, GitCompare, Calendar } from 'lucide-react';
import { Link } from 'react-router-dom';

interface AttemptComparisonModalProps {
  isOpen: boolean;
  onClose: () => void;
  problem?: ProblemWithHistory | null;
}

export const AttemptComparisonModal: React.FC<AttemptComparisonModalProps> = ({
  isOpen,
  onClose,
  problem,
}) => {
  if (!isOpen || !problem) return null;

  const completedAttempts = problem.attempts.filter((a) => a.overall_score !== null);
  const firstAttempt = completedAttempts[completedAttempts.length - 1];
  const latestAttempt = completedAttempts[0];

  const scoreDelta = (latestAttempt && firstAttempt && latestAttempt.overall_score !== null && firstAttempt.overall_score !== null)
    ? latestAttempt.overall_score - firstAttempt.overall_score
    : 0;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 overflow-y-auto">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/60">
          <div>
            <span className="text-xs font-mono text-indigo-400 font-semibold uppercase flex items-center gap-1.5">
              <GitCompare className="h-4 w-4" /> Attempt Progression Analysis
            </span>
            <h3 className="text-lg font-bold text-white">{problem.title}</h3>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 overflow-y-auto space-y-6 flex-1 text-sm text-slate-300">
          {/* Progression Metric Highlights */}
          {completedAttempts.length >= 2 && (
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                <div className="text-xs text-slate-400 uppercase font-semibold">Initial Score (Attempt #{firstAttempt.attempt_number})</div>
                <div className="text-2xl font-extrabold text-white mt-1">{firstAttempt.overall_score}/100</div>
              </div>

              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                <div className="text-xs text-slate-400 uppercase font-semibold">Latest Score (Attempt #{latestAttempt.attempt_number})</div>
                <div className="text-2xl font-extrabold text-indigo-400 mt-1">{latestAttempt.overall_score}/100</div>
              </div>

              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                <div className="text-xs text-slate-400 uppercase font-semibold">Score Progression &Delta;</div>
                <div className={`text-2xl font-extrabold mt-1 flex items-center gap-1 ${
                  scoreDelta > 0 ? 'text-emerald-400' : scoreDelta < 0 ? 'text-rose-400' : 'text-slate-300'
                }`}>
                  {scoreDelta > 0 ? <ArrowUpRight className="h-6 w-6" /> : scoreDelta < 0 ? <ArrowDownRight className="h-6 w-6" /> : null}
                  {scoreDelta > 0 ? `+${scoreDelta} pts` : `${scoreDelta} pts`}
                </div>
              </div>
            </div>
          )}

          {/* Attempt Timeline */}
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-1.5">
              <TrendingUp className="h-4 w-4 text-indigo-400" />
              Iteration Timeline & Revisions ({problem.attempts.length})
            </h4>

            <div className="space-y-3">
              {problem.attempts.map((att) => (
                <div
                  key={att.id}
                  className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 hover:border-slate-700 transition-colors"
                >
                  <div className="space-y-1.5 flex-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="font-mono font-bold text-sm text-white px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
                        Attempt #{att.attempt_number}
                      </span>
                      <Badge variant="status" status={att.status} />
                      {att.overall_score !== null && (
                        <Badge variant="score" score={att.overall_score} />
                      )}
                      <span className="text-xs text-slate-500 font-mono">
                        {att.class_count} classes modeled
                      </span>
                    </div>

                    {att.solution_summary && (
                      <p className="text-xs text-slate-400 line-clamp-1 italic">
                        "{att.solution_summary}"
                      </p>
                    )}

                    <div className="text-[11px] text-slate-500 flex items-center gap-2 font-mono">
                      <Calendar className="h-3 w-3" />
                      <span>{new Date(att.started_at).toLocaleString()}</span>
                      {att.evaluator_type && (
                        <>
                          <span>&bull;</span>
                          <span>Evaluator: {att.evaluator_type}</span>
                        </>
                      )}
                    </div>
                  </div>

                  <div className="shrink-0">
                    {att.status === 'COMPLETED' ? (
                      <Link
                        to={`/attempts/${att.id}/feedback`}
                        className="inline-flex items-center gap-1 text-xs font-semibold px-3.5 py-1.5 rounded-lg bg-emerald-600/20 text-emerald-300 border border-emerald-500/30 hover:bg-emerald-600/30 transition-colors"
                      >
                        <span>View Report</span>
                        <ArrowRight className="h-3.5 w-3.5" />
                      </Link>
                    ) : (
                      <Link
                        to={`/practice/${att.id}`}
                        className="inline-flex items-center gap-1 text-xs font-semibold px-3.5 py-1.5 rounded-lg bg-indigo-600/20 text-indigo-300 border border-indigo-500/30 hover:bg-indigo-600/30 transition-colors"
                      >
                        <span>Resume</span>
                        <ArrowRight className="h-3.5 w-3.5" />
                      </Link>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-slate-800 bg-slate-950/60 flex justify-end">
          <Button variant="outline" onClick={onClose}>
            Close
          </Button>
        </div>
      </div>
    </div>
  );
};
