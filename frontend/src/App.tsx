import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/layout/Layout';
import { DashboardPage } from './pages/DashboardPage';
import { ProblemListPage } from './pages/ProblemListPage';
import { ProblemDetailPage } from './pages/ProblemDetailPage';
import { PracticePage } from './pages/PracticePage';
import { AttemptHistoryPage } from './pages/AttemptHistoryPage';
import { FeedbackPage } from './pages/FeedbackPage';
import { NotFoundPage } from './pages/NotFoundPage';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<DashboardPage />} />
          <Route path="problems" element={<ProblemListPage />} />
          <Route path="problems/:id" element={<ProblemDetailPage />} />
          <Route path="practice/:attemptId" element={<PracticePage />} />
          <Route path="attempts" element={<AttemptHistoryPage />} />
          <Route path="attempts/:attemptId/feedback" element={<FeedbackPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;
