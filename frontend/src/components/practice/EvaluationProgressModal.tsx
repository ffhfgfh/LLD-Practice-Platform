import React, { useEffect, useState } from 'react';
import { Cpu, CheckCircle2, Loader2, Sparkles, ShieldCheck, Layers, GitFork } from 'lucide-react';

interface EvaluationProgressModalProps {
  isOpen: boolean;
  evaluatorName: string;
}

const TIPS = [
  'In LLD interviews, separating responsibilities into focused classes matters more than writing full method algorithms.',
  'Applying the Open/Closed Principle via Strategy or Factory patterns allows your system to scale with new requirements.',
  'Deterministic static rules analyze your class coupling and inheritance hierarchies with 100% confidence.',
  'AI reasoning reviews your assumptions, concurrency considerations, and edge cases to provide interview-grade feedback.',
];

export const EvaluationProgressModal: React.FC<EvaluationProgressModalProps> = ({
  isOpen,
  evaluatorName,
}) => {
  const [activeStep, setActiveStep] = useState(0);
  const [tipIndex, setTipIndex] = useState(0);

  useEffect(() => {
    if (!isOpen) {
      setActiveStep(0);
      return;
    }

    const stepTimers = [
      setTimeout(() => setActiveStep(1), 800),
      setTimeout(() => setActiveStep(2), 2200),
      setTimeout(() => setActiveStep(3), 4200),
    ];

    const tipTimer = setInterval(() => {
      setTipIndex((prev) => (prev + 1) % TIPS.length);
    }, 3500);

    return () => {
      stepTimers.forEach(clearTimeout);
      clearInterval(tipTimer);
    };
  }, [isOpen]);

  if (!isOpen) return null;

  const steps = [
    { label: 'Domain Validation & Completeness Checks', icon: ShieldCheck },
    { label: '8-Pass Deterministic Rule Static Analysis', icon: Layers },
    { label: 'AI Semantic Reasoning & SOLID Violation Detection', icon: Sparkles },
    { label: 'Synthesizing 9 Category Scores & Refactoring Plan', icon: GitFork },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-md p-4 animate-fade-in">
      <div className="bg-slate-900 border border-slate-700/80 rounded-3xl w-full max-w-lg p-6 sm:p-8 shadow-2xl space-y-6 text-center">
        {/* Animated Icon */}
        <div className="relative inline-flex items-center justify-center">
          <div className="absolute inset-0 rounded-full bg-indigo-500/20 blur-xl animate-pulse" />
          <div className="relative h-16 w-16 rounded-2xl bg-gradient-to-tr from-indigo-600 to-indigo-400 p-0.5 shadow-lg shadow-indigo-500/30 flex items-center justify-center">
            <Cpu className="h-8 w-8 text-white animate-bounce" />
          </div>
        </div>

        {/* Title */}
        <div className="space-y-1">
          <h3 className="text-xl font-bold text-white tracking-tight">
            Evaluating Your Architecture
          </h3>
          <p className="text-xs text-slate-400">
            Running evaluation engine: <span className="text-indigo-300 font-mono font-semibold capitalize">{evaluatorName}</span>
          </p>
        </div>

        {/* Evaluation Step Timeline */}
        <div className="space-y-3 text-left bg-slate-950/70 p-4 rounded-2xl border border-slate-800">
          {steps.map((step, idx) => {
            const isCompleted = activeStep > idx;
            const isCurrent = activeStep === idx;
            const Icon = step.icon;

            return (
              <div
                key={idx}
                className={`flex items-center gap-3 text-xs transition-all duration-300 ${
                  isCompleted
                    ? 'text-emerald-400 font-medium'
                    : isCurrent
                    ? 'text-indigo-300 font-semibold'
                    : 'text-slate-500 opacity-60'
                }`}
              >
                <div className="shrink-0">
                  {isCompleted ? (
                    <CheckCircle2 className="h-4 w-4 text-emerald-400" />
                  ) : isCurrent ? (
                    <Loader2 className="h-4 w-4 text-indigo-400 animate-spin" />
                  ) : (
                    <Icon className="h-4 w-4 text-slate-600" />
                  )}
                </div>
                <span className="flex-1">{step.label}</span>
              </div>
            );
          })}
        </div>

        {/* Dynamic Learning Tip */}
        <div className="bg-indigo-500/10 border border-indigo-500/20 rounded-xl p-3.5 text-xs text-slate-300 transition-all">
          <div className="flex items-center justify-center gap-1.5 text-indigo-400 font-semibold text-[11px] uppercase tracking-wider mb-1">
            <Sparkles className="h-3.5 w-3.5" />
            Interview Tip
          </div>
          <p className="italic text-slate-300 leading-relaxed text-[11px]">
            &ldquo;{TIPS[tipIndex]}&rdquo;
          </p>
        </div>
      </div>
    </div>
  );
};
