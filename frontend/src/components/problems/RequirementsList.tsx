import React from 'react';
import { ProblemRequirement } from '../../types';
import { Tag, Sparkles, CheckSquare, Square } from 'lucide-react';

interface RequirementsListProps {
  requirements: ProblemRequirement[];
  compact?: boolean;
  checkedReqs?: string[];
  onToggleReq?: (code: string) => void;
}

export const RequirementsList: React.FC<RequirementsListProps> = ({
  requirements,
  compact = false,
  checkedReqs = [],
  onToggleReq,
}) => {
  if (!requirements || requirements.length === 0) {
    return <p className="text-sm text-slate-500 italic">No functional requirements specified.</p>;
  }

  const coreReqs = requirements.filter((r) => !r.is_advanced);
  const advancedReqs = requirements.filter((r) => r.is_advanced);

  const renderReqItem = (req: ProblemRequirement) => {
    const isChecked = checkedReqs.includes(req.req_code);

    return (
      <div
        key={req.id || req.req_code}
        onClick={() => onToggleReq && onToggleReq(req.req_code)}
        className={`rounded-lg border p-3 transition-all ${
          onToggleReq ? 'cursor-pointer' : ''
        } ${
          isChecked
            ? 'border-emerald-500/40 bg-emerald-500/5'
            : 'border-slate-800/80 bg-slate-900/40 hover:border-slate-700/80'
        }`}
      >
        <div className="flex items-start justify-between gap-2">
          <div className="flex items-center gap-2 flex-wrap">
            {onToggleReq && (
              <button type="button" className="text-slate-400 hover:text-emerald-400">
                {isChecked ? (
                  <CheckSquare className="h-4 w-4 text-emerald-400" />
                ) : (
                  <Square className="h-4 w-4 text-slate-500" />
                )}
              </button>
            )}

            <span className={`inline-flex items-center px-1.5 py-0.5 rounded text-[11px] font-mono font-bold border ${
              isChecked
                ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30'
                : 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20'
            }`}>
              {req.req_code}
            </span>

            <h4 className={`text-xs sm:text-sm font-semibold ${isChecked ? 'text-emerald-200 line-through' : 'text-slate-200'}`}>
              {req.title}
            </h4>
          </div>

          <div className="flex items-center gap-1.5 shrink-0">
            {req.is_advanced && (
              <span className="text-[10px] font-mono text-purple-300 px-1.5 py-0.5 rounded bg-purple-500/15 border border-purple-500/30 flex items-center gap-1">
                <Sparkles className="h-2.5 w-2.5 text-purple-400" /> Phase 2
              </span>
            )}
            {req.category && (
              <span className="text-[10px] font-mono text-slate-400 px-1.5 py-0.5 rounded bg-slate-800">
                {req.category}
              </span>
            )}
          </div>
        </div>

        <p className={`text-xs sm:text-sm mt-1.5 leading-relaxed ${isChecked ? 'text-slate-400' : 'text-slate-300'}`}>
          {req.description}
        </p>

        {!compact && req.keywords && req.keywords.length > 0 && (
          <div className="mt-2.5 flex items-center gap-1.5 flex-wrap">
            <span className="text-[10px] text-slate-400 flex items-center gap-1">
              <Tag className="h-3 w-3 text-slate-500" /> Expected Entities:
            </span>
            {req.keywords.map((kw, i) => (
              <span
                key={i}
                className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700/50"
              >
                {kw}
              </span>
            ))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="space-y-4">
      {/* Core Requirements */}
      <div className="space-y-2">
        <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center justify-between">
          <span>Phase 1: Core Domain MVP Requirements ({coreReqs.length})</span>
        </div>
        <div className="space-y-2">
          {coreReqs.map(renderReqItem)}
        </div>
      </div>

      {/* Advanced Requirements */}
      {advancedReqs.length > 0 && (
        <div className="space-y-2 pt-2 border-t border-slate-800/80">
          <div className="text-xs font-semibold uppercase tracking-wider text-purple-400 flex items-center gap-1.5">
            <Sparkles className="h-3.5 w-3.5" />
            <span>Phase 2: Scale, Concurrency & Advanced Strategies ({advancedReqs.length})</span>
          </div>
          <div className="space-y-2">
            {advancedReqs.map(renderReqItem)}
          </div>
        </div>
      )}
    </div>
  );
};
