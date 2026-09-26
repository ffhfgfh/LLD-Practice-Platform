import React from 'react';
import { Solution } from '../../types';
import { X, Code2, Layers, Split, FileText } from 'lucide-react';
import { Button } from '../common/Button';

interface SubmissionSnapshotModalProps {
  isOpen: boolean;
  onClose: () => void;
  solution?: Solution;
  problemTitle: string;
}

export const SubmissionSnapshotModal: React.FC<SubmissionSnapshotModalProps> = ({
  isOpen,
  onClose,
  solution,
  problemTitle,
}) => {
  if (!isOpen || !solution) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 overflow-y-auto">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/60">
          <div>
            <span className="text-xs font-mono text-indigo-400 font-semibold uppercase">Submitted Solution Snapshot</span>
            <h3 className="text-lg font-bold text-white">{problemTitle}</h3>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto space-y-6 flex-1 text-sm text-slate-300">
          {/* Summary */}
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5 flex items-center gap-1.5">
              <FileText className="h-4 w-4 text-indigo-400" />
              Solution Architecture Summary
            </h4>
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 text-slate-200 leading-relaxed whitespace-pre-line text-xs sm:text-sm font-sans">
              {solution.summary || 'No summary provided.'}
            </div>
          </div>

          {/* Design Patterns & Assumptions */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5 flex items-center gap-1.5">
                <Layers className="h-4 w-4 text-indigo-400" />
                Declared Design Patterns
              </h4>
              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 flex flex-wrap gap-1.5">
                {solution.design_patterns_used && solution.design_patterns_used.length > 0 ? (
                  solution.design_patterns_used.map((p) => (
                    <span key={p} className="px-2.5 py-1 rounded bg-indigo-500/15 text-indigo-300 border border-indigo-500/30 text-xs font-mono">
                      {p}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-slate-500 italic">None declared</span>
                )}
              </div>
            </div>

            <div>
              <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5 flex items-center gap-1.5">
                <Split className="h-4 w-4 text-amber-400" />
                Assumptions & Trade-offs
              </h4>
              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 text-xs text-slate-300 leading-relaxed whitespace-pre-line max-h-32 overflow-y-auto">
                {solution.assumptions_and_tradeoffs || 'No assumptions documented.'}
              </div>
            </div>
          </div>

          {/* Submitted Classes */}
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
              <Code2 className="h-4 w-4 text-indigo-400" />
              Submitted Classes & Entities ({solution.classes ? solution.classes.length : 0})
            </h4>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {solution.classes && solution.classes.map((c, i) => (
                <div key={i} className="bg-slate-950 p-3.5 rounded-xl border border-slate-800 text-xs space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-white font-mono">{c.name}</span>
                    <span className="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">
                      {c.is_interface ? 'interface' : c.is_abstract ? 'abstract' : 'class'}
                    </span>
                  </div>
                  <p className="text-slate-400 italic">{c.responsibility}</p>
                  {c.methods && c.methods.length > 0 && (
                    <div className="font-mono text-[11px] text-slate-300 border-t border-slate-850 pt-1">
                      {c.methods.map((m, j) => (
                        <div key={j} className="truncate">
                          + {m.name}({m.params}): {m.returnType}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Mermaid Diagram Code */}
          {solution.mermaid_diagram && (
            <div>
              <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
                Mermaid Diagram Source
              </h4>
              <pre className="bg-slate-950 p-4 rounded-xl border border-slate-800 text-indigo-300 font-mono text-xs overflow-x-auto">
                {solution.mermaid_diagram}
              </pre>
            </div>
          )}
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
