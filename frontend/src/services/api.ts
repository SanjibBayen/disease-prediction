import axios from 'axios';
import { 
  DiabetesData, AsthmaData, CardioData, StrokeData, HypertensionData,
  PredictionResult, HealthCheckResponse, MentalHealthResponse, SleepData
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const healthAPI = {
  checkHealth: (): Promise<{ data: HealthCheckResponse }> => api.get('/api/health'),
  
  predictDiabetes: (data: DiabetesData): Promise<{ data: PredictionResult }> => 
    api.post('/api/predict/diabetes', data),
  
  predictAsthma: (data: AsthmaData): Promise<{ data: PredictionResult }> => 
    api.post('/api/predict/asthma', data),
  
  predictCardio: (data: CardioData): Promise<{ data: PredictionResult }> => 
    api.post('/api/predict/cardio', data),
  
  predictStroke: (data: StrokeData): Promise<{ data: PredictionResult }> => 
    api.post('/api/predict/stroke', data),
  
  predictHypertension: (data: HypertensionData): Promise<{ data: PredictionResult }> => 
    api.post('/api/predict/hypertension', data),
  
  predictMentalHealth: (text: string): Promise<{ data: MentalHealthResponse }> => 
    api.post('/api/predict/mental-health', { text }),
  
  predictSleep: (data: SleepData): Promise<{ data: PredictionResult }> => 
    api.post('/api/predict/sleep', data),
};

export default api;