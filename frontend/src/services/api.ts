import axios from 'axios';
import {
  LLDProblemList,
  LLDProblemDetail,
  PracticeAttempt,
  Evaluation,
  ProblemWithHistory,
  DashboardData,
  Solution
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Dashboard
  getDashboard: async (): Promise<DashboardData> => {
    const res = await apiClient.get<DashboardData>('/dashboard/');
    return res.data;
  },

  // Problems
  getProblems: async (params?: { difficulty?: string; search?: string }): Promise<LLDProblemList[]> => {
    const res = await apiClient.get<LLDProblemList[]>('/problems/', { params });
    return res.data;
  },

  getProblem: async (idOrSlug: string): Promise<LLDProblemDetail> => {
    const res = await apiClient.get<LLDProblemDetail>(`/problems/${idOrSlug}/`);
    return res.data;
  },

  // Attempts
  createAttempt: async (problemId: string): Promise<PracticeAttempt> => {
    const res = await apiClient.post<PracticeAttempt>('/attempts/', { problem_id: problemId });
    return res.data;
  },

  getAttempt: async (attemptId: string): Promise<PracticeAttempt> => {
    const res = await apiClient.get<PracticeAttempt>(`/attempts/${attemptId}/`);
    return res.data;
  },

  saveDraft: async (attemptId: string, solution: Partial<Solution>): Promise<PracticeAttempt> => {
    const res = await apiClient.put<PracticeAttempt>(`/attempts/${attemptId}/`, {
      solution,
    });
    return res.data;
  },

  submitAttempt: async (attemptId: string, evaluatorType?: string): Promise<PracticeAttempt> => {
    const res = await apiClient.post<PracticeAttempt>(`/attempts/${attemptId}/submit/`, {
      evaluator_type: evaluatorType,
    });
    return res.data;
  },

  retryEvaluation: async (attemptId: string, evaluatorType?: string): Promise<PracticeAttempt> => {
    const res = await apiClient.post<PracticeAttempt>(`/attempts/${attemptId}/evaluate/`, {
      evaluator_type: evaluatorType,
    });
    return res.data;
  },

  // Evaluations
  getEvaluation: async (evaluationId: string): Promise<Evaluation> => {
    const res = await apiClient.get<Evaluation>(`/evaluations/${evaluationId}/`);
    return res.data;
  },

  // History
  getHistory: async (): Promise<ProblemWithHistory[]> => {
    const res = await apiClient.get<ProblemWithHistory[]>('/history/');
    return res.data;
  },
};
