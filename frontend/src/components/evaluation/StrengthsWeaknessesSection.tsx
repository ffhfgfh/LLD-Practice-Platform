import React from 'react';
import { Card } from '../common/Card';
import { CheckCircle2, AlertCircle, ArrowUpRight } from 'lucide-react';

interface StrengthsWeaknessesProps {
  strengths: string[];
  improvementAreas: string[];
}

export const StrengthsWeaknessesSection: React.FC<StrengthsWeaknessesProps> = ({
  strengths,
  improvementAreas,
}) => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* What You Did Well */}
      <Card className="border-emerald-500/20 bg-emerald-500/5">
        <div className="flex items-center gap-2 text-emerald-400 mb-4 pb-2 border-b border-emerald-500/15">
          <CheckCircle2 className="h-5 w-5" />
          <h3 className="font-bold text-base text-emerald-300">What You Did Well</h3>
        </div>

        {strengths.length === 0 ? (
          <p className="text-xs text-slate-500 italic">No specific strengths recorded.</p>
        ) : (
          <ul className="space-y-2.5">
            {strengths.map((str, idx) => (
              <li key={idx} className="text-sm text-slate-200 flex items-start gap-2.5">
                <span className="text-emerald-400 font-bold text-base leading-none mt-0.5">&check;</span>
                <span className="leading-relaxed">{str}</span>
              </li>
            ))}
          </ul>
        )}
      </Card>

      {/* What Could Be Improved */}
      <Card className="border-amber-500/20 bg-amber-500/5">
        <div className="flex items-center gap-2 text-amber-400 mb-4 pb-2 border-b border-amber-500/15">
          <AlertCircle className="h-5 w-5" />
          <h3 className="font-bold text-base text-amber-300">Areas for Growth & Refactoring</h3>
        </div>

        {improvementAreas.length === 0 ? (
          <p className="text-xs text-slate-500 italic">No major improvement areas recorded.</p>
        ) : (
          <ul className="space-y-2.5">
            {improvementAreas.map((imp, idx) => (
              <li key={idx} className="text-sm text-slate-200 flex items-start gap-2.5">
                <span className="text-amber-400 font-bold text-base leading-none mt-0.5">&bull;</span>
                <span className="leading-relaxed">{imp}</span>
              </li>
            ))}
          </ul>
        )}
      </Card>
    </div>
  );
};
