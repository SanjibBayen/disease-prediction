import axios from 'axios';
import { 
  DiabetesInput, AsthmaInput, CardioInput, StrokeInput, 
  HypertensionInput, SleepInput, MentalHealthInput,
  PredictionResponse, MentalHealthResponse, SleepHealthResponse
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

export const predictionService = {
  predictDiabetes: async (data: DiabetesInput): Promise<PredictionResponse> => {
    const response = await api.post('/api/predict/diabetes', data);
                                     
    return response.data;
  },
  predictAsthma: async (data: AsthmaInput): Promise<PredictionResponse> => {
    const response = await api.post('/api/predict/asthma', data);
    return response.data;
  },
  predictCardio: async (data: CardioInput): Promise<PredictionResponse> => {
    const response = await api.post('/api/predict/cardio', data);
    return response.data;
  },
  predictStroke: async (data: StrokeInput): Promise<PredictionResponse> => {
    const response = await api.post('/api/predict/stroke', data);
    return response.data;
  },
  predictHypertension: async (data: HypertensionInput): Promise<PredictionResponse> => {
    const response = await api.post('/api/predict/hypertension', data);
    return response.data;
  },
  predictSleep: async (data: SleepInput): Promise<SleepHealthResponse> => {
    const response = await api.post('/api/predict/sleep', data);
    return response.data;
  },
  predictMentalHealth: async (data: MentalHealthInput): Promise<MentalHealthResponse> => {
    const response = await api.post('/api/predict/mental-health', data);
    return response.data;
  },
  checkHealth: async () => {
    const response = await api.get('/api/health');
    //                                 ^^^^ ADD THIS
    return response.data;
  }
};