import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Sidebar from './components/Layout/Sidebar';
import Header from './components/Layout/Header';
import Dashboard from './pages/Dashboard';
import DiabetesPredictor from './pages/DiabetesPredictor';
import HypertensionPredictor from './pages/HypertensionPredictor';
import CardiovascularPredictor from './pages/CardiovascularPredictor';
import StrokePredictor from './pages/StrokePredictor';
import AsthmaPredictor from './pages/AsthmaPredictor';
import MentalHealthPredictor from './pages/MentalHealthPredictor';
import SleepHealthPredictor from './pages/SleepHealthPredictor';
import Analytics from './pages/Analytics';



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
              <Route path="/hypertension" element={<HypertensionPredictor />} />
              <Route path="/cardiovascular" element={<CardiovascularPredictor />} />
              <Route path="/stroke" element={<StrokePredictor />} />
              <Route path="/asthma" element={<AsthmaPredictor />} />
              <Route path="/mental-health" element={<MentalHealthPredictor />} />
              <Route path="/sleep" element={<SleepHealthPredictor />} />
              <Route path="/analytics" element={<Analytics />} />
            </Routes>
          </main>
        </div>
        <Toaster 
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
            success: {
              iconTheme: {
                primary: '#10b981',
                secondary: '#fff',
              },
            },
            error: {
              iconTheme: {
                primary: '#ef4444',
                secondary: '#fff',
              },
            },
          }}
        />
      </div>
    </Router>
  );
}

export default App;