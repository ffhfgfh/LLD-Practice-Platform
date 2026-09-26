import React from 'react';
import { Layers, ShieldCheck, Sparkles } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-slate-800/80 bg-slate-950 py-8 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2 text-slate-400 text-sm">
          <Layers className="h-4 w-4 text-indigo-400" />
          <span>LLD Practice Platform &copy; 2026</span>
        </div>
        <div className="flex items-center gap-4 text-xs text-slate-500">
          <span className="flex items-center gap-1 text-slate-400">
            <ShieldCheck className="h-3.5 w-3.5 text-emerald-400" /> Deterministic Verification
          </span>
          <span className="flex items-center gap-1 text-slate-400">
            <Sparkles className="h-3.5 w-3.5 text-indigo-400" /> AI-Assisted Reasoning
          </span>
        </div>
      </div>
    </footer>
  );
};
