import React, { useState } from 'react';
import { CategoryScoreData } from '../../types';
import { Card } from '../common/Card';
import { Badge } from '../common/Badge';
import { ShieldCheck, AlertTriangle, Lightbulb, Search, ChevronDown, ChevronUp, Layers } from 'lucide-react';

interface CategoryScoreCardProps {
  categoryScores: Record<string, CategoryScoreData>;
}

export const CategoryScoreGrid: React.FC<CategoryScoreCardProps> = ({ categoryScores }) => {
  const [expandedCriteria, setExpandedCriteria] = useState<Record<string, boolean>>({});

  if (!categoryScores || Object.keys(categoryScores).length === 0) return null;

  const toggleExpand = (key: string) => {
    setExpandedCriteria((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const getScoreColor = (score: number, max: number) => {
    const ratio = score / max;
    if (ratio >= 0.8) return { bar: 'bg-emerald-500', text: 'text-emerald-400', badge: 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30' };
    if (ratio >= 0.6) return { bar: 'bg-amber-500', text: 'text-amber-400', badge: 'bg-amber-500/10 text-amber-300 border-amber-500/30' };
    return { bar: 'bg-rose-500', text: 'text-rose-400', badge: 'bg-rose-500/10 text-rose-300 border-rose-500/30' };
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between flex-wrap gap-2">
        <div>
          <h3 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
            <Layers className="h-5 w-5 text-indigo-400" />
            Rubric-Based Criterion Evaluations (9 Dimensions)
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Structured format: <span className="font-mono text-indigo-300">criterion &rarr; score &rarr; evidence &rarr; concern &rarr; suggestion &rarr; confidence</span>
          </p>
        </div>
        <div className="flex items-center gap-2 text-xs">
          <button
            onClick={() => {
              const allExpanded: Record<string, boolean> = {};
              Object.keys(categoryScores).forEach((k) => (allExpanded[k] = true));
              setExpandedCriteria(allExpanded);
            }}
            className="px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white border border-slate-700 transition-colors"
          >
            Expand All
          </button>
          <button
            onClick={() => setExpandedCriteria({})}
            className="px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white border border-slate-700 transition-colors"
          >
            Collapse All
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {Object.entries(categoryScores).map(([key, data]) => {
          const score = data.score ?? 0;
          const maxScore = data.max_score || 10;
          const percentage = Math.min(100, Math.round((score / maxScore) * 100));
          const colors = getScoreColor(score, maxScore);
          const isExpanded = expandedCriteria[key] ?? true;

          const hasRichFields = data.evidence || data.concern || data.suggestion;

          return (
            <Card
              key={key}
              className="flex flex-col justify-between border-slate-800/80 bg-slate-900/50 hover:border-slate-700 transition-all shadow-sm"
            >
              <div>
                {/* Header: Criterion & Score */}
                <div className="flex items-start justify-between gap-2 mb-2">
                  <div>
                    <h4 className="text-sm font-bold text-white leading-snug">
                      {data.criterion || data.title || key.replace(/_/g, ' ').toUpperCase()}
                    </h4>
                    {data.confidence && (
                      <div className="mt-1">
                        <Badge variant="confidence" confidence={data.confidence} />
                      </div>
                    )}
                  </div>
                  <span className={`font-mono text-xs font-bold px-2 py-0.5 rounded border ${colors.badge}`}>
                    {score}/{maxScore}
                  </span>
                </div>

                {/* Progress bar */}
                <div className="w-full h-1.5 rounded-full bg-slate-800 overflow-hidden mb-3">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${colors.bar}`}
                    style={{ width: `${percentage}%` }}
                  />
                </div>

                {/* Main Rationale */}
                <p className="text-xs text-slate-300 leading-relaxed mb-3">
                  {data.rationale}
                </p>

                {/* Structured Shape Details: Evidence, Concern, Suggestion */}
                {hasRichFields && (
                  <div className="space-y-2 border-t border-slate-800/80 pt-2.5">
                    {/* Toggle */}
                    <button
                      onClick={() => toggleExpand(key)}
                      className="w-full flex items-center justify-between text-[11px] font-semibold uppercase tracking-wider text-slate-400 hover:text-slate-200"
                    >
                      <span>Rubric Evidence & Recommendations</span>
                      {isExpanded ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
                    </button>

                    {isExpanded && (
                      <div className="space-y-2.5 pt-1 text-xs animate-fade-in">
                        {/* Evidence */}
                        {data.evidence && (
                          <div className="bg-slate-950/80 p-2.5 rounded-xl border border-slate-800 text-[11px] space-y-1">
                            <span className="font-semibold text-indigo-300 flex items-center gap-1">
                              <Search className="h-3 w-3 text-indigo-400" />
                              Evidence Cited
                            </span>
                            <p className="text-slate-300 leading-relaxed italic">
                              &ldquo;{data.evidence}&rdquo;
                            </p>
                          </div>
                        )}

                        {/* Concern */}
                        {data.concern && (
                          <div className="bg-rose-500/10 p-2.5 rounded-xl border border-rose-500/20 text-[11px] space-y-1">
                            <span className="font-semibold text-rose-300 flex items-center gap-1">
                              <AlertTriangle className="h-3 w-3 text-rose-400" />
                              Identified Concern
                            </span>
                            <p className="text-slate-300 leading-relaxed">
                              {data.concern}
                            </p>
                          </div>
                        )}

                        {/* Suggestion */}
                        {data.suggestion && (
                          <div className="bg-emerald-500/10 p-2.5 rounded-xl border border-emerald-500/20 text-[11px] space-y-1">
                            <span className="font-semibold text-emerald-300 flex items-center gap-1">
                              <Lightbulb className="h-3 w-3 text-emerald-400" />
                              Concrete Improvement
                            </span>
                            <p className="text-slate-200 leading-relaxed">
                              {data.suggestion}
                            </p>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
};
