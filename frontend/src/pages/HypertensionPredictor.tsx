import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Activity, TrendingUp, AlertCircle, CheckCircle, Shield, Heart } from 'lucide-react';
import { useApi } from '../hooks/useApi';
import { healthAPI } from '../services/api';
import { HypertensionData, PredictionResult } from '../types';
import LoadingSpinner from '../components/Common/LoadingSpinner';

const HypertensionPredictor: React.FC = () => {
  const [formData, setFormData] = useState<HypertensionData>({
    male: 1,
    age: 50,
    cigsPerDay: 0,
    BPMeds: 0,
    totChol: 200,
    sysBP: 120,
    diaBP: 80,
    BMI: 24.5,
    heartRate: 72,
    glucose: 90,
  });
  
  const [result, setResult] = useState<PredictionResult | null>(null);
  const { execute: predict, loading } = useApi<PredictionResult>();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const data = await predict(healthAPI.predictHypertension(formData), {
      showError: true,
      successMessage: 'Hypertension risk assessment completed',
    });
    if (data) setResult(data);
  };

  const handleChange = (name: keyof HypertensionData, value: string) => {
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
    { name: 'age', label: 'Age', min: 32, max: 70, step: 1, icon: '🎂', unit: 'years' },
    { name: 'cigsPerDay', label: 'Cigarettes per Day', min: 0, max: 70, step: 1, icon: '🚬', unit: 'cigarettes' },
    { name: 'totChol', label: 'Total Cholesterol', min: 107, max: 500, step: 1, icon: '🩸', unit: 'mg/dL' },
    { name: 'sysBP', label: 'Systolic BP', min: 83.5, max: 295, step: 0.5, icon: '❤️', unit: 'mmHg' },
    { name: 'diaBP', label: 'Diastolic BP', min: 48, max: 142.5, step: 0.5, icon: '❤️', unit: 'mmHg' },
    { name: 'BMI', label: 'BMI', min: 15.54, max: 56.8, step: 0.1, icon: '⚖️', unit: 'kg/m²' },
    { name: 'heartRate', label: 'Heart Rate', min: 44, max: 143, step: 1, icon: '💓', unit: 'bpm' },
    { name: 'glucose', label: 'Glucose', min: 40, max: 394, step: 1, icon: '🩸', unit: 'mg/dL' },
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
              <h1 className="text-3xl font-bold mb-2">Hypertension Risk Prediction</h1>
              <p className="opacity-90">Extra Trees machine learning model for blood pressure assessment</p>
              <div className="flex gap-4 mt-3">
                <span className="text-sm bg-white/20 px-3 py-1 rounded-full">Accuracy: 82%</span>
                <span className="text-sm bg-white/20 px-3 py-1 rounded-full">10 Input Features</span>
              </div>
            </div>
            <Heart className="w-16 h-16 opacity-50" />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <Activity className="w-5 h-5 mr-2 text-primary-600" />
              Patient Health Data
            </h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Gender Selection */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Gender</label>
                <div className="flex space-x-4">
                  <button
                    type="button"
                    onClick={() => setFormData({ ...formData, male: 0 })}
                    className={`flex-1 py-2 px-4 rounded-lg font-medium transition-all ${
                      formData.male === 0
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    Female
                  </button>
                  <button
                    type="button"
                    onClick={() => setFormData({ ...formData, male: 1 })}
                    className={`flex-1 py-2 px-4 rounded-lg font-medium transition-all ${
                      formData.male === 1
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    Male
                  </button>
                </div>
              </div>

              {/* BP Medication */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Blood Pressure Medication</label>
                <div className="flex space-x-4">
                  <button
                    type="button"
                    onClick={() => setFormData({ ...formData, BPMeds: 0 })}
                    className={`flex-1 py-2 px-4 rounded-lg font-medium transition-all ${
                      formData.BPMeds === 0
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    No
                  </button>
                  <button
                    type="button"
                    onClick={() => setFormData({ ...formData, BPMeds: 1 })}
                    className={`flex-1 py-2 px-4 rounded-lg font-medium transition-all ${
                      formData.BPMeds === 1
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    Yes
                  </button>
                </div>
              </div>
              
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
                    value={formData[field.name as keyof HypertensionData]}
                    onChange={(e) => handleChange(field.name as keyof HypertensionData, e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                    required
                  />
                  <p className="text-xs text-gray-400 mt-1">Range: {field.min} - {field.max}</p>
                </div>
              ))}
              
              <button
                type="submit"
                disabled={loading}
                className="w-full gradient-bg text-white py-3 rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50 mt-6"
              >
                {loading ? <LoadingSpinner size="sm" color="white" /> : 'Predict Hypertension Risk'}
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
                    <strong>Note:</strong> This assessment is for informational purposes. Consult a cardiologist for proper evaluation.
                  </p>
                </div>
                
                <div className="text-right">
                  <p className="text-xs text-gray-400">
                    Predicted: {new Date(result.timestamp).toLocaleString()}
                  </p>
                </div>
              </motion.div>
            ) : (
              <div className="text-center text-gray-400 py-12">
                <Heart className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>Enter patient data and click "Predict Hypertension Risk"</p>
                <p className="text-sm mt-2">The model will analyze blood pressure risk factors</p>
              </div>
            )}
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default HypertensionPredictor;