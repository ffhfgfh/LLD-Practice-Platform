export type Difficulty = 'EASY' | 'MEDIUM' | 'HARD';

export type AttemptStatus = 'DRAFT' | 'SUBMITTED' | 'EVALUATING' | 'COMPLETED' | 'FAILED';

export type FeedbackSeverity = 'POSITIVE' | 'INFO' | 'WARNING' | 'CRITICAL';

export type FeedbackSource = 'DETERMINISTIC' | 'AI_SUGGESTION' | 'HYBRID';

export type ConfidenceLevel = 'HIGH' | 'MEDIUM' | 'LOW';

export type EvaluationCategory =
  | 'requirements_coverage'
  | 'responsibility_assignment'
  | 'abstraction_and_interfaces'
  | 'solid_principles'
  | 'coupling_and_cohesion'
  | 'extensibility'
  | 'design_patterns'
  | 'edge_cases'
  | 'overall_explanation'
  | 'refactoring_plan';

export interface ProblemRequirement {
  id: string;
  req_code: string;
  title: string;
  description: string;
  category: string;
  keywords: string[];
  is_advanced?: boolean;
  order: number;
}

export interface LLDProblemList {
  id: string;
  slug: string;
  title: string;
  difficulty: Difficulty;
  estimated_time_minutes: number;
  tags: string[];
  summary: string;
  requirements_count: number;
  attempts_count: number;
  latest_score: number | null;
  latest_attempt_id: string | null;
  created_at: string;
}

export interface LLDProblemDetail {
  id: string;
  slug: string;
  title: string;
  difficulty: Difficulty;
  estimated_time_minutes: number;
  tags: string[];
  summary: string;
  problem_statement: string;
  constraints: string[];
  expected_design_considerations: string[];
  hints: string[];
  requirements: ProblemRequirement[];
  attempts_count: number;
  latest_attempt_id: string | null;
  created_at: string;
}

export interface ClassAttribute {
  name: string;
  type: string;
  visibility: 'public' | 'private' | 'protected';
}

export interface ClassMethod {
  name: string;
  returnType: string;
  params: string;
  visibility: 'public' | 'private' | 'protected';
}

export interface ClassRelationship {
  target: string;
  type: 'ASSOCIATION' | 'AGGREGATION' | 'COMPOSITION' | 'INHERITANCE' | 'IMPLEMENTATION';
  multiplicity: string;
  description?: string;
}

export interface ClassDesign {
  id?: string;
  name: string;
  responsibility: string;
  attributes: ClassAttribute[];
  methods: ClassMethod[];
  relationships: ClassRelationship[];
  interfaces_implemented: string[];
  is_interface: boolean;
  is_abstract: boolean;
  order?: number;
}

export interface Solution {
  id?: string;
  summary: string;
  assumptions_and_tradeoffs: string;
  design_patterns_used: string[];
  mermaid_diagram: string;
  classes: ClassDesign[];
  created_at?: string;
  updated_at?: string;
}

export interface FeedbackItem {
  id?: string;
  category: EvaluationCategory;
  source: FeedbackSource;
  confidence?: ConfidenceLevel;
  severity: FeedbackSeverity;
  title: string;
  message: string;
  target_entity?: string | null;
  suggestion?: string | null;
  why_it_matters?: string | null;
}

export interface CategoryScoreData {
  title: string;
  criterion?: string;
  score: number;
  max_score: number;
  evidence?: string;
  concern?: string;
  suggestion?: string;
  confidence?: ConfidenceLevel;
  rationale: string;
}

export interface Evaluation {
  id: string;
  evaluator_type: string;
  overall_score: number;
  overall_summary: string;
  strengths: string[];
  design_issues: string[];
  missing_requirements: string[];
  solid_violations: string[];
  coupling_concerns: string[];
  extensibility_suggestions: string[];
  edge_cases_analysis: string[];
  actionable_recommendations: string[];
  refactoring_plan: string[];
  improvement_areas: string[];
  category_scores: Record<string, CategoryScoreData>;
  feedback_items: FeedbackItem[];
  is_fallback: boolean;
  error_message?: string | null;
  evaluated_at: string;
}

export interface PracticeAttempt {
  id: string;
  problem: LLDProblemDetail;
  attempt_number: number;
  status: AttemptStatus;
  started_at: string;
  submitted_at: string | null;
  last_saved_at: string;
  solution: Solution;
  evaluation?: Evaluation | null;
  is_mutable: boolean;
}

export interface AttemptHistoryItem {
  id: string;
  attempt_number: number;
  status: AttemptStatus;
  started_at: string;
  submitted_at: string | null;
  overall_score: number | null;
  evaluator_type: string | null;
  class_count: number;
  solution_summary?: string;
}

export interface ProblemWithHistory {
  id: string;
  slug: string;
  title: string;
  difficulty: Difficulty;
  estimated_time_minutes: number;
  tags: string[];
  summary: string;
  total_attempts: number;
  best_score: number | null;
  latest_attempt: AttemptHistoryItem | null;
  attempts: AttemptHistoryItem[];
}

export interface DashboardStats {
  total_problems: number;
  problems_practiced: number;
  total_attempts: number;
  completed_evaluations: number;
  average_score: number;
}

export interface DashboardRecentAttempt {
  id: string;
  problem_id: string;
  problem_title: string;
  problem_difficulty: Difficulty;
  attempt_number: number;
  status: AttemptStatus;
  overall_score: number | null;
  started_at: string;
  submitted_at: string | null;
}

export interface DashboardData {
  stats: DashboardStats;
  recent_attempts: DashboardRecentAttempt[];
  recommended_problems: LLDProblemList[];
}
