import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Activity, TrendingUp, AlertCircle, CheckCircle, Shield, Brain } from 'lucide-react';
import { useApi } from '../hooks/useApi';
import { healthAPI } from '../services/api';
import { StrokeData, PredictionResult } from '../types';
import LoadingSpinner from '../components/Common/LoadingSpinner';

const StrokePredictor: React.FC = () => {
  const [formData, setFormData] = useState<StrokeData>({
    age: 55,
    hypertension: 0,
    heart_disease: 0,
    ever_married: 1,
    avg_glucose_level: 120,
    bmi: 25.5,
    smoking_status: 0,
  });
  
  const [result, setResult] = useState<PredictionResult | null>(null);
  const { execute: predict, loading } = useApi<PredictionResult>();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const data = await predict(healthAPI.predictStroke(formData), {
      showError: true,
      successMessage: 'Stroke risk assessment completed',
    });
    if (data) setResult(data);
  };

  const handleChange = (name: keyof StrokeData, value: string) => {
    setFormData({ ...formData, [name]: parseFloat(value) || 0 });
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

  const inputFields = [
    { name: 'age', label: 'Age', min: 0, max: 82, step: 1, icon: '🎂', unit: 'years' },
    { name: 'avg_glucose_level', label: 'Average Glucose', min: 55, max: 270, step: 1, icon: '🩸', unit: 'mg/dL' },
    { name: 'bmi', label: 'BMI', min: 13.5, max: 98, step: 0.1, icon: '⚖️', unit: 'kg/m²' },
  ];

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
              <h1 className="text-3xl font-bold mb-2">Stroke Risk Prediction</h1>
              <p className="opacity-90">Ensemble machine learning model for stroke risk assessment</p>
              <div className="flex gap-4 mt-3">
                <span className="text-sm bg-white/20 px-3 py-1 rounded-full">Accuracy: 80%</span>
                <span className="text-sm bg-white/20 px-3 py-1 rounded-full">7 Input Features</span>
              </div>
            </div>
            <Brain className="w-16 h-16 opacity-50" />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <Activity className="w-5 h-5 mr-2 text-primary-600" />
              Patient Health Data
            </h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              {inputFields.map((field) => (
                <div key={field.name}>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {field.icon} {field.label} ({field.unit})
                  </label>
                  <input
                    type="number"
                    step={field.step}
                    min={field.min}
                    max={field.max}
                    value={formData[field.name as keyof StrokeData]}
                    onChange={(e) => handleChange(field.name as keyof StrokeData, e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                    required
                  />
                  <p className="text-xs text-gray-400 mt-1">Range: {field.min} - {field.max}</p>
                </div>
              ))}

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Medical History</label>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-xs text-gray-500 mb-1">Hypertension</p>
                    <div className="flex gap-2">
                      <button
                        type="button"
                        onClick={() => setFormData({ ...formData, hypertension: 0 })}
                        className={`flex-1 py-1 px-2 rounded text-sm ${
                          formData.hypertension === 0 ? 'bg-primary-600 text-white' : 'bg-gray-100'
                        }`}
                      >
                        No
                      </button>
                      <button
                        type="button"
                        onClick={() => setFormData({ ...formData, hypertension: 1 })}
                        className={`flex-1 py-1 px-2 rounded text-sm ${
                          formData.hypertension === 1 ? 'bg-primary-600 text-white' : 'bg-gray-100'
                        }`}
                      >
                        Yes
                      </button>
                    </div>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500 mb-1">Heart Disease</p>
                    <div className="flex gap-2">
                      <button
                        type="button"
                        onClick={() => setFormData({ ...formData, heart_disease: 0 })}
                        className={`flex-1 py-1 px-2 rounded text-sm ${
                          formData.heart_disease === 0 ? 'bg-primary-600 text-white' : 'bg-gray-100'
                        }`}
                      >
                        No
                      </button>
                      <button
                        type="button"
                        onClick={() => setFormData({ ...formData, heart_disease: 1 })}
                        className={`flex-1 py-1 px-2 rounded text-sm ${
                          formData.heart_disease === 1 ? 'bg-primary-600 text-white' : 'bg-gray-100'
                        }`}
                      >
                        Yes
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Marital Status</label>
                <div className="flex gap-4">
                  <button
                    type="button"
                    onClick={() => setFormData({ ...formData, ever_married: 0 })}
                    className={`flex-1 py-2 px-4 rounded-lg font-medium transition-all ${
                      formData.ever_married === 0
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    Never Married
                  </button>
                  <button
                    type="button"
                    onClick={() => setFormData({ ...formData, ever_married: 1 })}
                    className={`flex-1 py-2 px-4 rounded-lg font-medium transition-all ${
                      formData.ever_married === 1
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    Ever Married
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Smoking Status</label>
                <div className="grid grid-cols-2 gap-2">
                  {[
                    { value: 0, label: 'Never Smoked' },
                    { value: 1, label: 'Former Smoker' },
                    { value: 2, label: 'Smokes' },
                    { value: 3, label: 'Unknown' },
                  ].map((opt) => (
                    <button
                      key={opt.value}
                      type="button"
                      onClick={() => setFormData({ ...formData, smoking_status: opt.value })}
                      className={`py-2 px-3 rounded-lg text-sm font-medium transition-all ${
                        formData.smoking_status === opt.value
                          ? 'bg-primary-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      {opt.label}
                    </button>
                  ))}
                </div>
              </div>
              
              <button
                type="submit"
                disabled={loading}
                className="w-full gradient-bg text-white py-3 rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50 mt-6"
              >
                {loading ? <LoadingSpinner size="sm" color="white" /> : 'Assess Stroke Risk'}
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
                    <strong>Note:</strong> This assessment is for informational purposes. Consult a neurologist for proper evaluation.
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
                <Brain className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>Enter patient data and click "Assess Stroke Risk"</p>
                <p className="text-sm mt-2">The model will analyze stroke risk factors</p>
              </div>
            )}
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default StrokePredictor;