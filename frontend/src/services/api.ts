import axios from 'axios';
import { type DiabetesData, type PredictionResult } from '../types';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Add response interceptor for better error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const healthAPI = {
  checkHealth: () => api.get('/api/health'),
  
  predictDiabetes: (data: DiabetesData): Promise<{ data: PredictionResult }> => 
    api.post('/api/predict/diabetes', data),
  
  predictAsthma: (data: any) => api.post('/api/predict/asthma', data),
  
  predictCardio: (data: any) => api.post('/api/predict/cardio', data),
  
  predictStroke: (data: any) => api.post('/api/predict/stroke', data),
  
  predictHypertension: (data: any) => api.post('/api/predict/hypertension', data),
};

export default api;