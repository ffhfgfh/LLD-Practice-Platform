import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { api } from '../services/api';
import { ProblemWithHistory } from '../types';
import { AttemptHistoryCard } from '../components/history/AttemptHistoryCard';
import { AttemptComparisonModal } from '../components/history/AttemptComparisonModal';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorAlert } from '../components/common/ErrorAlert';
import { Button } from '../components/common/Button';
import { History, Search, Layers, Compass, Plus } from 'lucide-react';

export const AttemptHistoryPage: React.FC = () => {
  const [history, setHistory] = useState<ProblemWithHistory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [compareProblem, setCompareProblem] = useState<ProblemWithHistory | null>(null);
  const [startingProblemId, setStartingProblemId] = useState<string | null>(null);
  const navigate = useNavigate();

  const fetchHistory = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getHistory();
      setHistory(data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || 'Failed to load attempt history.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleTryAgain = async (problemId: string) => {
    try {
      setStartingProblemId(problemId);
      const newAttempt = await api.createAttempt(problemId);
      navigate(`/practice/${newAttempt.id}`);
    } catch (err: any) {
      alert('Failed to start attempt: ' + (err?.response?.data?.detail || err?.message));
    } finally {
      setStartingProblemId(null);
    }
  };

  const filteredHistory = history.filter((p) => {
    if (!searchQuery.trim()) return true;
    return (
      p.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.summary.toLowerCase().includes(searchQuery.toLowerCase())
    );
  });

  const totalAttemptsCount = history.reduce((acc, p) => acc + p.total_attempts, 0);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-indigo-400 text-xs font-semibold uppercase tracking-wider mb-1">
            <History className="h-4 w-4" />
            <span>Practice History & Progression</span>
          </div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">
            Attempt History
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Review past iterations, compare feedback progression, and try problems again to refine your design.
          </p>
        </div>

        <Link to="/problems">
          <Button variant="primary" leftIcon={<Plus className="h-4 w-4" />}>
            Explore New Problems
          </Button>
        </Link>
      </div>

      {/* Search Bar */}
      <div className="relative max-w-md">
        <Search className="h-4 w-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
        <input
          type="text"
          placeholder="Filter by problem title..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full pl-10 pr-4 py-2 rounded-xl bg-slate-900 border border-slate-700 text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
      </div>

      {/* Main Content */}
      {loading ? (
        <LoadingSpinner message="Loading attempt history..." />
      ) : error ? (
        <ErrorAlert message={error} onRetry={fetchHistory} />
      ) : filteredHistory.length === 0 ? (
        <div className="text-center py-16 border border-dashed border-slate-800 rounded-2xl bg-slate-900/30">
          <Compass className="h-10 w-10 text-slate-600 mx-auto mb-3" />
          <h3 className="text-base font-bold text-slate-300">No attempts found</h3>
          <p className="text-xs text-slate-500 mt-1 mb-4">You haven't practiced any problems yet.</p>
          <Link to="/problems">
            <Button size="sm">Browse Problems</Button>
          </Link>
        </div>
      ) : (
        <div className="space-y-6">
          {filteredHistory.map((prob) => (
            <AttemptHistoryCard
              key={prob.id}
              problemHistory={prob}
              onTryAgain={handleTryAgain}
              onCompare={(p) => setCompareProblem(p)}
              isStarting={startingProblemId === prob.id}
            />
          ))}
        </div>
      )}

      {/* Comparison Modal */}
      <AttemptComparisonModal
        isOpen={compareProblem !== null}
        onClose={() => setCompareProblem(null)}
        problem={compareProblem}
      />
    </div>
  );
};
