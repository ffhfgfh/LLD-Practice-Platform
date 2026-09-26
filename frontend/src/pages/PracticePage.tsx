import React, { useEffect, useState, useRef, useCallback } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { api } from '../services/api';
import { PracticeAttempt, ClassDesign, Solution } from '../types';
import { Button } from '../components/common/Button';
import { Card } from '../components/common/Card';
import { Badge } from '../components/common/Badge';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorAlert } from '../components/common/ErrorAlert';
import { ClassCard } from '../components/practice/ClassCard';
import { ClassEditorModal } from '../components/practice/ClassEditorModal';
import { MermaidViewer } from '../components/practice/MermaidViewer';
import { ArchitectureEditor } from '../components/practice/ArchitectureEditor';
import { ValidationModal } from '../components/practice/ValidationModal';
import { GuidedTourBanner } from '../components/practice/GuidedTourBanner';
import { EvaluationProgressModal } from '../components/practice/EvaluationProgressModal';
import { RequirementsList } from '../components/problems/RequirementsList';
import { ConstraintsSection, DesignConsiderationsSection, HintsSection } from '../components/problems/ProblemDetailsSections';
import {
  Save,
  Send,
  Plus,
  Layers,
  Code2,
  FileText,
  BookOpen,
  PanelLeftClose,
  PanelLeftOpen,
  CheckCircle,
  RotateCcw,
  Sparkles,
  ShieldCheck,
  AlertCircle,
  ExternalLink,
  Clock,
  RotateCw,
} from 'lucide-react';

export const PracticePage: React.FC = () => {
  const { attemptId } = useParams<{ attemptId: string }>();
  const navigate = useNavigate();

  const [attempt, setAttempt] = useState<PracticeAttempt | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Studio State
  const [activeTab, setActiveTab] = useState<'classes' | 'diagram' | 'architecture'>('classes');
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [selectedEvaluator, setSelectedEvaluator] = useState<string>('composite');

  // Solution Editable State
  const [classes, setClasses] = useState<ClassDesign[]>([]);
  const [summary, setSummary] = useState('');
  const [assumptions, setAssumptions] = useState('');
  const [designPatterns, setDesignPatterns] = useState<string[]>([]);
  const [mermaidDiagram, setMermaidDiagram] = useState('');

  // Modals & States
  const [isClassModalOpen, setIsClassModalOpen] = useState(false);
  const [editingClassIndex, setEditingClassIndex] = useState<number | null>(null);
  const [validationErrors, setValidationErrors] = useState<string[]>([]);
  const [isValidationModalOpen, setIsValidationModalOpen] = useState(false);

  // Requirements checklist tracker
  const [checkedReqs, setCheckedReqs] = useState<string[]>([]);

  // Saving / Autosave / Recovery States
  const [isSaving, setIsSaving] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [lastSavedTime, setLastSavedTime] = useState<string | null>(null);
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const [recoveryAvailable, setRecoveryAvailable] = useState(false);
  const autosaveTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Fetch Attempt
  const fetchAttempt = async () => {
    if (!attemptId) return;
    try {
      setLoading(true);
      setError(null);
      const data = await api.getAttempt(attemptId);
      setAttempt(data);

      if (data.solution) {
        setClasses(data.solution.classes || []);
        setSummary(data.solution.summary || '');
        setAssumptions(data.solution.assumptions_and_tradeoffs || '');
        setDesignPatterns(data.solution.design_patterns_used || []);
        setMermaidDiagram(data.solution.mermaid_diagram || '');
      }
      setLastSavedTime(data.last_saved_at);
      setHasUnsavedChanges(false);

      // Check local recovery storage
      const cached = localStorage.getItem(`lld_recovery_${attemptId}`);
      if (cached && data.is_mutable) {
        try {
          const parsed = JSON.parse(cached);
          if (parsed.timestamp > new Date(data.last_saved_at).getTime()) {
            setRecoveryAvailable(true);
          }
        } catch (e) {}
      }
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || 'Failed to load practice attempt.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAttempt();
  }, [attemptId]);

  // Mark changes & trigger debounced autosave
  const markChanged = useCallback(() => {
    if (!hasUnsavedChanges) setHasUnsavedChanges(true);

    // Save to local recovery cache
    if (attemptId) {
      localStorage.setItem(`lld_recovery_${attemptId}`, JSON.stringify({
        timestamp: Date.now(),
        classes,
        summary,
        assumptions,
        designPatterns,
        mermaidDiagram,
      }));
    }

    // Debounced autosave to server
    if (autosaveTimerRef.current) clearTimeout(autosaveTimerRef.current);
    autosaveTimerRef.current = setTimeout(() => {
      handleSaveDraft(true);
    }, 4000);
  }, [hasUnsavedChanges, attemptId, classes, summary, assumptions, designPatterns, mermaidDiagram]);

  const restoreFromRecovery = () => {
    if (!attemptId) return;
    const cached = localStorage.getItem(`lld_recovery_${attemptId}`);
    if (cached) {
      try {
        const parsed = JSON.parse(cached);
        if (parsed.classes) setClasses(parsed.classes);
        if (parsed.summary) setSummary(parsed.summary);
        if (parsed.assumptions) setAssumptions(parsed.assumptions);
        if (parsed.designPatterns) setDesignPatterns(parsed.designPatterns);
        if (parsed.mermaidDiagram) setMermaidDiagram(parsed.mermaidDiagram);
        setRecoveryAvailable(false);
        setHasUnsavedChanges(true);
        alert('Draft recovered from local backup.');
      } catch (e) {}
    }
  };

  // Class Actions
  const handleSaveClass = (classDesign: ClassDesign) => {
    markChanged();
    if (editingClassIndex !== null) {
      const updated = [...classes];
      updated[editingClassIndex] = classDesign;
      setClasses(updated);
    } else {
      setClasses([...classes, classDesign]);
    }
    setEditingClassIndex(null);
  };

  const handleEditClass = (index: number) => {
    setEditingClassIndex(index);
    setIsClassModalOpen(true);
  };

  const handleDeleteClass = (index: number) => {
    markChanged();
    setClasses(classes.filter((_, i) => i !== index));
  };

  // Requirement Checklist Toggle
  const handleToggleReq = (code: string) => {
    if (checkedReqs.includes(code)) {
      setCheckedReqs(checkedReqs.filter((c) => c !== code));
    } else {
      setCheckedReqs([...checkedReqs, code]);
    }
  };

  // Save Draft
  const handleSaveDraft = async (silent = false) => {
    if (!attemptId || !attempt?.is_mutable) return;
    try {
      setIsSaving(true);
      const updated = await api.saveDraft(attemptId, {
        summary,
        assumptions_and_tradeoffs: assumptions,
        design_patterns_used: designPatterns,
        mermaid_diagram: mermaidDiagram,
        classes,
      });
      setAttempt(updated);
      setLastSavedTime(updated.last_saved_at);
      setHasUnsavedChanges(false);
      localStorage.removeItem(`lld_recovery_${attemptId}`);
      setRecoveryAvailable(false);
    } catch (err: any) {
      if (!silent) {
        alert('Failed to save draft: ' + (err?.response?.data?.detail || err?.message));
      }
    } finally {
      setIsSaving(false);
    }
  };

  // Submit Solution
  const handleSubmit = async () => {
    if (!attemptId) return;

    // Client-side validation check
    const errors: string[] = [];
    if (classes.length === 0) {
      errors.push('At least one class or interface entity must be defined.');
    }
    const emptyNameClasses = classes.filter((c) => !c.name.trim());
    if (emptyNameClasses.length > 0) {
      errors.push('All classes must have a valid class name.');
    }
    const emptyRespClasses = classes.filter((c) => c.responsibility.trim().length < 8);
    if (emptyRespClasses.length > 0) {
      const names = emptyRespClasses.map((c) => c.name || 'Unnamed');
      errors.push(`Classes (${names.join(', ')}) must have a clearly stated Single Responsibility (min 8 characters).`);
    }
    if (!summary.trim() || summary.trim().length < 20) {
      errors.push('Please provide a solution summary (minimum 20 characters) explaining the architecture data flow.');
    }

    if (errors.length > 0) {
      setValidationErrors(errors);
      setIsValidationModalOpen(true);
      return;
    }

    try {
      setIsSubmitting(true);
      // Save current state first
      await api.saveDraft(attemptId, {
        summary,
        assumptions_and_tradeoffs: assumptions,
        design_patterns_used: designPatterns,
        mermaid_diagram: mermaidDiagram,
        classes,
      });

      // Submit and evaluate
      const evaluatedAttempt = await api.submitAttempt(attemptId, selectedEvaluator);
      localStorage.removeItem(`lld_recovery_${attemptId}`);
      navigate(`/attempts/${evaluatedAttempt.id}/feedback`);
    } catch (err: any) {
      const backendErrors = err?.response?.data?.validation_errors;
      if (backendErrors && Array.isArray(backendErrors)) {
        setValidationErrors(backendErrors);
        setIsValidationModalOpen(true);
      } else {
        alert('Submission failed: ' + (err?.response?.data?.detail || err?.message));
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) return <LoadingSpinner message="Initializing practice workspace..." />;
  if (error) return <ErrorAlert message={error} onRetry={fetchAttempt} />;
  if (!attempt) return null;

  const totalReqCount = attempt.problem.requirements.length;
  const progressPercent = Math.round((checkedReqs.length / Math.max(1, totalReqCount)) * 100);

  return (
    <div className="space-y-4">
      {/* Draft Recovery Alert */}
      {recoveryAvailable && attempt.is_mutable && (
        <div className="rounded-xl border border-amber-500/30 bg-amber-500/10 p-3.5 flex items-center justify-between gap-3 text-xs sm:text-sm">
          <div className="flex items-center gap-2 text-amber-300">
            <AlertCircle className="h-4 w-4 shrink-0 text-amber-400" />
            <span>Unsaved local changes detected from a previous browser session.</span>
          </div>
          <div className="flex items-center gap-2">
            <Button size="sm" variant="primary" onClick={restoreFromRecovery}>
              Restore Backup
            </Button>
            <Button size="sm" variant="ghost" onClick={() => setRecoveryAvailable(false)}>
              Discard
            </Button>
          </div>
        </div>
      )}

      {/* Immutable Attempt Notification */}
      {!attempt.is_mutable && (
        <div className="rounded-xl border border-indigo-500/30 bg-indigo-500/10 p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <CheckCircle className="h-5 w-5 text-emerald-400 shrink-0" />
            <div className="text-xs sm:text-sm text-slate-200">
              <span className="font-bold text-white">This attempt is submitted and immutable. </span>
              Your past architecture is preserved for historical progression review.
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Link to={`/attempts/${attempt.id}/feedback`}>
              <Button size="sm" variant="success" leftIcon={<ExternalLink className="h-3.5 w-3.5" />}>
                View Evaluation
              </Button>
            </Link>
            <Button
              size="sm"
              variant="primary"
              leftIcon={<RotateCcw className="h-3.5 w-3.5" />}
              onClick={async () => {
                const newAtt = await api.createAttempt(attempt.problem.id);
                navigate(`/practice/${newAtt.id}`);
              }}
            >
              Try Again (New Attempt)
            </Button>
          </div>
        </div>
      )}

      {/* Guided Tour Best Practice Guide */}
      <GuidedTourBanner />

      {/* Top Workspace Header */}
      <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
        <div className="flex items-center gap-3">
          <button
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="text-slate-400 hover:text-white p-1.5 rounded-lg hover:bg-slate-800 transition-colors cursor-pointer"
            title={isSidebarOpen ? 'Hide requirements panel' : 'Show requirements panel'}
          >
            {isSidebarOpen ? <PanelLeftClose className="h-5 w-5" /> : <PanelLeftOpen className="h-5 w-5" />}
          </button>

          <div>
            <div className="flex items-center gap-2 mb-0.5 flex-wrap">
              <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
                Attempt #{attempt.attempt_number}
              </span>
              <Badge variant="status" status={attempt.status} />
              <Badge variant="difficulty" difficulty={attempt.problem.difficulty} />
              <span className="text-xs text-slate-400 font-mono hidden sm:inline">
                ⏱️ ~{attempt.problem.estimated_time_minutes || 45}m target
              </span>
            </div>
            <h1 className="text-lg font-bold text-white tracking-tight">
              {attempt.problem.title}
            </h1>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-3 flex-wrap w-full lg:w-auto justify-end">
          {/* Saved Status Indicator */}
          <div className="text-[11px] text-slate-400 font-mono hidden sm:flex items-center gap-1.5">
            {isSaving ? (
              <span className="text-indigo-400 flex items-center gap-1">
                <RotateCw className="h-3 w-3 animate-spin" /> Autosaving...
              </span>
            ) : hasUnsavedChanges ? (
              <span className="text-amber-400 flex items-center gap-1">
                <span className="h-1.5 w-1.5 rounded-full bg-amber-400 animate-pulse" /> Unsaved changes
              </span>
            ) : lastSavedTime ? (
              <span className="text-emerald-400 flex items-center gap-1">
                <CheckCircle className="h-3 w-3" /> Saved at {new Date(lastSavedTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            ) : null}
          </div>

          {/* Evaluator Selector */}
          <div className="flex items-center gap-1.5 text-xs">
            <span className="text-slate-500 hidden xl:inline">Evaluator:</span>
            <select
              value={selectedEvaluator}
              onChange={(e) => setSelectedEvaluator(e.target.value)}
              disabled={!attempt.is_mutable}
              className="px-2.5 py-1.5 rounded-lg bg-slate-950 border border-slate-700 text-slate-200 text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500 disabled:opacity-50 font-mono"
            >
              <option value="composite">Composite (Deterministic + AI)</option>
              <option value="rule_based">Deterministic Rule-Based Only</option>
              <option value="deepseek">DeepSeek AI</option>
              <option value="openai">OpenAI GPT</option>
              <option value="gemini">Google Gemini AI</option>
            </select>
          </div>

          {/* Save Draft Button */}
          {attempt.is_mutable && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => handleSaveDraft(false)}
              isLoading={isSaving}
              leftIcon={<Save className="h-4 w-4" />}
            >
              Save Draft
            </Button>
          )}

          {/* Submit Button */}
          {attempt.is_mutable ? (
            <Button
              variant="primary"
              size="sm"
              onClick={handleSubmit}
              isLoading={isSubmitting}
              leftIcon={<Send className="h-4 w-4" />}
              className="font-bold shadow-indigo-500/25"
            >
              Submit & Evaluate
            </Button>
          ) : (
            <Link to={`/attempts/${attempt.id}/feedback`}>
              <Button variant="success" size="sm" leftIcon={<ExternalLink className="h-4 w-4" />}>
                View Evaluation
              </Button>
            </Link>
          )}
        </div>
      </div>

      {/* Main Workspace Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Drawer / Panel: Problem Requirements Reference & Checklist */}
        {isSidebarOpen && (
          <div className="lg:col-span-4 space-y-4 max-h-[82vh] overflow-y-auto pr-1">
            <Card className="space-y-4 border-slate-800">
              <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                <div>
                  <h3 className="text-sm font-bold text-white flex items-center gap-1.5">
                    <BookOpen className="h-4 w-4 text-indigo-400" />
                    Requirements Checklist
                  </h3>
                  <p className="text-[11px] text-slate-400 mt-0.5">
                    Click items to track completion as you design.
                  </p>
                </div>
                <span className="text-xs text-indigo-300 font-mono font-bold px-2 py-0.5 rounded bg-indigo-500/10 border border-indigo-500/20">
                  {checkedReqs.length}/{totalReqCount} ({progressPercent}%)
                </span>
              </div>

              {/* Progress Bar */}
              <div className="w-full h-1.5 rounded-full bg-slate-800 overflow-hidden">
                <div
                  className="h-full bg-emerald-500 transition-all duration-300"
                  style={{ width: `${progressPercent}%` }}
                />
              </div>

              {/* Interactive Requirements Checklist */}
              <RequirementsList
                requirements={attempt.problem.requirements}
                compact
                checkedReqs={checkedReqs}
                onToggleReq={handleToggleReq}
              />

              {/* Constraints */}
              <ConstraintsSection constraints={attempt.problem.constraints} />

              {/* Considerations */}
              <DesignConsiderationsSection considerations={attempt.problem.expected_design_considerations} />

              {/* Hints */}
              <HintsSection hints={attempt.problem.hints} />
            </Card>
          </div>
        )}

        {/* Right Studio Area: Tabs for Classes, Diagram, Architecture */}
        <div className={`${isSidebarOpen ? 'lg:col-span-8' : 'lg:col-span-12'} space-y-4`}>
          {/* Studio Navigation Tabs */}
          <div className="flex items-center justify-between border-b border-slate-800 pb-2">
            <div className="flex items-center gap-2">
              <button
                onClick={() => setActiveTab('classes')}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                  activeTab === 'classes'
                    ? 'bg-indigo-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-white hover:bg-slate-900'
                }`}
              >
                <Code2 className="h-4 w-4" />
                <span>Class Design Studio ({classes.length})</span>
              </button>

              <button
                onClick={() => setActiveTab('diagram')}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                  activeTab === 'diagram'
                    ? 'bg-indigo-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-white hover:bg-slate-900'
                }`}
              >
                <Layers className="h-4 w-4" />
                <span>Mermaid Diagram</span>
              </button>

              <button
                onClick={() => setActiveTab('architecture')}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                  activeTab === 'architecture'
                    ? 'bg-indigo-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-white hover:bg-slate-900'
                }`}
              >
                <FileText className="h-4 w-4" />
                <span>Architecture & Trade-offs</span>
              </button>
            </div>

            {activeTab === 'classes' && attempt.is_mutable && (
              <Button
                variant="primary"
                size="sm"
                onClick={() => {
                  setEditingClassIndex(null);
                  setIsClassModalOpen(true);
                }}
                leftIcon={<Plus className="h-4 w-4" />}
                className="text-xs font-bold"
              >
                Add Class
              </Button>
            )}
          </div>

          {/* TAB 1: Class Design Studio */}
          {activeTab === 'classes' && (
            <div className="space-y-4">
              {classes.length === 0 ? (
                <div className="text-center py-16 border-2 border-dashed border-slate-800 rounded-2xl bg-slate-900/30 p-8 space-y-3">
                  <div className="h-12 w-12 rounded-2xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center mx-auto border border-indigo-500/20">
                    <Code2 className="h-6 w-6" />
                  </div>
                  <h3 className="text-base font-bold text-white">No Classes Defined Yet</h3>
                  <p className="text-xs text-slate-400 max-w-md mx-auto leading-relaxed">
                    Identify domain entities from the requirements, assign single responsibilities, and create polymorphic interfaces for extensible algorithms.
                  </p>
                  {attempt.is_mutable && (
                    <Button
                      variant="primary"
                      size="sm"
                      onClick={() => {
                        setEditingClassIndex(null);
                        setIsClassModalOpen(true);
                      }}
                      leftIcon={<Plus className="h-4 w-4" />}
                    >
                      Add First Class / Entity
                    </Button>
                  )}
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {classes.map((cls, idx) => (
                    <ClassCard
                      key={idx}
                      classDesign={cls}
                      onEdit={() => handleEditClass(idx)}
                      onDelete={() => handleDeleteClass(idx)}
                    />
                  ))}
                </div>
              )}
            </div>
          )}

          {/* TAB 2: Mermaid Diagram */}
          {activeTab === 'diagram' && (
            <Card className="border-slate-800 bg-slate-900/60">
              <MermaidViewer
                diagramCode={mermaidDiagram}
                onChange={(code) => {
                  markChanged();
                  setMermaidDiagram(code);
                }}
                classes={classes}
              />
            </Card>
          )}

          {/* TAB 3: Architecture & Trade-offs */}
          {activeTab === 'architecture' && (
            <Card className="border-slate-800 bg-slate-900/60">
              <ArchitectureEditor
                summary={summary}
                onSummaryChange={(val) => {
                  markChanged();
                  setSummary(val);
                }}
                assumptions={assumptions}
                onAssumptionsChange={(val) => {
                  markChanged();
                  setAssumptions(val);
                }}
                designPatterns={designPatterns}
                onDesignPatternsChange={(patterns) => {
                  markChanged();
                  setDesignPatterns(patterns);
                }}
              />
            </Card>
          )}
        </div>
      </div>

      {/* Class Modal */}
      <ClassEditorModal
        isOpen={isClassModalOpen}
        onClose={() => {
          setIsClassModalOpen(false);
          setEditingClassIndex(null);
        }}
        onSave={handleSaveClass}
        initialData={editingClassIndex !== null ? classes[editingClassIndex] : null}
        existingClassNames={classes.map((c) => c.name)}
      />

      {/* Validation Errors Modal */}
      <ValidationModal
        isOpen={isValidationModalOpen}
        onClose={() => setIsValidationModalOpen(false)}
        errors={validationErrors}
      />

      {/* Evaluation Animated Progress Modal */}
      <EvaluationProgressModal
        isOpen={isSubmitting}
        evaluatorName={selectedEvaluator}
      />
    </div>
  );
};
