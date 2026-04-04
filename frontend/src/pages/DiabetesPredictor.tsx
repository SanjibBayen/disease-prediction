import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useForm } from 'react-hook-form';
import toast, { Toaster } from 'react-hot-toast';
import { Activity, TrendingUp, AlertCircle, CheckCircle, Shield } from 'lucide-react';
import { healthAPI } from '../services/api';
import { type DiabetesData, type PredictionResult } from '../types';

const DiabetesPredictor: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
  
  const { register, handleSubmit, formState: { errors } } = useForm<DiabetesData>({
    defaultValues: {
      pregnancies: 0,
      glucose: 100,
      blood_pressure: 80,
      skin_thickness: 20,
      insulin: 79,
      bmi: 25,
      diabetes_pedigree: 0.5,
      age: 30,
    }
  });

  const onSubmit = async (data: DiabetesData) => {
    setLoading(true);
    try {
      const response = await healthAPI.predictDiabetes(data);
      setResult(response.data);
      toast.success('Prediction completed successfully!');
    } catch (error) {
      toast.error('Prediction failed. Please try again.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const inputFields = [
    { name: 'pregnancies', label: 'Number of Pregnancies', min: 0, max: 20, step: 1, icon: '👶' },
    { name: 'glucose', label: 'Glucose Level (mg/dL)', min: 0, max: 300, step: 1, icon: '🩸' },
    { name: 'blood_pressure', label: 'Blood Pressure (mmHg)', min: 0, max: 200, step: 1, icon: '❤️' },
    { name: 'skin_thickness', label: 'Skin Thickness (mm)', min: 0, max: 100, step: 1, icon: '📏' },
    { name: 'insulin', label: 'Insulin Level (mu U/ml)', min: 0, max: 900, step: 1, icon: '💉' },
    { name: 'bmi', label: 'BMI (Body Mass Index)', min: 0, max: 70, step: 0.1, icon: '⚖️' },
    { name: 'diabetes_pedigree', label: 'Diabetes Pedigree Function', min: 0, max: 2.5, step: 0.01, icon: '📊' },
    { name: 'age', label: 'Age (years)', min: 1, max: 120, step: 1, icon: '🎂' },
  ];

  return (
    <div className="p-8">
      <Toaster position="top-right" />
      
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-7xl mx-auto"
      >
        {/* Header */}
        <div className="gradient-bg rounded-2xl p-8 text-white mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold mb-2">Diabetes Risk Prediction</h1>
              <p className="opacity-90">Advanced SVC machine learning model for accurate diabetes detection</p>
            </div>
            <Shield className="w-16 h-16 opacity-50" />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form Section */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <Activity className="w-5 h-5 mr-2 text-primary-600" />
              Patient Health Data
            </h2>
            
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              {inputFields.map((field) => (
                <div key={field.name}>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {field.icon} {field.label}
                  </label>
                  <input
                    type="number"
                    step={field.step}
                    {...register(field.name as keyof DiabetesData, { 
                      required: true,
                      min: field.min,
                      max: field.max
                    })}
                    className="input-field"
                  />
                  {errors[field.name as keyof DiabetesData] && (
                    <p className="text-red-500 text-xs mt-1">Please enter a valid value</p>
                  )}
                </div>
              ))}
              
              <button
                type="submit"
                disabled={loading}
                className="w-full btn-primary py-3 mt-6"
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    Analyzing...
                  </div>
                ) : (
                  'Predict Diabetes Risk'
                )}
              </button>
            </form>
          </div>
          
          {/* Results Section */}
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
                <div className={`p-4 rounded-lg ${result.prediction === 1 ? 'bg-red-50 border border-red-200' : 'bg-green-50 border border-green-200'}`}>
                  <div className="flex items-center">
                    {result.prediction === 1 ? (
                      <AlertCircle className="w-5 h-5 mr-2 text-red-600" />
                    ) : (
                      <CheckCircle className="w-5 h-5 mr-2 text-green-600" />
                    )}
                    <span className={`font-semibold ${result.prediction === 1 ? 'text-red-600' : 'text-green-600'}`}>
                      {result.message}
                    </span>
                  </div>
                </div>
                
                <div>
                  <p className="text-gray-600 mb-2">Risk Level</p>
                  <div className="relative pt-1">
                    <div className="flex mb-2 items-center justify-between">
                      <div>
                        <span className={`text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full ${
                          result.risk_level === 'High' ? 'bg-red-200 text-red-600' : 'bg-green-200 text-green-600'
                        }`}>
                          {result.risk_level} Risk
                        </span>
                      </div>
                      <div className="text-right">
                        <span className="text-xs font-semibold inline-block text-primary-600">
                          {result.probability}% Confidence
                        </span>
                      </div>
                    </div>
                    <div className="overflow-hidden h-2 mb-4 text-xs flex rounded bg-gray-200">
                      <div
                        style={{ width: `${result.probability}%` }}
                        className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center gradient-bg"
                      ></div>
                    </div>
                  </div>
                </div>
                
                <div className="bg-gray-50 rounded-lg p-4">
                  <h3 className="font-semibold text-gray-800 mb-2">Recommendations</h3>
                  <ul className="space-y-2">
                    {result.recommendations.map((rec, idx) => (
                      <li key={idx} className="text-sm text-gray-600 flex items-start">
                        <span className="text-primary-500 mr-2">•</span>
                        {rec}
                      </li>
                    ))}
                  </ul>
                </div>
                
                <div className="text-right">
                  <p className="text-xs text-gray-400">Predicted on: {new Date(result.timestamp).toLocaleString()}</p>
                </div>
              </motion.div>
            ) : (
              <div className="text-center text-gray-400 py-12">
                <Activity className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>Fill the form and click predict to see results</p>
              </div>
            )}
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default DiabetesPredictor;