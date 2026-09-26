import React from 'react';
import { AlertTriangle, X, CheckCircle2 } from 'lucide-react';
import { Button } from '../common/Button';

interface ValidationModalProps {
  isOpen: boolean;
  onClose: () => void;
  errors: string[];
}

export const ValidationModal: React.FC<ValidationModalProps> = ({ isOpen, onClose, errors }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 backdrop-blur-sm p-4">
      <div className="bg-slate-900 border border-rose-500/30 rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 bg-rose-500/10 flex items-center justify-between">
          <div className="flex items-center gap-2 text-rose-400">
            <AlertTriangle className="h-5 w-5" />
            <h3 className="text-base font-bold">Submission Requirements Missing</h3>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-4">
          <p className="text-sm text-slate-300">
            Please resolve the following required items before submitting your Low-Level Design for evaluation:
          </p>

          <ul className="space-y-2 bg-slate-950/60 p-4 rounded-xl border border-slate-800">
            {errors.map((err, idx) => (
              <li key={idx} className="flex items-start gap-2 text-sm text-rose-300">
                <span className="text-rose-500 font-bold">&bull;</span>
                <span>{err}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-slate-800 bg-slate-950/50 flex justify-end">
          <Button variant="primary" onClick={onClose}>
            Back to Editor
          </Button>
        </div>
      </div>
    </div>
  );
};
