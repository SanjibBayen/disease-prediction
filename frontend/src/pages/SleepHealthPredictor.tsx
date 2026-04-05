import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Activity, TrendingUp, AlertCircle, CheckCircle, Moon, BarChart3 } from 'lucide-react';
import { useApi } from '../hooks/useApi';
import { healthAPI } from '../services/api';
import { SleepData, PredictionResult } from '../types';
import LoadingSpinner from '../components/Common/LoadingSpinner';

const SleepHealthPredictor: React.FC = () => {
  const [formData, setFormData] = useState<SleepData>({
    gender: 'Male',
    age: 35,
    occupation: 'Software Engineer',
    sleep_duration: 7.0,
    quality_of_sleep: 7,
    physical_activity_level: 45,
    stress_level: 5,
    bmi_category: 'Normal',
    blood_pressure: '120/80',
    heart_rate: 72,
    daily_steps: 7000,
  });
  
  const [systolic, setSystolic] = useState(120);
  const [diastolic, setDiastolic] = useState(80);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const { execute: predict, loading } = useApi<PredictionResult>();

  // Update blood pressure string when systolic/diastolic change
  const updateBloodPressure = (sys: number, dia: number) => {
    setSystolic(sys);
    setDiastolic(dia);
    setFormData({ ...formData, blood_pressure: `${sys}/${dia}` });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Prepare data for API - using snake_case to match backend
    const apiData = {
      gender: formData.gender,
      age: formData.age,
      occupation: formData.occupation,
      sleep_duration: formData.sleep_duration,
      quality_of_sleep: formData.quality_of_sleep,
      physical_activity_level: formData.physical_activity_level,
      stress_level: formData.stress_level,
      bmi_category: formData.bmi_category,
      blood_pressure: formData.blood_pressure,
      heart_rate: formData.heart_rate,
      daily_steps: formData.daily_steps,
    };
    
    // Call the sleep health API endpoint
    const data = await predict(healthAPI.predictSleep(apiData), {
      showError: true,
      successMessage: 'Sleep health analysis completed',
    });
    if (data) setResult(data);
  };

  const handleChange = (name: keyof SleepData, value: string | number) => {
    setFormData({ ...formData, [name]: value });
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

  const occupations = [
    'Software Engineer', 'Doctor', 'Sales Representative', 'Teacher', 
    'Business', 'Scientist', 'Accountant', 'Engineer', 'Nurse', 
    'Lawyer', 'Manager', 'Analyst'
  ];

  const bmiCategories = ['Normal', 'Overweight', 'Obese'];

  const getBmiCategoryColor = (category: string) => {
    switch (category) {
      case 'Normal': return 'text-green-600';
      case 'Overweight': return 'text-yellow-600';
      case 'Obese': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

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
              <h1 className="text-3xl font-bold mb-2">Sleep Health Analysis</h1>
              <p className="opacity-90">SVC machine learning model for sleep disorder detection and analysis</p>
              <div className="flex gap-4 mt-3">
                <span className="text-sm bg-white/20 px-3 py-1 rounded-full">Accuracy: 76%</span>
                <span className="text-sm bg-white/20 px-3 py-1 rounded-full">11 Input Features</span>
                <span className="text-sm bg-white/20 px-3 py-1 rounded-full">SVC Classifier</span>
              </div>
            </div>
            <Moon className="w-16 h-16 opacity-50" />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form Section */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <Activity className="w-5 h-5 mr-2 text-primary-600" />
              Sleep Health Data
            </h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Gender */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Gender</label>
                <div className="flex space-x-4">
                  <button
                    type="button"
                    onClick={() => handleChange('gender', 'Male')}
                    className={`flex-1 py-2 px-4 rounded-lg font-medium transition-all ${
                      formData.gender === 'Male'
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    Male
                  </button>
                  <button
                    type="button"
                    onClick={() => handleChange('gender', 'Female')}
                    className={`flex-1 py-2 px-4 rounded-lg font-medium transition-all ${
                      formData.gender === 'Female'
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    Female
                  </button>
                </div>
              </div>

              {/* Age */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  🎂 Age (years)
                </label>
                <input
                  type="number"
                  min={27}
                  max={59}
                  value={formData.age}
                  onChange={(e) => handleChange('age', parseInt(e.target.value))}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  required
                />
                <p className="text-xs text-gray-400 mt-1">Range: 27 - 59 years</p>
              </div>

              {/* Occupation */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  💼 Occupation
                </label>
                <select
                  value={formData.occupation}
                  onChange={(e) => handleChange('occupation', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                >
                  {occupations.map(occ => (
                    <option key={occ} value={occ}>{occ}</option>
                  ))}
                </select>
              </div>

              {/* Sleep Duration */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  😴 Sleep Duration (hours)
                </label>
                <div className="space-y-2">
                  <input
                    type="range"
                    min={5.8}
                    max={8.5}
                    step={0.1}
                    value={formData.sleep_duration}
                    onChange={(e) => handleChange('sleep_duration', parseFloat(e.target.value))}
                    className="w-full"
                  />
                  <div className="flex justify-between text-xs text-gray-500">
                    <span>Poor (&lt;6h)</span>
                    <span>Good (7-8h)</span>
                    <span>Excess (&gt;8.5h)</span>
                  </div>
                  <p className="text-sm text-gray-600">Selected: {formData.sleep_duration} hours</p>
                </div>
              </div>

              {/* Quality of Sleep */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  ⭐ Quality of Sleep (1-10)
                </label>
                <div className="space-y-2">
                  <input
                    type="range"
                    min={4}
                    max={9}
                    step={1}
                    value={formData.quality_of_sleep}
                    onChange={(e) => handleChange('quality_of_sleep', parseInt(e.target.value))}
                    className="w-full"
                  />
                  <div className="flex justify-between text-xs text-gray-500">
                    <span>Poor (4)</span>
                    <span>Average (6-7)</span>
                    <span>Excellent (9)</span>
                  </div>
                  <p className="text-sm text-gray-600">Selected: {formData.quality_of_sleep}/10</p>
                </div>
              </div>

              {/* Physical Activity Level */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  🏃 Physical Activity (minutes/day)
                </label>
                <div className="space-y-2">
                  <input
                    type="range"
                    min={30}
                    max={90}
                    step={5}
                    value={formData.physical_activity_level}
                    onChange={(e) => handleChange('physical_activity_level', parseInt(e.target.value))}
                    className="w-full"
                  />
                  <div className="flex justify-between text-xs text-gray-500">
                    <span>Low (30)</span>
                    <span>Moderate (45-60)</span>
                    <span>High (90)</span>
                  </div>
                  <p className="text-sm text-gray-600">Selected: {formData.physical_activity_level} minutes/day</p>
                </div>
              </div>

              {/* Stress Level */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  😰 Stress Level (1-10)
                </label>
                <div className="space-y-2">
                  <input
                    type="range"
                    min={3}
                    max={8}
                    step={1}
                    value={formData.stress_level}
                    onChange={(e) => handleChange('stress_level', parseInt(e.target.value))}
                    className="w-full"
                  />
                  <div className="flex justify-between text-xs text-gray-500">
                    <span>Low (3)</span>
                    <span>Moderate (5-6)</span>
                    <span>High (8)</span>
                  </div>
                  <p className="text-sm text-gray-600">Selected: {formData.stress_level}/10</p>
                </div>
              </div>

              {/* BMI Category */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">BMI Category</label>
                <div className="grid grid-cols-3 gap-2">
                  {bmiCategories.map((cat) => (
                    <button
                      key={cat}
                      type="button"
                      onClick={() => handleChange('bmi_category', cat)}
                      className={`py-2 px-3 rounded-lg text-sm font-medium transition-all ${
                        formData.bmi_category === cat
                          ? 'bg-primary-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      {cat}
                    </button>
                  ))}
                </div>
                <p className="text-xs text-gray-400 mt-1">
                  BMI ranges: Normal (18.5-24.9), Overweight (25-29.9), Obese (30+)
                </p>
              </div>

              {/* Blood Pressure */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  💓 Blood Pressure (mmHg)
                </label>
                <div className="flex gap-4">
                  <div className="flex-1">
                    <label className="text-xs text-gray-500">Systolic</label>
                    <input
                      type="number"
                      min={110}
                      max={140}
                      value={systolic}
                      onChange={(e) => updateBloodPressure(parseInt(e.target.value), diastolic)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                    />
                  </div>
                  <div className="flex-1">
                    <label className="text-xs text-gray-500">Diastolic</label>
                    <input
                      type="number"
                      min={70}
                      max={95}
                      value={diastolic}
                      onChange={(e) => updateBloodPressure(systolic, parseInt(e.target.value))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                    />
                  </div>
                </div>
                <p className="text-xs text-gray-400 mt-1">Normal range: 120/80 mmHg</p>
              </div>

              {/* Heart Rate */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  💓 Heart Rate (bpm)
                </label>
                <input
                  type="number"
                  min={65}
                  max={86}
                  value={formData.heart_rate}
                  onChange={(e) => handleChange('heart_rate', parseInt(e.target.value))}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  required
                />
                <p className="text-xs text-gray-400 mt-1">Range: 65 - 86 bpm (resting heart rate)</p>
              </div>

              {/* Daily Steps */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  👣 Daily Steps
                </label>
                <div className="space-y-2">
                  <input
                    type="range"
                    min={3000}
                    max={10000}
                    step={500}
                    value={formData.daily_steps}
                    onChange={(e) => handleChange('daily_steps', parseInt(e.target.value))}
                    className="w-full"
                  />
                  <div className="flex justify-between text-xs text-gray-500">
                    <span>Sedentary (3k)</span>
                    <span>Active (7k)</span>
                    <span>Very Active (10k)</span>
                  </div>
                  <p className="text-sm text-gray-600">Selected: {formData.daily_steps} steps/day</p>
                </div>
              </div>
              
              <button
                type="submit"
                disabled={loading}
                className="w-full gradient-bg text-white py-3 rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50 mt-6"
              >
                {loading ? <LoadingSpinner size="sm" color="white" /> : 'Analyze Sleep Health'}
              </button>
            </form>
          </div>
          
          {/* Results Section */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <TrendingUp className="w-5 h-5 mr-2 text-green-600" />
              Sleep Health Analysis
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
                  <span className="text-sm font-medium text-gray-700">Sleep Disorder Risk</span>
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
                
                <div className="bg-gray-50 rounded-lg p-4">
                  <h3 className="font-semibold text-gray-800 mb-2 flex items-center">
                    <BarChart3 className="w-4 h-4 mr-2" />
                    Key Health Indicators
                  </h3>
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-500">Sleep Duration:</span>
                      <span className="font-medium">{formData.sleep_duration}h</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Sleep Quality:</span>
                      <span className="font-medium">{formData.quality_of_sleep}/10</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Stress Level:</span>
                      <span className="font-medium">{formData.stress_level}/10</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">BMI Category:</span>
                      <span className={`font-medium ${getBmiCategoryColor(formData.bmi_category)}`}>
                        {formData.bmi_category}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Daily Steps:</span>
                      <span className="font-medium">{formData.daily_steps.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Heart Rate:</span>
                      <span className="font-medium">{formData.heart_rate} bpm</span>
                    </div>
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
                    <strong>💤 Sleep Hygiene Tips:</strong> Maintain consistent sleep schedule, 
                    avoid screens before bed, keep bedroom dark and cool, and limit caffeine in evening.
                  </p>
                </div>
                
                <div className="bg-yellow-50 rounded-lg p-3">
                  <p className="text-xs text-yellow-700">
                    <strong>Note:</strong> This analysis is based on sleep patterns and lifestyle factors. 
                    Consult a sleep specialist for persistent sleep issues.
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
                <Moon className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>Enter sleep data and click "Analyze Sleep Health"</p>
                <p className="text-sm mt-2">The SVC model will analyze sleep patterns and detect potential disorders</p>
              </div>
            )}
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default SleepHealthPredictor;