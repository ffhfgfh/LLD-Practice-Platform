import React, { useState } from 'react';
import { Lightbulb, X, Compass, CheckCircle, Sparkles, Layers } from 'lucide-react';

export const GuidedTourBanner: React.FC = () => {
  const [isDismissed, setIsDismissed] = useState(() => {
    return localStorage.getItem('lld_tour_dismissed') === 'true';
  });

  if (isDismissed) return null;

  const handleDismiss = () => {
    localStorage.setItem('lld_tour_dismissed', 'true');
    setIsDismissed(true);
  };

  return (
    <div className="rounded-2xl border border-indigo-500/30 bg-gradient-to-r from-indigo-950/60 via-slate-900 to-slate-900/90 p-4 sm:p-5 relative shadow-lg">
      <button
        onClick={handleDismiss}
        className="absolute top-3 right-3 text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition-colors"
        title="Dismiss guide"
      >
        <X className="h-4 w-4" />
      </button>

      <div className="flex items-start gap-3.5 pr-6">
        <div className="h-9 w-9 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center shrink-0 border border-indigo-500/30">
          <Compass className="h-5 w-5" />
        </div>

        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <h4 className="text-sm font-bold text-white tracking-tight">
              Low-Level Design Best Practice Workflow
            </h4>
            <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-bold">
              Pro Tip
            </span>
          </div>

          <p className="text-xs text-slate-300 leading-relaxed">
            In Staff/Senior LLD interviews, start by identifying <strong>Core Domain Nouns</strong> (Classes) from requirements,
            assign each class a <strong>Single Reason to Change (SRP)</strong>, define <strong>Polymorphic Interfaces</strong> for variable algorithms (e.g. Allocation/Pricing Strategies), and document trade-offs.
          </p>

          <div className="flex items-center gap-4 text-[11px] text-slate-400 pt-1 flex-wrap">
            <span className="flex items-center gap-1 text-indigo-300 font-medium">
              <CheckCircle className="h-3 w-3 text-emerald-400" /> 1. Model Entities
            </span>
            <span>&rarr;</span>
            <span className="flex items-center gap-1 text-indigo-300 font-medium">
              <CheckCircle className="h-3 w-3 text-emerald-400" /> 2. Define SRP & Interfaces
            </span>
            <span>&rarr;</span>
            <span className="flex items-center gap-1 text-indigo-300 font-medium">
              <CheckCircle className="h-3 w-3 text-emerald-400" /> 3. Sync Diagram
            </span>
            <span>&rarr;</span>
            <span className="flex items-center gap-1 text-indigo-300 font-medium">
              <CheckCircle className="h-3 w-3 text-emerald-400" /> 4. Explain Flow & Concurrency
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
