import { Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import { Header } from './components/Header/Header';
import { Walkthrough } from './features/core/walkthrough/Walkthrough';
import { loadAllInvestigationBriefs } from './data/investigationBriefLoader';
import { WorkflowCanvas } from './features/core/workflow/WorkflowCanvas';

import { Homepage } from './features/home/Homepage';

const loadedBriefs = loadAllInvestigationBriefs();
const defaultInvestigation = loadedBriefs.length > 0 ? loadedBriefs[0] : ({} as any);

export default function App() {
  return (
    <div className="app-container">
      <Header />

      <main className="main-content">
        <Routes>
          <Route path="/" element={<Homepage />} />
          <Route path="/index.dev.html" element={<Navigate to="/" replace />} />
          <Route path="/walkthrough" element={<Walkthrough />} />
          <Route path="/workflow" element={<WorkflowCanvas investigation={defaultInvestigation as any} />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}
