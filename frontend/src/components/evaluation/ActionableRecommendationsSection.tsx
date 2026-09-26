import React from 'react';
import { Card } from '../common/Card';
import { Compass, Lightbulb, ArrowRight } from 'lucide-react';

interface ActionableRecommendationsProps {
  recommendations: string[];
}

export const ActionableRecommendationsSection: React.FC<ActionableRecommendationsProps> = ({
  recommendations,
}) => {
  if (!recommendations || recommendations.length === 0) return null;

  return (
    <Card className="border-indigo-500/30 bg-gradient-to-br from-indigo-950/40 via-slate-900 to-slate-900">
      <div className="flex items-center gap-2 text-indigo-400 mb-4 pb-2 border-b border-indigo-500/20">
        <Compass className="h-5 w-5" />
        <h3 className="font-bold text-base text-indigo-300">
          Actionable Next Steps & Concrete Recommendations
        </h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {recommendations.map((rec, idx) => (
          <div
            key={idx}
            className="rounded-xl border border-indigo-500/20 bg-indigo-500/5 p-3.5 flex items-start gap-3"
          >
            <div className="h-6 w-6 rounded-full bg-indigo-500/20 text-indigo-300 flex items-center justify-center shrink-0 text-xs font-bold font-mono mt-0.5">
              {idx + 1}
            </div>
            <p className="text-xs sm:text-sm text-slate-200 leading-relaxed">
              {rec}
            </p>
          </div>
        ))}
      </div>
    </Card>
  );
};
