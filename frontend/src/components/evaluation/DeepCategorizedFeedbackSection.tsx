import React from 'react';
import { Card } from '../common/Card';
import {
  AlertTriangle,
  FileQuestion,
  ShieldAlert,
  GitFork,
  Zap,
  Cpu,
  Workflow,
  CheckCircle2,
  Lightbulb,
} from 'lucide-react';

interface DeepCategorizedFeedbackProps {
  designIssues?: string[];
  missingRequirements?: string[];
  solidViolations?: string[];
  couplingConcerns?: string[];
  extensibilitySuggestions?: string[];
  edgeCasesAnalysis?: string[];
  refactoringPlan?: string[];
}

export const DeepCategorizedFeedbackSection: React.FC<DeepCategorizedFeedbackProps> = ({
  designIssues = [],
  missingRequirements = [],
  solidViolations = [],
  couplingConcerns = [],
  extensibilitySuggestions = [],
  edgeCasesAnalysis = [],
  refactoringPlan = [],
}) => {
  return (
    <div className="space-y-6">
      {/* Recommended Step-by-Step Refactoring Plan */}
      {refactoringPlan && refactoringPlan.length > 0 && (
        <Card className="border-indigo-500/30 bg-gradient-to-r from-indigo-950/40 via-slate-900 to-slate-900/90 shadow-xl">
          <div className="flex items-center gap-2 text-indigo-400 mb-3 pb-2 border-b border-indigo-500/20">
            <Workflow className="h-5 w-5" />
            <h3 className="font-bold text-base text-indigo-300">
              Recommended Step-by-Step Refactoring Plan
            </h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {refactoringPlan.map((step, idx) => (
              <div
                key={idx}
                className="p-3.5 rounded-xl border border-indigo-500/20 bg-indigo-500/5 flex items-start gap-3"
              >
                <div className="h-6 w-6 rounded-full bg-indigo-500/20 text-indigo-300 flex items-center justify-center shrink-0 text-xs font-bold font-mono mt-0.5">
                  {idx + 1}
                </div>
                <p className="text-xs sm:text-sm text-slate-200 leading-relaxed font-medium">
                  {step}
                </p>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Grid of Specialized Design Analyses */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {/* SOLID Principles */}
        <Card className="border-slate-800 bg-slate-900/50 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 text-amber-400 mb-2.5 pb-2 border-b border-slate-800">
              <ShieldAlert className="h-4 w-4" />
              <h4 className="text-sm font-bold text-slate-200">SOLID Principles Analysis</h4>
            </div>
            {solidViolations.length === 0 ? (
              <p className="text-xs text-emerald-400 flex items-center gap-1.5 py-2 font-medium">
                <CheckCircle2 className="h-4 w-4" /> No major SOLID violations detected.
              </p>
            ) : (
              <ul className="space-y-2 text-xs text-slate-300">
                {solidViolations.map((v, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <span className="text-amber-500 font-bold">&bull;</span>
                    <span>{v}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </Card>

        {/* Missing Requirements */}
        <Card className="border-slate-800 bg-slate-900/50 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 text-rose-400 mb-2.5 pb-2 border-b border-slate-800">
              <FileQuestion className="h-4 w-4" />
              <h4 className="text-sm font-bold text-slate-200">Missing Requirements Coverage</h4>
            </div>
            {missingRequirements.length === 0 ? (
              <p className="text-xs text-emerald-400 flex items-center gap-1.5 py-2 font-medium">
                <CheckCircle2 className="h-4 w-4" /> All stated requirements mapped to classes.
              </p>
            ) : (
              <ul className="space-y-2 text-xs text-slate-300">
                {missingRequirements.map((m, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <span className="text-rose-500 font-bold">&bull;</span>
                    <span>{m}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </Card>

        {/* Coupling & Cohesion */}
        <Card className="border-slate-800 bg-slate-900/50 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 text-sky-400 mb-2.5 pb-2 border-b border-slate-800">
              <GitFork className="h-4 w-4" />
              <h4 className="text-sm font-bold text-slate-200">Coupling & Cohesion</h4>
            </div>
            {couplingConcerns.length === 0 ? (
              <p className="text-xs text-emerald-400 flex items-center gap-1.5 py-2 font-medium">
                <CheckCircle2 className="h-4 w-4" /> High cohesion and clean relationship graph.
              </p>
            ) : (
              <ul className="space-y-2 text-xs text-slate-300">
                {couplingConcerns.map((c, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <span className="text-sky-400 font-bold">&bull;</span>
                    <span>{c}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </Card>

        {/* Extensibility Critique */}
        <Card className="border-slate-800 bg-slate-900/50 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 text-purple-400 mb-2.5 pb-2 border-b border-slate-800">
              <Zap className="h-4 w-4" />
              <h4 className="text-sm font-bold text-slate-200">Extensibility & Pluggability</h4>
            </div>
            {extensibilitySuggestions.length === 0 ? (
              <p className="text-xs text-emerald-400 flex items-center gap-1.5 py-2 font-medium">
                <CheckCircle2 className="h-4 w-4" /> Highly extensible via interfaces & patterns.
              </p>
            ) : (
              <ul className="space-y-2 text-xs text-slate-300">
                {extensibilitySuggestions.map((e, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <span className="text-purple-400 font-bold">&bull;</span>
                    <span>{e}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </Card>

        {/* Edge Cases & Concurrency */}
        <Card className="border-slate-800 bg-slate-900/50 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 text-emerald-400 mb-2.5 pb-2 border-b border-slate-800">
              <Cpu className="h-4 w-4" />
              <h4 className="text-sm font-bold text-slate-200">Concurrency & Failure Modes</h4>
            </div>
            {edgeCasesAnalysis.length === 0 ? (
              <p className="text-xs text-slate-400 py-2">
                Concurrency and error handling noted.
              </p>
            ) : (
              <ul className="space-y-2 text-xs text-slate-300">
                {edgeCasesAnalysis.map((ec, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <span className="text-emerald-400 font-bold">&bull;</span>
                    <span>{ec}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </Card>

        {/* Design Issues & Smells */}
        <Card className="border-slate-800 bg-slate-900/50 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 text-amber-400 mb-2.5 pb-2 border-b border-slate-800">
              <AlertTriangle className="h-4 w-4" />
              <h4 className="text-sm font-bold text-slate-200">Architectural Code Smells</h4>
            </div>
            {designIssues.length === 0 ? (
              <p className="text-xs text-emerald-400 flex items-center gap-1.5 py-2 font-medium">
                <CheckCircle2 className="h-4 w-4" /> Zero God classes or design smells detected.
              </p>
            ) : (
              <ul className="space-y-2 text-xs text-slate-300">
                {designIssues.map((issue, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <span className="text-amber-500 font-bold">&bull;</span>
                    <span>{issue}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
};
