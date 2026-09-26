import React, { useEffect, useRef, useState } from 'react';
import mermaid from 'mermaid';
import { ClassDesign } from '../../types';
import { Button } from '../common/Button';
import { Sparkles, RefreshCw, AlertTriangle, Layers, Code2, Copy, Check } from 'lucide-react';

interface MermaidViewerProps {
  diagramCode: string;
  onChange: (code: string) => void;
  classes?: ClassDesign[];
}

export const isMeaningfulMermaid = (code?: string): boolean => {
  if (!code || typeof code !== 'string') return false;
  const lines = code
    .split('\n')
    .map((l) => l.trim())
    .filter((l) => l.length > 0 && !l.startsWith('%%'));

  if (lines.length === 0) return false;

  // Filter out standalone diagram headers
  const nonHeaderLines = lines.filter((l) => {
    const lower = l.toLowerCase();
    return (
      !lower.startsWith('classdiagram') &&
      !lower.startsWith('graph') &&
      !lower.startsWith('flowchart') &&
      !lower.startsWith('sequencediagram') &&
      !lower.startsWith('statediagram')
    );
  });

  return nonHeaderLines.length > 0;
};

export const MermaidViewer: React.FC<MermaidViewerProps> = ({ diagramCode, onChange, classes = [] }) => {
  const [svgContent, setSvgContent] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const [activeView, setActiveView] = useState<'both' | 'diagram' | 'code'>('both');
  const [copied, setCopied] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    mermaid.initialize({
      startOnLoad: false,
      theme: 'dark',
      suppressErrorRendering: true,
      themeVariables: {
        darkMode: true,
        background: '#0f172a',
        primaryColor: '#6366f1',
        primaryTextColor: '#f8fafc',
        primaryBorderColor: '#4f46e5',
        lineColor: '#94a3b8',
        secondaryColor: '#1e293b',
        tertiaryColor: '#0f172a',
      },
      securityLevel: 'loose',
    });
  }, []);

  useEffect(() => {
    let isMounted = true;
    const renderDiagram = async () => {
      if (!isMeaningfulMermaid(diagramCode)) {
        if (isMounted) {
          setSvgContent('');
          setError(null);
        }
        return;
      }

      const id = `mermaid-svg-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`;
      try {
        const { svg } = await mermaid.render(id, diagramCode.trim());
        if (isMounted) {
          setSvgContent(svg);
          setError(null);
        }
      } catch (err: any) {
        // Remove stray error nodes generated in document body by mermaid
        const strayDiv = document.querySelector(`[id^="dmermaid-svg-"]`) || document.getElementById(id);
        if (strayDiv && strayDiv.parentNode) {
          strayDiv.parentNode.removeChild(strayDiv);
        }
        if (isMounted) {
          setError(err?.message || 'Mermaid syntax error. Please verify your diagram syntax.');
        }
      }
    };

    const timer = setTimeout(renderDiagram, 250);
    return () => {
      isMounted = false;
      clearTimeout(timer);
    };
  }, [diagramCode]);

  const generateFromClasses = () => {
    if (!classes || classes.length === 0) {
      alert('Add at least one class in the Class Architecture editor above to generate a diagram.');
      return;
    }

    let code = 'classDiagram\n';

    const sanitizeType = (typeStr: string): string => {
      if (!typeStr) return 'void';
      return typeStr.replace(/</g, '~').replace(/>/g, '~').replace(/\s+/g, '');
    };

    const sanitizeName = (nameStr: string): string => {
      return (nameStr || '').replace(/[^a-zA-Z0-9_]/g, '');
    };

    // 1. Declare Classes & Interfaces
    classes.forEach((c) => {
      const safeName = sanitizeName(c.name);
      if (!safeName) return;

      if (c.is_interface) {
        code += `    class ${safeName} {\n        <<interface>>\n`;
      } else if (c.is_abstract) {
        code += `    class ${safeName} {\n        <<abstract>>\n`;
      } else {
        code += `    class ${safeName} {\n`;
      }

      (c.attributes || []).forEach((a) => {
        const vis = a.visibility === 'public' ? '+' : a.visibility === 'protected' ? '#' : '-';
        const cleanType = sanitizeType(a.type || 'String');
        const cleanName = sanitizeName(a.name);
        if (cleanName) {
          code += `        ${vis}${cleanType} ${cleanName}\n`;
        }
      });

      (c.methods || []).forEach((m) => {
        const vis = m.visibility === 'public' ? '+' : m.visibility === 'protected' ? '#' : '-';
        const cleanName = sanitizeName(m.name);
        const cleanReturn = sanitizeType(m.returnType || 'void');
        const cleanParams = (m.params || '')
          .replace(/</g, '~')
          .replace(/>/g, '~')
          .replace(/[;\n\r]/g, ' ')
          .trim();
        if (cleanName) {
          code += `        ${vis}${cleanName}(${cleanParams}) ${cleanReturn}\n`;
        }
      });

      code += `    }\n`;
    });

    // 2. Declare Implementations
    classes.forEach((c) => {
      const safeName = sanitizeName(c.name);
      if (!safeName) return;
      if (c.interfaces_implemented && c.interfaces_implemented.length > 0) {
        c.interfaces_implemented.forEach((iface) => {
          const safeIface = sanitizeName(iface);
          if (safeIface && safeIface !== safeName) {
            code += `    ${safeIface} <|.. ${safeName} : implements\n`;
          }
        });
      }
    });

    // 3. Declare Relationships
    classes.forEach((c) => {
      const safeSource = sanitizeName(c.name);
      if (!safeSource) return;
      (c.relationships || []).forEach((rel) => {
        const safeTarget = sanitizeName(rel.target);
        if (!safeTarget || safeTarget === safeSource) return;

        let arrow = '-->';
        if (rel.type === 'COMPOSITION') arrow = '*--';
        else if (rel.type === 'AGGREGATION') arrow = 'o--';
        else if (rel.type === 'INHERITANCE') arrow = '--|>';
        else if (rel.type === 'IMPLEMENTATION') arrow = '..|>';

        const mult = rel.multiplicity ? ` "${rel.multiplicity.replace(/"/g, '')}" ` : ' ';
        code += `    ${safeSource} ${arrow}${mult}${safeTarget}\n`;
      });
    });

    onChange(code);
    setError(null);
  };

  const handleCopyCode = () => {
    navigator.clipboard.writeText(diagramCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-3">
      {/* Controls Bar */}
      <div className="flex items-center justify-between flex-wrap gap-2 pb-2 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-300 flex items-center gap-1.5">
            <Layers className="h-4 w-4 text-indigo-400" />
            Mermaid Class Diagram
          </span>
          <div className="flex rounded-lg bg-slate-950 border border-slate-800 p-0.5 text-xs">
            <button
              onClick={() => setActiveView('both')}
              className={`px-2.5 py-1 rounded transition-colors cursor-pointer ${
                activeView === 'both' ? 'bg-indigo-600 text-white font-medium' : 'text-slate-400 hover:text-white'
              }`}
            >
              Split
            </button>
            <button
              onClick={() => setActiveView('diagram')}
              className={`px-2.5 py-1 rounded transition-colors cursor-pointer ${
                activeView === 'diagram' ? 'bg-indigo-600 text-white font-medium' : 'text-slate-400 hover:text-white'
              }`}
            >
              Diagram
            </button>
            <button
              onClick={() => setActiveView('code')}
              className={`px-2.5 py-1 rounded transition-colors cursor-pointer ${
                activeView === 'code' ? 'bg-indigo-600 text-white font-medium' : 'text-slate-400 hover:text-white'
              }`}
            >
              Code
            </button>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {diagramCode && (
            <button
              onClick={handleCopyCode}
              className="inline-flex items-center gap-1 px-2.5 py-1 text-xs rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200 transition-colors"
              title="Copy Mermaid Code"
            >
              {copied ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
              <span>{copied ? 'Copied' : 'Copy'}</span>
            </button>
          )}

          <Button
            variant="outline"
            size="sm"
            onClick={generateFromClasses}
            leftIcon={<Sparkles className="h-3.5 w-3.5 text-amber-400" />}
            className="text-xs"
          >
            Sync from Classes ({classes.length})
          </Button>
        </div>
      </div>

      {/* Main Grid */}
      <div className={`grid gap-4 ${activeView === 'both' ? 'grid-cols-1 lg:grid-cols-2' : 'grid-cols-1'}`}>
        {/* Editor Area */}
        {(activeView === 'both' || activeView === 'code') && (
          <div className="flex flex-col">
            <div className="flex items-center justify-between text-xs text-slate-400 mb-1.5 font-mono">
              <span className="flex items-center gap-1">
                <Code2 className="h-3.5 w-3.5 text-indigo-400" />
                diagram.mmd
              </span>
              <span className="text-[11px] text-slate-500">Mermaid classDiagram syntax</span>
            </div>
            <textarea
              rows={14}
              value={diagramCode}
              onChange={(e) => onChange(e.target.value)}
              placeholder={`classDiagram\n    class ParkingLot {\n        -List~ParkingSpot~ spots\n        +parkVehicle(Vehicle v) Ticket\n    }\n    ParkingLot *-- ParkingSpot`}
              className="w-full h-80 p-3.5 rounded-xl bg-slate-950 border border-slate-800 text-indigo-300 font-mono text-xs leading-relaxed focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none placeholder-slate-600"
              spellCheck={false}
            />
          </div>
        )}

        {/* Diagram Visual Preview */}
        {(activeView === 'both' || activeView === 'diagram') && (
          <div className="flex flex-col">
            <div className="flex items-center justify-between text-xs text-slate-400 mb-1.5">
              <span>Live Visual Preview</span>
              {error ? (
                <span className="text-rose-400 flex items-center gap-1 font-mono text-[11px]">
                  <AlertTriangle className="h-3.5 w-3.5" /> Syntax Error
                </span>
              ) : svgContent ? (
                <span className="text-emerald-400 text-xs font-mono flex items-center gap-1">
                  &bull; Valid UML SVG
                </span>
              ) : null}
            </div>

            <div
              ref={containerRef}
              className="w-full h-80 rounded-xl bg-slate-950 border border-slate-800 p-4 flex items-center justify-center overflow-auto"
            >
              {error ? (
                <div className="text-center p-4 space-y-3 max-w-md">
                  <div className="inline-flex p-2.5 rounded-xl bg-rose-500/10 text-rose-400 border border-rose-500/20">
                    <AlertTriangle className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="text-xs font-semibold text-rose-300">Mermaid Syntax Warning</p>
                    <p className="text-slate-400 font-mono text-[11px] mt-1 bg-slate-900/80 p-2.5 rounded-lg border border-slate-800 text-left overflow-x-auto max-h-24">
                      {error}
                    </p>
                  </div>
                  {classes.length > 0 && (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={generateFromClasses}
                      leftIcon={<RefreshCw className="h-3.5 w-3.5 text-indigo-400" />}
                      className="text-xs"
                    >
                      Regenerate from Classes ({classes.length})
                    </Button>
                  )}
                </div>
              ) : svgContent ? (
                <div
                  className="w-full h-full flex items-center justify-center [&>svg]:max-w-full [&>svg]:max-h-full"
                  dangerouslySetInnerHTML={{ __html: svgContent }}
                />
              ) : (
                <div className="text-center p-4 space-y-3 max-w-sm">
                  <div className="inline-flex p-3 rounded-2xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                    <Layers className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="text-xs font-semibold text-slate-300">No Diagram Defined Yet</p>
                    <p className="text-[11px] text-slate-500 mt-1">
                      {classes.length > 0
                        ? `You have ${classes.length} class${classes.length > 1 ? 'es' : ''} defined. Click below to generate your UML class diagram.`
                        : 'Define classes in the Class Architecture tab or write Mermaid syntax in the editor.'}
                    </p>
                  </div>
                  {classes.length > 0 && (
                    <Button
                      variant="primary"
                      size="sm"
                      onClick={generateFromClasses}
                      leftIcon={<Sparkles className="h-3.5 w-3.5 text-amber-300" />}
                      className="text-xs"
                    >
                      Generate from {classes.length} Classes
                    </Button>
                  )}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
