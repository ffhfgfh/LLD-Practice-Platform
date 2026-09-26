import React, { useState } from 'react';
import { FeedbackItem, FeedbackSource, FeedbackSeverity } from '../../types';
import { Card } from '../common/Card';
import { Badge } from '../common/Badge';
import { Tag, Lightbulb, MessageSquare, HelpCircle, GraduationCap } from 'lucide-react';

interface FeedbackItemsListProps {
  items: FeedbackItem[];
}

export const FeedbackItemsList: React.FC<FeedbackItemsListProps> = ({ items }) => {
  const [sourceFilter, setSourceFilter] = useState<string>('ALL');
  const [severityFilter, setSeverityFilter] = useState<string>('ALL');

  if (!items || items.length === 0) {
    return (
      <Card>
        <p className="text-sm text-slate-500 italic text-center py-4">No detailed feedback items available.</p>
      </Card>
    );
  }

  const filteredItems = items.filter((item) => {
    if (sourceFilter !== 'ALL' && item.source !== sourceFilter) return false;
    if (severityFilter !== 'ALL' && item.severity !== severityFilter) return false;
    return true;
  });

  return (
    <div className="space-y-4">
      {/* Header and Filter Controls */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pb-2 border-b border-slate-800">
        <div>
          <h3 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
            <MessageSquare className="h-4 w-4 text-indigo-400" />
            Detailed Findings & Suggestions ({filteredItems.length}/{items.length})
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Clear distinction between deterministic structural checks and qualitative AI suggestions.
          </p>
        </div>

        <div className="flex items-center gap-2 flex-wrap text-xs">
          {/* Source Filter */}
          <select
            value={sourceFilter}
            onChange={(e) => setSourceFilter(e.target.value)}
            className="px-2.5 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-slate-200 text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500 font-mono"
          >
            <option value="ALL">All Sources</option>
            <option value="DETERMINISTIC">Deterministic Verification (100%)</option>
            <option value="AI_SUGGESTION">AI Qualitative Reasoning</option>
          </select>

          {/* Severity Filter */}
          <select
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}
            className="px-2.5 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-slate-200 text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500 font-mono"
          >
            <option value="ALL">All Severities</option>
            <option value="CRITICAL">Critical</option>
            <option value="WARNING">Warnings</option>
            <option value="POSITIVE">Positive</option>
            <option value="INFO">Info</option>
          </select>
        </div>
      </div>

      {/* Items List */}
      {filteredItems.length === 0 ? (
        <Card className="text-center py-8">
          <p className="text-sm text-slate-500">No items match the selected filter criteria.</p>
        </Card>
      ) : (
        <div className="space-y-3">
          {filteredItems.map((item, idx) => (
            <Card
              key={idx}
              className={`border-l-4 ${
                item.severity === 'POSITIVE'
                  ? 'border-l-emerald-500'
                  : item.severity === 'WARNING'
                  ? 'border-l-amber-500'
                  : item.severity === 'CRITICAL'
                  ? 'border-l-rose-500'
                  : 'border-l-sky-500'
              } bg-slate-900/40 space-y-2`}
            >
              <div className="flex items-start justify-between gap-2 flex-wrap">
                <div className="flex items-center gap-2 flex-wrap">
                  <Badge variant="severity" severity={item.severity} />
                  <Badge variant="source" source={item.source} />
                  {item.confidence && (
                    <Badge variant="confidence" confidence={item.confidence} />
                  )}
                  <span className="text-[11px] font-mono text-slate-400 uppercase">
                    {item.category.replace(/_/g, ' ')}
                  </span>
                </div>

                {item.target_entity && (
                  <span className="inline-flex items-center gap-1 text-[11px] font-mono px-2 py-0.5 rounded bg-slate-800 text-indigo-300 border border-slate-700">
                    <Tag className="h-3 w-3 text-indigo-400" />
                    Target: {item.target_entity}
                  </span>
                )}
              </div>

              <h4 className="text-sm font-bold text-white">
                {item.title}
              </h4>

              <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                {item.message}
              </p>

              {/* Actionable Concrete Suggestion */}
              {item.suggestion && (
                <div className="p-2.5 rounded-lg bg-indigo-950/30 border border-indigo-500/20 text-xs text-indigo-200 flex items-start gap-2">
                  <Lightbulb className="h-4 w-4 text-amber-400 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-semibold text-indigo-300">Concrete Suggestion: </span>
                    {item.suggestion}
                  </div>
                </div>
              )}

              {/* Why It Matters Context */}
              {item.why_it_matters && (
                <div className="p-2.5 rounded-lg bg-slate-950/60 border border-slate-800 text-[11px] text-slate-400 flex items-start gap-2">
                  <GraduationCap className="h-3.5 w-3.5 text-slate-400 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-semibold text-slate-300">Why this matters in an interview: </span>
                    {item.why_it_matters}
                  </div>
                </div>
              )}
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
