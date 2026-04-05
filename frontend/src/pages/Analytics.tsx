import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { 
  BarChart3, TrendingUp, PieChart, LineChart, Activity, 
  Calendar, Users, Brain, Heart, Droplets, Wind, Moon,
  Shield, Download, RefreshCw
} from 'lucide-react';
import {
  LineChart as ReLineChart,
  Line,
  BarChart as ReBarChart,
  Bar,
  PieChart as RePieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from 'recharts';
import { useApi } from '../hooks/useApi';
import api from '../services/api';
import LoadingSpinner from '../components/Common/LoadingSpinner';

interface AnalyticsData {
  daily_predictions: any[];
  disease_distribution: any[];
  risk_distribution: any[];
  model_accuracy: any[];
  age_distribution: any[];
  total_predictions: number;
  average_daily: number;
}

const Analytics: React.FC = () => {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState(30);
  const [selectedDisease, setSelectedDisease] = useState<string | null>(null);
  const [trendsData, setTrendsData] = useState<any[]>([]);

  useEffect(() => {
    fetchAnalytics();
    fetchTrends();
  }, [timeRange, selectedDisease]);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const response = await api.get(`/api/analytics/predictions-summary?days=${timeRange}`);
      setData(response.data);
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchTrends = async () => {
    try {
      const url = selectedDisease 
        ? `/api/analytics/trends?disease=${selectedDisease}`
        : '/api/analytics/trends';
      const response = await api.get(url);
      setTrendsData(response.data.trends);
    } catch (error) {
      console.error('Failed to fetch trends:', error);
    }
  };

  const COLORS = {
    diabetes: '#3b82f6',
    hypertension: '#ef4444',
    cardiovascular: '#8b5cf6',
    stroke: '#10b981',
    asthma: '#f59e0b',
    sleep: '#6366f1',
    mental_health: '#ec4899',
  };

  const riskColors = ['#10b981', '#f59e0b', '#ef4444'];

  if (loading) {
    return (
      <div className="flex justify-center items-center h-96">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

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
              <h1 className="text-3xl font-bold mb-2">Analytics Dashboard</h1>
              <p className="opacity-90">Real-time insights and predictions analytics</p>
              <div className="flex gap-4 mt-3">
                <span className="text-sm bg-white/20 px-3 py-1 rounded-full">
                  Total Predictions: {data?.total_predictions?.toLocaleString() || 0}
                </span>
                <span className="text-sm bg-white/20 px-3 py-1 rounded-full">
                  Avg Daily: {data?.average_daily || 0}
                </span>
              </div>
            </div>
            <BarChart3 className="w-16 h-16 opacity-50" />
          </div>
        </div>

        {/* Time Range Selector */}
        <div className="bg-white rounded-xl shadow-lg p-4 mb-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <span className="text-sm font-medium text-gray-700">Time Range:</span>
              <div className="flex gap-2">
                {[7, 30, 90, 365].map((days) => (
                  <button
                    key={days}
                    onClick={() => setTimeRange(days)}
                    className={`px-3 py-1 rounded-lg text-sm font-medium transition-all ${
                      timeRange === days
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {days === 7 ? 'Week' : days === 30 ? 'Month' : days === 90 ? 'Quarter' : 'Year'}
                  </button>
                ))}
              </div>
            </div>
            <button
              onClick={() => { fetchAnalytics(); fetchTrends(); }}
              className="flex items-center gap-2 px-3 py-1 text-sm text-gray-600 hover:text-primary-600 transition-colors"
            >
              <RefreshCw className="w-4 h-4" />
              Refresh
            </button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-blue-100 rounded-lg">
                <Activity className="w-6 h-6 text-blue-600" />
              </div>
              <span className="text-2xl font-bold text-blue-600">{data?.total_predictions?.toLocaleString() || 0}</span>
            </div>
            <h3 className="text-gray-600 text-sm">Total Predictions</h3>
          </div>
          
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-green-100 rounded-lg">
                <TrendingUp className="w-6 h-6 text-green-600" />
              </div>
              <span className="text-2xl font-bold text-green-600">{data?.average_daily || 0}</span>
            </div>
            <h3 className="text-gray-600 text-sm">Avg Daily Predictions</h3>
          </div>
          
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-purple-100 rounded-lg">
                <Users className="w-6 h-6 text-purple-600" />
              </div>
              <span className="text-2xl font-bold text-purple-600">7</span>
            </div>
            <h3 className="text-gray-600 text-sm">Active Models</h3>
          </div>
          
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-orange-100 rounded-lg">
                <Shield className="w-6 h-6 text-orange-600" />
              </div>
              <span className="text-2xl font-bold text-orange-600">81.5%</span>
            </div>
            <h3 className="text-gray-600 text-sm">Avg Model Accuracy</h3>
          </div>
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Daily Predictions Line Chart */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <LineChart className="w-5 h-5 mr-2 text-primary-600" />
              Daily Prediction Trends
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <ReLineChart data={data?.daily_predictions || []}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="total" stroke="#3b82f6" strokeWidth={2} name="Total" />
                <Line type="monotone" dataKey="diabetes" stroke="#3b82f6" strokeWidth={1} name="Diabetes" />
                <Line type="monotone" dataKey="hypertension" stroke="#ef4444" strokeWidth={1} name="Hypertension" />
                <Line type="monotone" dataKey="mental_health" stroke="#ec4899" strokeWidth={1} name="Mental Health" />
              </ReLineChart>
            </ResponsiveContainer>
          </div>

          {/* Disease Distribution Pie Chart */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <PieChart className="w-5 h-5 mr-2 text-primary-600" />
              Disease Distribution
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <RePieChart>
                <Pie
                  data={data?.disease_distribution || []}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {(data?.disease_distribution || []).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </RePieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Risk Distribution Bar Chart */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <BarChart3 className="w-5 h-5 mr-2 text-primary-600" />
              Risk Level Distribution
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <ReBarChart data={data?.risk_distribution || []}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#8884d8">
                  {(data?.risk_distribution || []).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={riskColors[index % riskColors.length]} />
                  ))}
                </Bar>
              </ReBarChart>
            </ResponsiveContainer>
          </div>

          {/* Model Accuracy Bar Chart */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <TrendingUp className="w-5 h-5 mr-2 text-primary-600" />
              Model Accuracy
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <ReBarChart data={data?.model_accuracy || []} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" domain={[60, 100]} />
                <YAxis type="category" dataKey="model" width={100} />
                <Tooltip />
                <Bar dataKey="accuracy" fill="#3b82f6" name="Accuracy (%)">
                  {(data?.model_accuracy || []).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color || '#3b82f6'} />
                  ))}
                </Bar>
              </ReBarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Prediction Trends by Disease */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold flex items-center">
                <TrendingUp className="w-5 h-5 mr-2 text-primary-600" />
                Prediction Trends
              </h2>
              <select
                value={selectedDisease || ''}
                onChange={(e) => setSelectedDisease(e.target.value || null)}
                className="px-3 py-1 border border-gray-300 rounded-lg text-sm"
              >
                <option value="">All Diseases</option>
                <option value="diabetes">Diabetes</option>
                <option value="hypertension">Hypertension</option>
                <option value="cardiovascular">Cardiovascular</option>
                <option value="stroke">Stroke</option>
                <option value="asthma">Asthma</option>
                <option value="sleep">Sleep Health</option>
                <option value="mental_health">Mental Health</option>
              </select>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <ReLineChart data={trendsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                {trendsData[0] && Object.keys(trendsData[0]).map((key) => {
                  if (key === 'month') return null;
                  return (
                    <Line
                      key={key}
                      type="monotone"
                      dataKey={key}
                      stroke={COLORS[key as keyof typeof COLORS] || '#8884d8'}
                      strokeWidth={2}
                      name={key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    />
                  );
                })}
              </ReLineChart>
            </ResponsiveContainer>
          </div>

          {/* Age Distribution */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <Users className="w-5 h-5 mr-2 text-primary-600" />
              Age Distribution
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <ReBarChart data={data?.age_distribution || []}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="range" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#8b5cf6" name="Number of Patients" />
              </ReBarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Export Button */}
        <div className="flex justify-end">
          <button
            onClick={() => {
              // Export data as JSON
              const dataStr = JSON.stringify(data, null, 2);
              const blob = new Blob([dataStr], { type: 'application/json' });
              const url = URL.createObjectURL(blob);
              const a = document.createElement('a');
              a.href = url;
              a.download = `analytics_${new Date().toISOString().split('T')[0]}.json`;
              a.click();
              URL.revokeObjectURL(url);
            }}
            className="flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            <Download className="w-4 h-4" />
            Export Analytics Data
          </button>
        </div>
      </motion.div>
    </div>
  );
};

export default Analytics;