import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Activity, TrendingUp, AlertCircle, CheckCircle, Shield, Heart } from 'lucide-react';
import { useApi } from '../hooks/useApi';
import { healthAPI } from '../services/api';
import { CardioData, PredictionResult } from '../types';
import LoadingSpinner from '../components/Common/LoadingSpinner';

const CardiovascularPredictor: React.FC = () => {
  const [formData, setFormData] = useState<CardioData>({
    age: 45,
    ap_hi: 120,
    ap_lo: 80,
    cholesterol: 1,
    gluc: 1,
    smoke: 0,
    alco: 0,
    active: 1,
    weight: 75,
  });
  
  const [result, setResult] = useState<PredictionResult | null>(null);
  const { execute: predict, loading } = useApi<PredictionResult>();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const data = await predict(healthAPI.predictCardio(formData), {
      showError: true,
      successMessage: 'Cardiovascular risk assessment completed',
    });
    if (data) setResult(data);
  };

  const handleChange = (name: keyof CardioData, value: string) => {
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
    { name: 'age', label: 'Age', min: 29, max: 65, step: 1, icon: '🎂', unit: 'years' },
    { name: 'ap_hi', label: 'Systolic BP', min: 90, max: 200, step: 1, icon: '❤️', unit: 'mmHg' },
    { name: 'ap_lo', label: 'Diastolic BP', min: 60, max: 140, step: 1, icon: '❤️', unit: 'mmHg' },
    { name: 'weight', label: 'Weight', min: 30, max: 200, step: 1, icon: '⚖️', unit: 'kg' },
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
              <h1 className="text-3xl font-bold mb-2">Cardiovascular Risk Assessment</h1>
              <p className="opacity-90">XGBoost machine learning model for heart disease prediction</p>
              <div className="flex gap-4 mt-3">
                <span className="text-sm bg-white/20 px-3 py-1 rounded-full">Accuracy: 78%</span>
                <span className="text-sm bg-white/20 px-3 py-1 rounded-full">9 Input Features</span>
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
                    value={formData[field.name as keyof CardioData]}
                    onChange={(e) => handleChange(field.name as keyof CardioData, e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                    required
                  />
                  <p className="text-xs text-gray-400 mt-1">Range: {field.min} - {field.max}</p>
                </div>
              ))}

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Cholesterol Level</label>
                <div className="grid grid-cols-3 gap-2">
                  {[
                    { value: 1, label: 'Normal', color: 'green', description: '< 200 mg/dL' },
                    { value: 2, label: 'Above Normal', color: 'yellow', description: '200-239 mg/dL' },
                    { value: 3, label: 'Well Above Normal', color: 'red', description: '> 240 mg/dL' },
                  ].map((opt) => (
                    <button
                      key={opt.value}
                      type="button"
                      onClick={() => setFormData({ ...formData, cholesterol: opt.value })}
                      className={`py-2 px-3 rounded-lg text-sm font-medium transition-all ${
                        formData.cholesterol === opt.value
                          ? 'bg-primary-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      {opt.label}
                    </button>
                  ))}
                </div>
                <p className="text-xs text-gray-400 mt-1">Total cholesterol level classification</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Glucose Level</label>
                <div className="grid grid-cols-3 gap-2">
                  {[
                    { value: 1, label: 'Normal', description: '< 100 mg/dL' },
                    { value: 2, label: 'Above Normal', description: '100-125 mg/dL' },
                    { value: 3, label: 'Well Above Normal', description: '> 126 mg/dL' },
                  ].map((opt) => (
                    <button
                      key={opt.value}
                      type="button"
                      onClick={() => setFormData({ ...formData, gluc: opt.value })}
                      className={`py-2 px-3 rounded-lg text-sm font-medium transition-all ${
                        formData.gluc === opt.value
                          ? 'bg-primary-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      {opt.label}
                    </button>
                  ))}
                </div>
                <p className="text-xs text-gray-400 mt-1">Fasting glucose level classification</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Lifestyle Factors</label>
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <p className="text-xs text-gray-500 mb-1">Smoking</p>
                    <div className="flex gap-2">
                      <button
                        type="button"
                        onClick={() => setFormData({ ...formData, smoke: 0 })}
                        className={`flex-1 py-1 px-2 rounded text-sm ${
                          formData.smoke === 0 ? 'bg-primary-600 text-white' : 'bg-gray-100'
                        }`}
                      >
                        No
                      </button>
                      <button
                        type="button"
                        onClick={() => setFormData({ ...formData, smoke: 1 })}
                        className={`flex-1 py-1 px-2 rounded text-sm ${
                          formData.smoke === 1 ? 'bg-primary-600 text-white' : 'bg-gray-100'
                        }`}
                      >
                        Yes
                      </button>
                    </div>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500 mb-1">Alcohol</p>
                    <div className="flex gap-2">
                      <button
                        type="button"
                        onClick={() => setFormData({ ...formData, alco: 0 })}
                        className={`flex-1 py-1 px-2 rounded text-sm ${
                          formData.alco === 0 ? 'bg-primary-600 text-white' : 'bg-gray-100'
                        }`}
                      >
                        No
                      </button>
                      <button
                        type="button"
                        onClick={() => setFormData({ ...formData, alco: 1 })}
                        className={`flex-1 py-1 px-2 rounded text-sm ${
                          formData.alco === 1 ? 'bg-primary-600 text-white' : 'bg-gray-100'
                        }`}
                      >
                        Yes
                      </button>
                    </div>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500 mb-1">Active</p>
                    <div className="flex gap-2">
                      <button
                        type="button"
                        onClick={() => setFormData({ ...formData, active: 0 })}
                        className={`flex-1 py-1 px-2 rounded text-sm ${
                          formData.active === 0 ? 'bg-primary-600 text-white' : 'bg-gray-100'
                        }`}
                      >
                        No
                      </button>
                      <button
                        type="button"
                        onClick={() => setFormData({ ...formData, active: 1 })}
                        className={`flex-1 py-1 px-2 rounded text-sm ${
                          formData.active === 1 ? 'bg-primary-600 text-white' : 'bg-gray-100'
                        }`}
                      >
                        Yes
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              
              <button
                type="submit"
                disabled={loading}
                className="w-full gradient-bg text-white py-3 rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50 mt-6"
              >
                {loading ? <LoadingSpinner size="sm" color="white" /> : 'Assess Cardiovascular Risk'}
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
                    Assessed: {new Date(result.timestamp).toLocaleString()}
                  </p>
                </div>
              </motion.div>
            ) : (
              <div className="text-center text-gray-400 py-12">
                <Heart className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>Enter patient data and click "Assess Cardiovascular Risk"</p>
                <p className="text-sm mt-2">The model will analyze heart disease risk factors</p>
              </div>
            )}
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default CardiovascularPredictor;