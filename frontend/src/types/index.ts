export interface PredictionResponse {
  success: boolean;
  prediction: number;
  probability: number;
  risk_level: string;
  message: string;
  recommendations: string[];
  timestamp: string;
}

export interface MentalHealthResponse {
  success: boolean;
  depression_risk: number;
  anxiety_risk: number;
  risk_level: string;
  message: string;
  recommendations: string[];
  timestamp: string;
}

export interface SleepHealthResponse extends PredictionResponse {
  sleep_score: number | null;
  factors_affected: string[] | null;
}

export interface DiabetesInput {
  pregnancies: number;
  glucose: number;
  blood_pressure: number;
  skin_thickness: number;
  insulin: number;
  bmi: number;
  diabetes_pedigree: number;
  age: number;
}

export interface AsthmaInput {
  gender_male: number;
  smoking_ex: number;
  smoking_non: number;
  age: number;
  peak_flow: number;
}

export interface CardioInput {
  active: number;
  age: number;
  alco: number;
  ap_hi: number;
  ap_lo: number;
  cholesterol: number;
  gluc: number;
  smoke: number;
  weight: number;
}

export interface StrokeInput {
  age: number;
  hypertension: number;
  heart_disease: number;
  ever_married: number;
  avg_glucose_level: number;
  bmi: number;
  smoking_status: number;
}

export interface HypertensionInput {
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

export interface SleepInput {
  gender: string;
  age: number;
  occupation: string;
  sleep_duration: number;
  quality_of_sleep: number;
  physical_activity_level: number;
  stress_level: number;
  bmi_category: string;
  blood_pressure: string;
  heart_rate: number;
  daily_steps: number;
}

export interface MentalHealthInput {
  text: string;
}
