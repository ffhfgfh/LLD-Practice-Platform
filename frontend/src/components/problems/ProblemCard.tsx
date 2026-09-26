import React from 'react';
import { Link } from 'react-router-dom';
import { LLDProblemList } from '../../types';
import { Card } from '../common/Card';
import { Badge } from '../common/Badge';
import { ArrowRight, Layers, Clock, Tag } from 'lucide-react';

interface ProblemCardProps {
  problem: LLDProblemList;
  onStartPractice?: (problemId: string) => void;
  isStarting?: boolean;
}

export const ProblemCard: React.FC<ProblemCardProps> = ({ problem, onStartPractice, isStarting = false }) => {
  return (
    <Card hoverEffect className="flex flex-col justify-between h-full group border-slate-800 bg-slate-900/60">
      <div>
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-center gap-2 flex-wrap">
            <Badge variant="difficulty" difficulty={problem.difficulty} />
            {problem.latest_score !== null && (
              <Badge variant="score" score={problem.latest_score} />
            )}
            <span className="inline-flex items-center gap-1 text-[11px] font-mono text-slate-400 px-2 py-0.5 rounded-full bg-slate-800 border border-slate-700">
              <Clock className="h-3 w-3 text-indigo-400" />
              ~{problem.estimated_time_minutes || 45} mins
            </span>
          </div>

          <span className="text-xs text-slate-500 font-mono shrink-0">
            {problem.requirements_count} reqs
          </span>
        </div>

        <Link to={`/problems/${problem.slug}`} className="block mt-3">
          <h3 className="text-lg font-bold text-white group-hover:text-indigo-400 transition-colors">
            {problem.title}
          </h3>
        </Link>

        <p className="text-sm text-slate-400 mt-2 line-clamp-2 leading-relaxed">
          {problem.summary}
        </p>

        {/* Tags */}
        {problem.tags && problem.tags.length > 0 && (
          <div className="mt-3 flex items-center gap-1.5 flex-wrap">
            {problem.tags.slice(0, 3).map((tag, i) => (
              <Badge key={i} variant="tag">
                {tag}
              </Badge>
            ))}
            {problem.tags.length > 3 && (
              <span className="text-[10px] text-slate-500">+{problem.tags.length - 3}</span>
            )}
          </div>
        )}
      </div>

      <div className="mt-5 pt-4 border-t border-slate-800/80 flex items-center justify-between">
        <div className="flex items-center gap-1.5 text-xs text-slate-500">
          <Layers className="h-3.5 w-3.5 text-slate-400" />
          <span>{problem.attempts_count} {problem.attempts_count === 1 ? 'attempt' : 'attempts'}</span>
        </div>

        <div className="flex items-center gap-2">
          <Link
            to={`/problems/${problem.slug}`}
            className="inline-flex items-center gap-1 text-xs font-semibold text-slate-300 hover:text-white px-2.5 py-1.5 rounded-md hover:bg-slate-800 transition-colors"
          >
            Specs
          </Link>

          {onStartPractice ? (
            <button
              onClick={() => onStartPractice(problem.id)}
              disabled={isStarting}
              className="inline-flex items-center gap-1 text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white px-3.5 py-1.5 rounded-md shadow-sm transition-all hover:shadow-indigo-500/20 cursor-pointer disabled:opacity-50"
            >
              <span>Practice</span>
              <ArrowRight className="h-3.5 w-3.5" />
            </button>
          ) : (
            <Link
              to={`/problems/${problem.slug}`}
              className="inline-flex items-center gap-1 text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white px-3.5 py-1.5 rounded-md shadow-sm transition-all hover:shadow-indigo-500/20"
            >
              <span>Practice</span>
              <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          )}
        </div>
      </div>
    </Card>
  );
};
