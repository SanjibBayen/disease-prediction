import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Activity, TrendingUp, AlertCircle, CheckCircle, Shield, Wind } from 'lucide-react';
import { useApi } from '../hooks/useApi';
import { healthAPI } from '../services/api';
import { AsthmaData, PredictionResult } from '../types';
import LoadingSpinner from '../components/Common/LoadingSpinner';

const AsthmaPredictor: React.FC = () => {
  const [formData, setFormData] = useState<AsthmaData>({
    gender_male: 0,
    smoking_ex: 0,
    smoking_non: 1,
    age: 0.3,
    peak_flow: 0.8,
  });
  
  const [result, setResult] = useState<PredictionResult | null>(null);
  const { execute: predict, loading } = useApi<PredictionResult>();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const data = await predict(healthAPI.predictAsthma(formData), {
      showError: true,
      successMessage: 'Asthma risk assessment completed',
    });
    if (data) setResult(data);
  };

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'Low': return 'bg-green-100 text-green-700 border-green-200';
      case 'Moderate': return 'bg-yellow-100 text-yellow-700 border-yellow-200';
      case 'High': return 'bg-red-100 text-red-700 border-red-200';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  const getRiskBadgeColor = (level: string) => {
    switch (level) {
      case 'Low': return 'bg-green-500';
      case 'Moderate': return 'bg-yellow-500';
      case 'High': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  return (
    <div className="p-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-7xl mx-auto"
      >
        <div className="gradient-bg rounded-2xl p-8 text-white mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold mb-2">Asthma Risk Assessment</h1>
              <p className="opacity-90">Random Forest machine learning model for respiratory health</p>
              <div className="flex gap-4 mt-3">
                <span className="text-sm bg-white/20 px-3 py-1 rounded-full">Accuracy: 83%</span>
                <span className="text-sm bg-white/20 px-3 py-1 rounded-full">5 Input Features</span>
              </div>
            </div>
            <Wind className="w-16 h-16 opacity-50" />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <Activity className="w-5 h-5 mr-2 text-primary-600" />
              Respiratory Health Data
            </h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Gender</label>
                <div className="flex space-x-4">
                  <button
                    type="button"
                    onClick={() => setFormData({ ...formData, gender_male: 0 })}
                    className={`flex-1 py-2 px-4 rounded-lg font-medium transition-all ${
                      formData.gender_male === 0
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    Female
                  </button>
                  <button
                    type="button"
                    onClick={() => setFormData({ ...formData, gender_male: 1 })}
                    className={`flex-1 py-2 px-4 rounded-lg font-medium transition-all ${
                      formData.gender_male === 1
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    Male
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Smoking Status</label>
                <div className="flex space-x-4">
                  <button
                    type="button"
                    onClick={() => setFormData({ ...formData, smoking_ex: 0, smoking_non: 1 })}
                    className={`flex-1 py-2 px-4 rounded-lg font-medium transition-all ${
                      formData.smoking_non === 1
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    Non-Smoker
                  </button>
                  <button
                    type="button"
                    onClick={() => setFormData({ ...formData, smoking_ex: 1, smoking_non: 0 })}
                    className={`flex-1 py-2 px-4 rounded-lg font-medium transition-all ${
                      formData.smoking_ex === 1
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    Ex-Smoker
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Age Range (Normalized 0-1)
                </label>
                <div className="space-y-2">
                  <input
                    type="range"
                    min={0}
                    max={1}
                    step={0.01}
                    value={formData.age}
                    onChange={(e) => setFormData({ ...formData, age: parseFloat(e.target.value) })}
                    className="w-full"
                  />
                  <div className="flex justify-between text-xs text-gray-500">
                    <span>Young (0)</span>
                    <span>Middle Age (0.5)</span>
                    <span>Elderly (1)</span>
                  </div>
                  <p className="text-sm text-gray-600">Selected: {formData.age}</p>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Peak Flow Rate (L/sec)
                </label>
                <div className="space-y-2">
                  <input
                    type="range"
                    min={0.1}
                    max={1}
                    step={0.01}
                    value={formData.peak_flow}
                    onChange={(e) => setFormData({ ...formData, peak_flow: parseFloat(e.target.value) })}
                    className="w-full"
                  />
                  <div className="flex justify-between text-xs text-gray-500">
                    <span>Low (0.1)</span>
                    <span>Normal (0.5)</span>
                    <span>High (1.0)</span>
                  </div>
                  <p className="text-sm text-gray-600">Selected: {formData.peak_flow} L/sec</p>
                </div>
              </div>
              
              <button
                type="submit"
                disabled={loading}
                className="w-full gradient-bg text-white py-3 rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50 mt-6"
              >
                {loading ? <LoadingSpinner size="sm" color="white" /> : 'Assess Asthma Risk'}
              </button>
            </form>
          </div>
          
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <TrendingUp className="w-5 h-5 mr-2 text-green-600" />
              Analysis Results
            </h2>
            
            {result ? (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="space-y-4"
              >
                <div className={`p-4 rounded-lg border ${getRiskColor(result.risk_level)}`}>
                  <div className="flex items-center">
                    {result.prediction === 1 ? (
                      <AlertCircle className="w-5 h-5 mr-2" />
                    ) : (
                      <CheckCircle className="w-5 h-5 mr-2" />
                    )}
                    <span className="font-semibold">{result.message}</span>
                  </div>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-700">Risk Level</span>
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold text-white ${getRiskBadgeColor(result.risk_level)}`}>
                    {result.risk_level}
                  </span>
                </div>
                
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Confidence Score</span>
                    <span className="text-sm font-semibold text-primary-600">{result.probability}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`${getRiskBadgeColor(result.risk_level)} h-2 rounded-full transition-all duration-500`}
                      style={{ width: `${result.probability}%` }}
                    ></div>
                  </div>
                </div>
                
                {result.recommendations && result.recommendations.length > 0 && (
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h3 className="font-semibold text-gray-800 mb-2 flex items-center">
                      <span className="text-lg mr-2">💡</span>
                      Recommendations
                    </h3>
                    <ul className="space-y-2">
                      {result.recommendations.map((rec, idx) => (
                        <li key={idx} className="text-sm text-gray-600 flex items-start">
                          <span className="text-primary-500 mr-2">•</span>
                          {rec}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                
                <div className="bg-blue-50 rounded-lg p-3">
                  <p className="text-xs text-blue-700">
                    <strong>Note:</strong> This assessment is based on statistical analysis. Consult a pulmonologist for proper diagnosis.
                  </p>
                </div>
                
                <div className="text-right">
                  <p className="text-xs text-gray-400">
                    Assessed: {new Date(result.timestamp).toLocaleString()}
                  </p>
                </div>
              </motion.div>
            ) : (
              <div className="text-center text-gray-400 py-12">
                <Wind className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>Enter respiratory data and click "Assess Asthma Risk"</p>
                <p className="text-sm mt-2">The model will analyze lung function and risk factors</p>
              </div>
            )}
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default AsthmaPredictor;