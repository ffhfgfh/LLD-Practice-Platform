import React from 'react';
import { Card } from '../common/Card';
import { Layers, FileText, Split, Check } from 'lucide-react';

interface ArchitectureEditorProps {
  summary: string;
  onSummaryChange: (val: string) => void;
  assumptions: string;
  onAssumptionsChange: (val: string) => void;
  designPatterns: string[];
  onDesignPatternsChange: (patterns: string[]) => void;
}

const AVAILABLE_PATTERNS = [
  'Strategy',
  'Factory / Abstract Factory',
  'State',
  'Observer / Pub-Sub',
  'Singleton',
  'Command',
  'Facade',
  'Adapter',
  'Decorator',
  'Template Method',
  'Composite',
  'Builder',
];

export const ArchitectureEditor: React.FC<ArchitectureEditorProps> = ({
  summary,
  onSummaryChange,
  assumptions,
  onAssumptionsChange,
  designPatterns,
  onDesignPatternsChange,
}) => {
  const togglePattern = (pat: string) => {
    if (designPatterns.includes(pat)) {
      onDesignPatternsChange(designPatterns.filter((p) => p !== pat));
    } else {
      onDesignPatternsChange([...designPatterns, pat]);
    }
  };

  return (
    <div className="space-y-6">
      {/* Design Patterns Pill Selector */}
      <div>
        <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2 flex items-center gap-1.5">
          <Layers className="h-4 w-4 text-indigo-400" />
          Design Patterns Applied ({designPatterns.length} selected)
        </label>
        <div className="flex flex-wrap gap-2">
          {AVAILABLE_PATTERNS.map((pattern) => {
            const isSelected = designPatterns.includes(pattern);
            return (
              <button
                key={pattern}
                type="button"
                onClick={() => togglePattern(pattern)}
                className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium border transition-all cursor-pointer ${
                  isSelected
                    ? 'bg-indigo-600 text-white border-indigo-500 shadow-sm shadow-indigo-500/20'
                    : 'bg-slate-900/80 text-slate-400 border-slate-800 hover:text-slate-200 hover:border-slate-700'
                }`}
              >
                {isSelected && <Check className="h-3.5 w-3.5 text-white" />}
                <span>{pattern}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* High-Level Architecture Explanation */}
      <div>
        <div className="flex items-center justify-between mb-1.5">
          <label className="text-xs font-semibold uppercase tracking-wider text-slate-300 flex items-center gap-1.5">
            <FileText className="h-4 w-4 text-indigo-400" />
            Solution Summary & Request Lifecycle Flow <span className="text-rose-400">*</span>
          </label>
          <span className="text-[11px] text-slate-500">
            {summary.length} characters
          </span>
        </div>
        <textarea
          rows={5}
          value={summary}
          onChange={(e) => onSummaryChange(e.target.value)}
          placeholder="Walk through how the classes collaborate during major use cases (e.g. When a vehicle enters Gate 1, EntryGate requests SpotAssignmentService to find a spot using NearestSpotStrategy, generates a Ticket, and marks Spot as OCCUPIED...)"
          className="w-full p-3.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 placeholder-slate-500 text-sm leading-relaxed focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
      </div>

      {/* Assumptions and Design Trade-offs */}
      <div>
        <div className="flex items-center justify-between mb-1.5">
          <label className="text-xs font-semibold uppercase tracking-wider text-slate-300 flex items-center gap-1.5">
            <Split className="h-4 w-4 text-amber-400" />
            Assumptions, Constraints & Architectural Trade-offs
          </label>
          <span className="text-[11px] text-slate-500">
            {assumptions.length} characters
          </span>
        </div>
        <textarea
          rows={4}
          value={assumptions}
          onChange={(e) => onAssumptionsChange(e.target.value)}
          placeholder="Document key assumptions and trade-offs (e.g. In-memory locking vs distributed redis lock for concurrency; Trade-off: Chosen Strategy pattern increases class count but provides OCP extensibility for future pricing formulas...)"
          className="w-full p-3.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 placeholder-slate-500 text-sm leading-relaxed focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
      </div>
    </div>
  );
};
