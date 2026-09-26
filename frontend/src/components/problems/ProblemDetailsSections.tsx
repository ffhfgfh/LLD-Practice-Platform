import React, { useState } from 'react';
import { Card } from '../common/Card';
import { ShieldAlert, Lightbulb, ChevronDown, ChevronUp, Compass } from 'lucide-react';

interface ConstraintsSectionProps {
  constraints: string[];
}

export const ConstraintsSection: React.FC<ConstraintsSectionProps> = ({ constraints }) => {
  if (!constraints || constraints.length === 0) return null;

  return (
    <Card className="border-amber-500/20 bg-amber-500/5">
      <div className="flex items-center gap-2 text-amber-400 mb-3">
        <ShieldAlert className="h-4 w-4" />
        <h4 className="text-sm font-semibold uppercase tracking-wider">System Constraints & Scale</h4>
      </div>
      <ul className="space-y-2">
        {constraints.map((c, i) => (
          <li key={i} className="text-sm text-slate-300 flex items-start gap-2">
            <span className="text-amber-500/70 font-mono text-xs mt-0.5">&bull;</span>
            <span>{c}</span>
          </li>
        ))}
      </ul>
    </Card>
  );
};

interface DesignConsiderationsSectionProps {
  considerations: string[];
}

export const DesignConsiderationsSection: React.FC<DesignConsiderationsSectionProps> = ({ considerations }) => {
  if (!considerations || considerations.length === 0) return null;

  return (
    <Card className="border-indigo-500/20 bg-indigo-500/5">
      <div className="flex items-center gap-2 text-indigo-400 mb-3">
        <Compass className="h-4 w-4" />
        <h4 className="text-sm font-semibold uppercase tracking-wider">Expected Design Considerations</h4>
      </div>
      <ul className="space-y-2">
        {considerations.map((c, i) => (
          <li key={i} className="text-sm text-slate-300 flex items-start gap-2">
            <span className="text-indigo-400 font-mono text-xs mt-0.5">&bull;</span>
            <span>{c}</span>
          </li>
        ))}
      </ul>
    </Card>
  );
};

interface HintsSectionProps {
  hints: string[];
}

export const HintsSection: React.FC<HintsSectionProps> = ({ hints }) => {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  if (!hints || hints.length === 0) return null;

  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2 text-slate-400 text-sm font-semibold mb-2">
        <Lightbulb className="h-4 w-4 text-amber-400" />
        <span>Progressive Hints ({hints.length})</span>
      </div>
      {hints.map((hint, idx) => {
        const isOpen = openIndex === idx;
        return (
          <div
            key={idx}
            className="rounded-lg border border-slate-800 bg-slate-900/50 overflow-hidden"
          >
            <button
              onClick={() => setOpenIndex(isOpen ? null : idx)}
              className="w-full px-4 py-2.5 flex items-center justify-between text-left text-sm font-medium text-slate-300 hover:text-white hover:bg-slate-800/50 transition-colors"
            >
              <span>Hint #{idx + 1}</span>
              {isOpen ? <ChevronUp className="h-4 w-4 text-slate-400" /> : <ChevronDown className="h-4 w-4 text-slate-400" />}
            </button>
            {isOpen && (
              <div className="px-4 py-3 border-t border-slate-800/80 text-sm text-amber-200/90 bg-amber-500/5 leading-relaxed">
                {hint}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};
