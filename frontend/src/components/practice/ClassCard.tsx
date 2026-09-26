import React from 'react';
import { ClassDesign } from '../../types';
import { Edit2, Trash2, Code2, Link2, CheckSquare } from 'lucide-react';

interface ClassCardProps {
  classDesign: ClassDesign;
  onEdit: () => void;
  onDelete: () => void;
}

export const ClassCard: React.FC<ClassCardProps> = ({ classDesign, onEdit, onDelete }) => {
  const getBadgeType = () => {
    if (classDesign.is_interface) return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
    if (classDesign.is_abstract) return 'bg-amber-500/10 text-amber-400 border-amber-500/20';
    return 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20';
  };

  const getTypeLabel = () => {
    if (classDesign.is_interface) return '«interface»';
    if (classDesign.is_abstract) return '«abstract»';
    return 'class';
  };

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4 hover:border-slate-700 transition-all flex flex-col justify-between">
      <div>
        <div className="flex items-start justify-between gap-2">
          <div className="flex items-center gap-2 flex-wrap">
            <span className={`text-[10px] uppercase font-mono px-2 py-0.5 rounded border ${getBadgeType()}`}>
              {getTypeLabel()}
            </span>
            <h4 className="font-bold text-white font-mono text-base">{classDesign.name}</h4>
          </div>

          <div className="flex items-center gap-1">
            <button
              onClick={onEdit}
              className="text-slate-400 hover:text-indigo-400 p-1 rounded hover:bg-slate-800 transition-colors"
              title="Edit class"
            >
              <Edit2 className="h-3.5 w-3.5" />
            </button>
            <button
              onClick={onDelete}
              className="text-slate-400 hover:text-rose-400 p-1 rounded hover:bg-slate-800 transition-colors"
              title="Delete class"
            >
              <Trash2 className="h-3.5 w-3.5" />
            </button>
          </div>
        </div>

        {/* Responsibility */}
        <p className="text-xs text-slate-300 mt-2 italic bg-slate-950/50 p-2 rounded border border-slate-800/80">
          <span className="font-semibold text-slate-400 not-italic">Responsibility: </span>
          {classDesign.responsibility || 'No responsibility specified.'}
        </p>

        {/* Implements */}
        {classDesign.interfaces_implemented && classDesign.interfaces_implemented.length > 0 && (
          <div className="mt-2.5 flex items-center gap-1 flex-wrap">
            <span className="text-[11px] text-slate-500 flex items-center gap-1">
              <CheckSquare className="h-3 w-3 text-emerald-400" /> Implements:
            </span>
            {classDesign.interfaces_implemented.map((iface) => (
              <span key={iface} className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
                {iface}
              </span>
            ))}
          </div>
        )}

        {/* Attributes Preview */}
        {classDesign.attributes && classDesign.attributes.length > 0 && (
          <div className="mt-3 border-t border-slate-800/60 pt-2 font-mono text-xs text-slate-400 space-y-0.5">
            <div className="text-[10px] uppercase font-sans font-semibold text-slate-500 tracking-wider">
              Attributes ({classDesign.attributes.length})
            </div>
            {classDesign.attributes.slice(0, 4).map((a, i) => (
              <div key={i} className="truncate text-slate-300">
                <span className="text-indigo-400">{a.visibility === 'public' ? '+' : a.visibility === 'protected' ? '#' : '-'}</span>{' '}
                <span className="text-slate-200">{a.name}</span>: <span className="text-slate-400">{a.type}</span>
              </div>
            ))}
            {classDesign.attributes.length > 4 && (
              <div className="text-[10px] text-slate-500 italic">+ {classDesign.attributes.length - 4} more attributes</div>
            )}
          </div>
        )}

        {/* Methods Preview */}
        {classDesign.methods && classDesign.methods.length > 0 && (
          <div className="mt-3 border-t border-slate-800/60 pt-2 font-mono text-xs text-slate-400 space-y-0.5">
            <div className="text-[10px] uppercase font-sans font-semibold text-slate-500 tracking-wider">
              Methods ({classDesign.methods.length})
            </div>
            {classDesign.methods.slice(0, 4).map((m, i) => (
              <div key={i} className="truncate text-slate-300">
                <span className="text-emerald-400">{m.visibility === 'public' ? '+' : m.visibility === 'protected' ? '#' : '-'}</span>{' '}
                <span className="text-slate-100 font-semibold">{m.name}</span>({m.params}): <span className="text-slate-400">{m.returnType}</span>
              </div>
            ))}
            {classDesign.methods.length > 4 && (
              <div className="text-[10px] text-slate-500 italic">+ {classDesign.methods.length - 4} more methods</div>
            )}
          </div>
        )}

        {/* Relationships Preview */}
        {classDesign.relationships && classDesign.relationships.length > 0 && (
          <div className="mt-3 border-t border-slate-800/60 pt-2 text-xs space-y-1">
            <div className="text-[10px] uppercase font-sans font-semibold text-slate-500 tracking-wider flex items-center gap-1">
              <Link2 className="h-3 w-3" /> Relationships ({classDesign.relationships.length})
            </div>
            {classDesign.relationships.map((rel, i) => (
              <div key={i} className="flex items-center gap-1 text-[11px] font-mono text-slate-400 truncate">
                <span className="text-slate-500">&bull;</span>
                <span className="text-indigo-400">{rel.type}</span>
                <span className="text-slate-300"> &rarr; {rel.target}</span>
                {rel.multiplicity && <span className="text-slate-500">[{rel.multiplicity}]</span>}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
