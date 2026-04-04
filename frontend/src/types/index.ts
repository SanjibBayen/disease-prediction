// Export all types
export interface DiabetesData {
  pregnancies: number;
  glucose: number;
  blood_pressure: number;
  skin_thickness: number;
  insulin: number;
  bmi: number;
  diabetes_pedigree: number;
  age: number;
}

export interface AsthmaData {
  gender_male: number;
  smoking_ex: number;
  smoking_non: number;
  age: number;
  peak_flow: number;
}

export interface CardioData {
  age: number;
  ap_hi: number;
  ap_lo: number;
  cholesterol: number;
  gluc: number;
  smoke: number;
  alco: number;
  active: number;
  weight: number;
}

export interface StrokeData {
  age: number;
  hypertension: number;
  heart_disease: number;
  ever_married: number;
  avg_glucose_level: number;
  bmi: number;
  smoking_status: number;
}

export interface HypertensionData {
  male: number;
  age: number;
  cigsPerDay: number;
  BPMeds: number;
  totChol: number;
  sysBP: number;
  diaBP: number;
  BMI: number;
  heartRate: number;
  glucose: number;
}

export interface PredictionResult {
  success: boolean;
  prediction: number;
  probability: number;
  risk_level: string;
  message: string;
  recommendations: string[];
  timestamp: string;
}

export interface ApiResponse<T = any> {
  data: T;
  message?: string;
  status: number;
}