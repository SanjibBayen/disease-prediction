import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Activity, TrendingUp, Users, Clock, Shield } from 'lucide-react';
import { healthAPI } from '../services/api';

const Dashboard: React.FC = () => {
  const [healthStatus, setHealthStatus] = useState<string>('loading');
  const [stats] = useState({
    totalPredictions: 1247,
    activeUsers: 892,
    avgResponseTime: 1.2,
    accuracy: 94.5,
  });

  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const response = await healthAPI.checkHealth();
      setHealthStatus(response.data.status);
    } catch (error) {
      setHealthStatus('unhealthy');
    }
  };

  const statCards = [
    { icon: Activity, label: 'Total Predictions', value: stats.totalPredictions, trend: '+12%', color: 'text-blue-600' },
    { icon: Users, label: 'Active Users', value: stats.activeUsers, trend: '+8%', color: 'text-green-600' },
    { icon: Clock, label: 'Avg Response', value: `${stats.avgResponseTime}s`, trend: '-0.3s', color: 'text-purple-600' },
    { icon: TrendingUp, label: 'Accuracy', value: `${stats.accuracy}%`, trend: '+2.5%', color: 'text-orange-600' },
  ];

  const features = [
    { name: 'Diabetes Prediction', icon: '🩸', accuracy: '94%', models: 'SVC' },
    { name: 'Heart Disease', icon: '❤️', accuracy: '92%', models: 'XGBoost' },
    { name: 'Stroke Risk', icon: '🧠', accuracy: '89%', models: 'Ensemble' },
    { name: 'Hypertension', icon: '💓', accuracy: '91%', models: 'Extra Trees' },
  ];

  return (
    <div className="p-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold gradient-text">Welcome back, Doctor</h1>
        <p className="text-gray-600 mt-1">Here's what's happening with your health predictions today.</p>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statCards.map((stat, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow"
          >
            <div className="flex items-center justify-between mb-4">
              <div className={`p-3 rounded-lg bg-opacity-10 ${stat.color} bg-current`}>
                <stat.icon className={`w-6 h-6 ${stat.color}`} />
              </div>
              <span className={`text-sm font-medium ${stat.trend.startsWith('+') ? 'text-green-600' : 'text-red-600'}`}>
                {stat.trend}
              </span>
            </div>
            <h3 className="text-2xl font-bold text-gray-800">{stat.value}</h3>
            <p className="text-gray-600 text-sm mt-1">{stat.label}</p>
          </motion.div>
        ))}
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-white rounded-xl shadow-lg p-6"
        >
          <h2 className="text-xl font-semibold mb-4">Available Predictions</h2>
          <div className="space-y-4">
            {features.map((feature, idx) => (
              <div key={idx} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">{feature.icon}</span>
                  <div>
                    <p className="font-medium text-gray-800">{feature.name}</p>
                    <p className="text-xs text-gray-500">Model: {feature.models}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm font-semibold text-green-600">Accuracy: {feature.accuracy}</p>
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-white rounded-xl shadow-lg p-6"
        >
          <h2 className="text-xl font-semibold mb-4">System Status</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <Shield className="w-5 h-5 text-primary-600" />
                <span className="font-medium">API Server</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className={`w-2 h-2 rounded-full ${healthStatus === 'healthy' ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></div>
                <span className={healthStatus === 'healthy' ? 'text-green-600' : 'text-red-600'}>
                  {healthStatus === 'healthy' ? 'Operational' : 'Issues'}
                </span>
              </div>
            </div>
            
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <Activity className="w-5 h-5 text-primary-600" />
                <span className="font-medium">ML Models</span>
              </div>
              <span className="text-green-600">6 Active</span>
            </div>
            
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <TrendingUp className="w-5 h-5 text-primary-600" />
                <span className="font-medium">Uptime</span>
              </div>
              <span className="text-green-600">99.9%</span>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Quick Action */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="gradient-bg rounded-xl p-8 text-white"
      >
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-2">Ready for a prediction?</h2>
            <p className="opacity-90">Select a disease from the sidebar to get started</p>
          </div>
          <Shield className="w-16 h-16 opacity-50" />
        </div>
      </motion.div>
    </div>
  );
};

export default Dashboard;