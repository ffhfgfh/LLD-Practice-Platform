import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { LLDProblemList, Difficulty } from '../types';
import { ProblemCard } from '../components/problems/ProblemCard';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorAlert } from '../components/common/ErrorAlert';
import { Search, Filter, BookOpen, Layers } from 'lucide-react';

export const ProblemListPage: React.FC = () => {
  const [problems, setProblems] = useState<LLDProblemList[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('ALL');
  const [startingProblemId, setStartingProblemId] = useState<string | null>(null);
  const navigate = useNavigate();

  const fetchProblems = async () => {
    try {
      setLoading(true);
      setError(null);
      const params: any = {};
      if (selectedDifficulty !== 'ALL') params.difficulty = selectedDifficulty;
      if (searchQuery.trim()) params.search = searchQuery.trim();

      const data = await api.getProblems(params);
      setProblems(data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || 'Failed to load problems.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProblems();
  }, [selectedDifficulty]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchProblems();
  };

  const handleStartPractice = async (problemId: string) => {
    try {
      setStartingProblemId(problemId);
      const attempt = await api.createAttempt(problemId);
      navigate(`/practice/${attempt.id}`);
    } catch (err: any) {
      alert('Failed to start attempt: ' + (err?.response?.data?.detail || err?.message));
    } finally {
      setStartingProblemId(null);
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 text-indigo-400 text-xs font-semibold uppercase tracking-wider mb-1">
          <BookOpen className="h-4 w-4" />
          <span>LLD Problem Catalog</span>
        </div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight">
          Low-Level Design Challenges
        </h1>
        <p className="text-sm text-slate-400 mt-1 max-w-2xl">
          Each problem provides full functional requirements, constraints, and hints to simulate real-world software engineering interview scenarios.
        </p>
      </div>

      {/* Filters Bar */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4 bg-slate-900/60 p-4 rounded-2xl border border-slate-800">
        {/* Search */}
        <form onSubmit={handleSearchSubmit} className="relative flex-1">
          <Search className="h-4 w-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            placeholder="Search problems by name, entity, or keyword..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 rounded-xl bg-slate-950 border border-slate-700 text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </form>

        {/* Difficulty Tabs */}
        <div className="flex items-center gap-1 bg-slate-950 p-1 rounded-xl border border-slate-800">
          {['ALL', 'EASY', 'MEDIUM', 'HARD'].map((diff) => (
            <button
              key={diff}
              onClick={() => setSelectedDifficulty(diff)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                selectedDifficulty === diff
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white hover:bg-slate-900'
              }`}
            >
              {diff === 'ALL' ? 'All Difficulties' : diff}
            </button>
          ))}
        </div>
      </div>

      {/* Problems Grid */}
      {loading ? (
        <LoadingSpinner message="Loading problems..." />
      ) : error ? (
        <ErrorAlert message={error} onRetry={fetchProblems} />
      ) : problems.length === 0 ? (
        <div className="text-center py-16 border border-dashed border-slate-800 rounded-2xl bg-slate-900/30">
          <Layers className="h-10 w-10 text-slate-600 mx-auto mb-3" />
          <h3 className="text-base font-bold text-slate-300">No problems found</h3>
          <p className="text-xs text-slate-500 mt-1">Try adjusting your search query or difficulty filters.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
          {problems.map((problem) => (
            <ProblemCard
              key={problem.id}
              problem={problem}
              onStartPractice={handleStartPractice}
              isStarting={startingProblemId === problem.id}
            />
          ))}
        </div>
      )}
    </div>
  );
};
