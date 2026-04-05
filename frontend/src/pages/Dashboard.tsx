import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Activity, Shield, Heart, Brain, Droplets, Moon, Wind,
  AlertCircle, PieChart
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { healthAPI } from '../services/api';
import { PieChart as RePieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';

const Dashboard: React.FC = () => {
  const [healthStatus, setHealthStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [modelsLoaded, setModelsLoaded] = useState(0);
  const [apiStatus, setApiStatus] = useState('loading');
  const [version, setVersion] = useState('3.0.0');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const healthResponse = await healthAPI.checkHealth();
        const healthData = healthResponse.data;
        
        setHealthStatus(healthData);
        setModelsLoaded(healthData.models_loaded || 0);
        setApiStatus(healthData.status || 'healthy');
        setVersion(healthData.version || '3.0.0');
        
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
        setApiStatus('offline');
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, []);

  const features = [
    { path: '/diabetes', icon: Droplets, title: 'Diabetes', description: 'SVC model for diabetes risk prediction', color: 'from-blue-500 to-blue-600', accuracy: '85%' },
    { path: '/hypertension', icon: Activity, title: 'Hypertension', description: 'Extra Trees for BP risk assessment', color: 'from-red-500 to-red-600', accuracy: '82%' },
    { path: '/cardiovascular', icon: Heart, title: 'Heart Disease', description: 'XGBoost cardiovascular prediction', color: 'from-purple-500 to-purple-600', accuracy: '78%' },
    { path: '/stroke', icon: Brain, title: 'Stroke', description: 'Ensemble stroke risk analysis', color: 'from-green-500 to-green-600', accuracy: '80%' },
    { path: '/asthma', icon: Wind, title: 'Asthma', description: 'Random Forest respiratory health', color: 'from-orange-500 to-orange-600', accuracy: '83%' },
    { path: '/mental-health', icon: Brain, title: 'Mental Health', description: 'NLP depression/anxiety assessment', color: 'from-indigo-500 to-indigo-600', accuracy: '82%' },
    { path: '/sleep', icon: Moon, title: 'Sleep Health', description: 'SVC sleep disorder detection', color: 'from-teal-500 to-teal-600', accuracy: '76%' },
  ];

  // Disease distribution data (mock - based on model types)
  const diseaseDistribution = [
    { name: 'Diabetes', value: 1, color: '#3b82f6' },
    { name: 'Hypertension', value: 1, color: '#ef4444' },
    { name: 'Cardiovascular', value: 1, color: '#8b5cf6' },
    { name: 'Mental Health', value: 1, color: '#ec4899' },
    { name: 'Sleep Health', value: 1, color: '#14b8a6' },
    { name: 'Asthma', value: 1, color: '#f59e0b' },
    { name: 'Stroke', value: 1, color: '#10b981' },
  ];

  if (loading) {
    return (
      <div className="flex flex-col justify-center items-center h-96">
        <div className="w-16 h-16 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
        <p className="mt-4 text-gray-500">Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div className="p-6 lg:p-8">
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-3xl lg:text-4xl font-bold gradient-text">Welcome to HealthPredict AI</h1>
        <p className="text-gray-600 mt-2">
          Advanced AI-powered healthcare prediction system with {modelsLoaded} active machine learning models
        </p>
        <div className="flex items-center gap-2 mt-3">
          <div className={`w-2 h-2 rounded-full ${apiStatus === 'healthy' ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></div>
          <span className={`text-sm ${apiStatus === 'healthy' ? 'text-green-600' : 'text-red-600'}`}>
            API Status: {apiStatus === 'healthy' ? 'Operational' : 'Issues Detected'}
          </span>
          <span className="text-gray-400 mx-2">•</span>
          <span className="text-sm text-gray-500">Version {version}</span>
        </div>
      </motion.div>
   {/* Features Grid - Disease Prediction Models */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="mb-8"
      >
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Disease Prediction Models</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <Link
              key={index}
              to={feature.path}
              className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-all duration-300 group hover:-translate-y-1"
            >
              <div className={`w-12 h-12 bg-gradient-to-r ${feature.color} rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                <feature.icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-gray-800 mb-1">{feature.title}</h3>
              <p className="text-gray-500 text-sm mb-3">{feature.description}</p>
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-400">Accuracy: {feature.accuracy}</span>
                <span className="text-primary-600 text-sm font-medium group-hover:underline flex items-center gap-1">
                  Predict <span className="text-lg">→</span>
                </span>
              </div>
            </Link>
          ))}
        </div>
      </motion.div>
      {/* System Status and Disease Distribution Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* System Status */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-xl shadow-lg p-6"
        >
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Shield className="w-5 h-5 text-primary-600" />
            System Status
          </h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <span className="font-medium text-gray-700">API Server</span>
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${apiStatus === 'healthy' ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></div>
                <span className={apiStatus === 'healthy' ? 'text-green-600' : 'text-red-600'}>
                  {apiStatus === 'healthy' ? 'Operational' : 'Issues'}
                </span>
              </div>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <span className="font-medium text-gray-700">ML Models</span>
              <span className="text-green-600 font-medium">{modelsLoaded} Active</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <span className="font-medium text-gray-700">API Version</span>
              <span className="text-gray-600">{version}</span>
            </div>
          </div>
        </motion.div>

        {/* Disease Distribution */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-xl shadow-lg p-6"
        >
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <PieChart className="w-5 h-5 text-primary-600" />
            Disease Distribution
          </h2>
          <div className="flex items-center justify-center">
            <ResponsiveContainer width="100%" height={200}>
              <RePieChart>
                <Pie
                  data={diseaseDistribution}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name }) => name}
                  outerRadius={70}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {diseaseDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </RePieChart>
            </ResponsiveContainer>
          </div>
          <div className="grid grid-cols-2 gap-2 mt-4">
            {diseaseDistribution.map((item) => (
              <div key={item.name} className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }}></div>
                <span className="text-xs text-gray-600">{item.name}</span>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

   
    </div>
  );
};

export default Dashboard;