import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Layout/Sidebar';
import Header from './components/Layout/Header';
import Dashboard from './pages/Dashboard';
import DiabetesPredictor from './pages/DiabetesPredictor';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Sidebar />
        <div className="ml-64">
          <Header />
          <main>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/diabetes" element={<DiabetesPredictor />} />
              <Route path="/hypertension" element={<div className="p-8"><h1>Hypertension Prediction</h1></div>} />
              <Route path="/cardiovascular" element={<div className="p-8"><h1>Cardiovascular Prediction</h1></div>} />
              <Route path="/stroke" element={<div className="p-8"><h1>Stroke Prediction</h1></div>} />
              <Route path="/asthma" element={<div className="p-8"><h1>Asthma Prediction</h1></div>} />
              <Route path="/sleep" element={<div className="p-8"><h1>Sleep Health Analysis</h1></div>} />
              <Route path="/consultant" element={<div className="p-8"><h1>Medical Consultant</h1></div>} />
              <Route path="/analytics" element={<div className="p-8"><h1>Analytics Dashboard</h1></div>} />
              <Route path="/settings" element={<div className="p-8"><h1>Settings</h1></div>} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;