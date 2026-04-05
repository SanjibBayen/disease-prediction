import React from 'react';
import { NavLink } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  LayoutDashboard,
  Droplets,
  Activity,
  Heart,
  Brain,
  Moon,
  Stethoscope,
  BarChart3,
  Settings,
  LogOut,
} from 'lucide-react';

const navItems = [
  { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { path: '/diabetes', icon: Droplets, label: 'Diabetes' },
  { path: '/hypertension', icon: Activity, label: 'Hypertension' },
  { path: '/cardiovascular', icon: Heart, label: 'Cardiovascular' },
  { path: '/stroke', icon: Brain, label: 'Stroke' },
  { path: '/asthma', icon: Activity, label: 'Asthma' },
  { path: '/mental-health', icon: Brain, label: 'Mental Health' },
  { path: '/sleep', icon: Moon, label: 'Sleep Health' },
  { path: '/consultant', icon: Stethoscope, label: 'Consultant' },
  
  

];

const Sidebar: React.FC = () => {
  return (
    <div className="fixed left-0 top-0 h-full w-64 bg-gradient-to-b from-gray-900 to-gray-800 text-white shadow-2xl z-50">
      <div className="p-6 border-b border-gray-700">
        <div className="flex items-center justify-center space-x-2">
          <div className="text-3xl">🏥</div>
          <div>
            <h1 className="text-xl font-bold">HealthPredict</h1>
            <p className="text-xs text-gray-400">AI-Powered Health</p>
          </div>
        </div>
      </div>

      <nav className="mt-8 px-4">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center px-4 py-3 my-1 text-gray-300 rounded-xl transition-all duration-200 ${
                isActive
                  ? 'gradient-bg text-white shadow-lg'
                  : 'hover:bg-gray-700 hover:text-white'
              }`
            }
          >
            <item.icon className="w-5 h-5 mr-3" />
            <span className="text-sm font-medium">{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="absolute bottom-0 left-0 right-0 p-6 border-t border-gray-700">
        <div className="flex items-center justify-between">
          <div className="text-xs text-gray-400">
            <p>Version 3.0.0</p>
            <p>© 2025 HealthPredict</p>
          </div>
          <button className="p-2 hover:bg-gray-700 rounded-lg transition-colors">
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;