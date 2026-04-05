import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Brain, TrendingUp, AlertCircle, Shield, Send } from 'lucide-react';
import { useApi } from '../hooks/useApi';
import { healthAPI } from '../services/api';
import { MentalHealthResponse } from '../types';
import LoadingSpinner from '../components/Common/LoadingSpinner';

const MentalHealthPredictor: React.FC = () => {
  const [text, setText] = useState('');
  const [charCount, setCharCount] = useState(0);
  const [result, setResult] = useState<MentalHealthResponse | null>(null);
  const { execute: predict, loading } = useApi<MentalHealthResponse>();

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newText = e.target.value;
    setText(newText);
    setCharCount(newText.length);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim() || text.length < 10) return;
    
    const data = await predict(healthAPI.predictMentalHealth(text), {
      showError: true,
      showSuccess: true,
      successMessage: 'Mental health analysis completed',
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

  const examplePrompts = [
    "I've been feeling very anxious lately and having trouble sleeping...",
    "I feel hopeless and sad most days. Nothing brings me joy anymore...",
    "I'm generally happy and motivated. I enjoy my work and hobbies...",
  ];

  return (
    <div className="p-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-7xl mx-auto"
      >
        {/* Header */}
        <div className="gradient-bg rounded-2xl p-8 text-white mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold mb-2">Mental Health Assessment</h1>
              <p className="opacity-90">NLP Transformer model for depression and anxiety analysis</p>
              <div className="flex gap-4 mt-3">
                <span className="text-sm bg-white/20 px-3 py-1 rounded-full">Accuracy: 82%</span>
                <span className="text-sm bg-white/20 px-3 py-1 rounded-full">Text Analysis</span>
              </div>
            </div>
            <Brain className="w-16 h-16 opacity-50" />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Section */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <Send className="w-5 h-5 mr-2 text-primary-600" />
              Describe Your Symptoms
            </h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  How have you been feeling lately?
                </label>
                <textarea
                  value={text}
                  onChange={handleTextChange}
                  placeholder="Example: I've been feeling very anxious lately and having trouble sleeping. I feel overwhelmed with work and can't concentrate..."
                  rows={8}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
                  required
                />
                <div className="flex justify-between mt-2">
                  <p className="text-xs text-gray-400">
                    Minimum 10 characters
                  </p>
                  <p className={`text-xs ${charCount < 10 ? 'text-red-500' : 'text-green-500'}`}>
                    {charCount} / 5000 characters
                  </p>
                </div>
              </div>

              {/* Example Prompts */}
              <div>
                <p className="text-xs text-gray-500 mb-2">Try an example:</p>
                <div className="flex flex-wrap gap-2">
                  {examplePrompts.map((prompt, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => {
                        setText(prompt);
                        setCharCount(prompt.length);
                      }}
                      className="text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1 rounded-full transition-colors"
                    >
                      Example {idx + 1}
                    </button>
                  ))}
                </div>
              </div>
              
              <button
                type="submit"
                disabled={loading || text.length < 10}
                className="w-full gradient-bg text-white py-3 rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50 mt-6"
              >
                {loading ? <LoadingSpinner size="sm" color="white" /> : 'Analyze Mental Health'}
              </button>
            </form>
          </div>
          
          {/* Results Section */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <TrendingUp className="w-5 h-5 mr-2 text-green-600" />
              Assessment Results
            </h2>
            
            {result ? (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="space-y-4"
              >
                <div className={`p-4 rounded-lg border ${getRiskColor(result.risk_level)}`}>
                  <div className="flex items-center">
                    <AlertCircle className="w-5 h-5 mr-2" />
                    <span className="font-semibold">{result.message}</span>
                  </div>
                </div>
                
                {/* Depression Risk */}
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Depression Risk</span>
                    <span className="text-sm font-semibold" style={{ color: result.depression_risk > 60 ? '#dc2626' : result.depression_risk > 30 ? '#d97706' : '#059669' }}>
                      {result.depression_risk}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="h-2 rounded-full transition-all duration-500"
                      style={{ 
                        width: `${result.depression_risk}%`,
                        backgroundColor: result.depression_risk > 60 ? '#dc2626' : result.depression_risk > 30 ? '#d97706' : '#10b981'
                      }}
                    ></div>
                  </div>
                </div>
                
                {/* Anxiety Risk */}
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Anxiety Risk</span>
                    <span className="text-sm font-semibold" style={{ color: result.anxiety_risk > 60 ? '#dc2626' : result.anxiety_risk > 30 ? '#d97706' : '#059669' }}>
                      {result.anxiety_risk}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="h-2 rounded-full transition-all duration-500"
                      style={{ 
                        width: `${result.anxiety_risk}%`,
                        backgroundColor: result.anxiety_risk > 60 ? '#dc2626' : result.anxiety_risk > 30 ? '#d97706' : '#10b981'
                      }}
                    ></div>
                  </div>
                </div>
                
                {/* Overall Risk Level */}
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-700">Overall Risk Level</span>
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold text-white ${getRiskBadgeColor(result.risk_level)}`}>
                    {result.risk_level}
                  </span>
                </div>
                
                {/* Recommendations */}
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
                
                {/* Crisis Disclaimer */}
                <div className="bg-red-50 rounded-lg p-3 border border-red-200">
                  <p className="text-xs text-red-700">
                    <strong>⚠️ Crisis Support:</strong> If you're experiencing a mental health crisis, 
                    please contact emergency services or a crisis helpline immediately.
                  </p>
                </div>
                
                <div className="bg-blue-50 rounded-lg p-3">
                  <p className="text-xs text-blue-700">
                    <strong>Note:</strong> This is an AI-powered screening tool only. 
                    Not a substitute for professional mental health diagnosis.
                  </p>
                </div>
                
                <div className="text-right">
                  <p className="text-xs text-gray-400">
                    Analyzed: {new Date(result.timestamp).toLocaleString()}
                  </p>
                </div>
              </motion.div>
            ) : (
              <div className="text-center text-gray-400 py-12">
                <Brain className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>Describe your symptoms to get an assessment</p>
                <p className="text-sm mt-2">The AI will analyze your text for depression and anxiety indicators</p>
              </div>
            )}
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default MentalHealthPredictor;