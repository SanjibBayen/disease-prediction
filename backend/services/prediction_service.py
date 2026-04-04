"""
Prediction Service - Handles all prediction logic and result formatting
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PredictionService:
    """Service for making predictions and formatting results"""
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
    
    def predict_diabetes(self, data: Dict) -> Dict:
        """Make diabetes prediction"""
        try:
            features = np.array([[
                data['pregnancies'], data['glucose'], data['blood_pressure'],
                data['skin_thickness'], data['insulin'], data['bmi'],
                data['diabetes_pedigree'], data['age']
            ]])
            
            model = self.model_manager.get_model('diabetes')
            if model is None:
                raise ValueError("Diabetes model not loaded")
            
            prediction = int(model.predict(features)[0])
            
            # Get probability
            probability = 0.0
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(features)[0]
                probability = float(proba[1] if prediction == 1 else proba[0])
            else:
                probability = 85.0 if prediction == 1 else 75.0
            
            recommendations = self._get_diabetes_recommendations(data, prediction)
            risk_factors = self._analyze_diabetes_risk_factors(data)
            
            return {
                'prediction': prediction,
                'probability': round(probability * 100, 2),
                'risk_level': self._get_risk_level(probability),
                'message': self._get_prediction_message('diabetes', prediction),
                'recommendations': recommendations,
                'risk_factors': risk_factors,
                'model_accuracy': self.model_manager.get_model_info('diabetes', {}).get('accuracy', 0.85)
            }
        except Exception as e:
            logger.error(f"Diabetes prediction error: {str(e)}")
            raise
    
    def predict_asthma(self, data: Dict) -> Dict:
        """Make asthma prediction"""
        try:
            # Prepare input
            raw_input = np.array([[
                data['gender_male'], data['smoking_ex'], data['smoking_non'],
                data['age'], data['peak_flow']
            ]])
            
            # Apply preprocessing
            preprocessor = self.model_manager.get_preprocessor('asthma')
            if preprocessor:
                processed_input = preprocessor.transform(raw_input)
            else:
                processed_input = raw_input
            
            model = self.model_manager.get_model('asthma')
            if model is None:
                raise ValueError("Asthma model not loaded")
            
            prediction = int(model.predict(processed_input)[0])
            
            # Calculate risk score based on factors
            risk_score = self._calculate_asthma_risk_score(data)
            
            recommendations = self._get_asthma_recommendations(data, prediction)
            risk_factors = self._analyze_asthma_risk_factors(data)
            
            return {
                'prediction': prediction,
                'probability': risk_score,
                'risk_level': self._get_risk_level(risk_score / 100),
                'message': self._get_prediction_message('asthma', prediction),
                'recommendations': recommendations,
                'risk_factors': risk_factors,
                'model_accuracy': self.model_manager.get_model_info('asthma', {}).get('accuracy', 0.83)
            }
        except Exception as e:
            logger.error(f"Asthma prediction error: {str(e)}")
            raise
    
    def predict_cardio(self, data: Dict) -> Dict:
        """Make cardiovascular disease prediction"""
        try:
            features = np.array([[
                data['age'], data['ap_hi'], data['ap_lo'], data['cholesterol'],
                data['gluc'], data['smoke'], data['alco'], data['active'], data['weight']
            ]])
            
            model = self.model_manager.get_model('cardio')
            if model is None:
                raise ValueError("Cardiovascular model not loaded")
            
            prediction = int(model.predict(features)[0])
            
            # Calculate risk score
            risk_score = self._calculate_cardio_risk_score(data)
            
            recommendations = self._get_cardio_recommendations(data, prediction)
            risk_factors = self._analyze_cardio_risk_factors(data)
            
            return {
                'prediction': prediction,
                'probability': risk_score,
                'risk_level': self._get_risk_level(risk_score / 100),
                'message': self._get_prediction_message('cardio', prediction),
                'recommendations': recommendations,
                'risk_factors': risk_factors,
                'model_accuracy': self.model_manager.get_model_info('cardio', {}).get('accuracy', 0.78)
            }
        except Exception as e:
            logger.error(f"Cardiovascular prediction error: {str(e)}")
            raise
    
    def predict_stroke(self, data: Dict) -> Dict:
        """Make stroke prediction"""
        try:
            features = np.array([[
                data['age'], data['hypertension'], data['heart_disease'], 
                data['ever_married'], data['avg_glucose_level'], 
                data['bmi'], data['smoking_status']
            ]])
            
            model = self.model_manager.get_model('stroke')
            if model is None:
                raise ValueError("Stroke model not loaded")
            
            prediction = int(model.predict(features)[0])
            
            # Calculate risk score
            risk_score = self._calculate_stroke_risk_score(data)
            
            recommendations = self._get_stroke_recommendations(data, prediction)
            risk_factors = self._analyze_stroke_risk_factors(data)
            
            return {
                'prediction': prediction,
                'probability': risk_score,
                'risk_level': self._get_risk_level(risk_score / 100),
                'message': self._get_prediction_message('stroke', prediction),
                'recommendations': recommendations,
                'risk_factors': risk_factors,
                'model_accuracy': self.model_manager.get_model_info('stroke', {}).get('accuracy', 0.80)
            }
        except Exception as e:
            logger.error(f"Stroke prediction error: {str(e)}")
            raise
    
    def predict_hypertension(self, data: Dict) -> Dict:
        """Make hypertension prediction"""
        try:
            input_df = pd.DataFrame({
                'male': [data['male']],
                'age': [data['age']],
                'cigsPerDay': [data['cigsPerDay']],
                'BPMeds': [data['BPMeds']],
                'totChol': [data['totChol']],
                'sysBP': [data['sysBP']],
                'diaBP': [data['diaBP']],
                'BMI': [data['BMI']],
                'heartRate': [data['heartRate']],
                'glucose': [data['glucose']]
            })
            
            # Scale features
            preprocessor = self.model_manager.get_preprocessor('hypertension')
            if preprocessor:
                num_cols = ['age', 'cigsPerDay', 'totChol', 'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose']
                input_df[num_cols] = preprocessor.transform(input_df[num_cols])
            
            model = self.model_manager.get_model('hypertension')
            if model is None:
                raise ValueError("Hypertension model not loaded")
            
            prediction = int(model.predict(input_df)[0])
            
            # Get probability
            probability = 0.0
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(input_df)[0]
                probability = float(proba[1] if prediction == 1 else proba[0])
            else:
                probability = 82.0 if prediction == 1 else 75.0
            
            recommendations = self._get_hypertension_recommendations(data, prediction)
            risk_factors = self._analyze_hypertension_risk_factors(data)
            
            return {
                'prediction': prediction,
                'probability': round(probability * 100, 2),
                'risk_level': self._get_risk_level(probability),
                'message': self._get_prediction_message('hypertension', prediction),
                'recommendations': recommendations,
                'risk_factors': risk_factors,
                'model_accuracy': self.model_manager.get_model_info('hypertension', {}).get('accuracy', 0.82)
            }
        except Exception as e:
            logger.error(f"Hypertension prediction error: {str(e)}")
            raise
    
    # ========================================================================
    # Helper Methods for Risk Analysis and Recommendations
    # ========================================================================
    
    def _get_risk_level(self, probability: float) -> str:
        """Convert probability to risk level"""
        if probability < 0.3:
            return "Low"
        elif probability < 0.6:
            return "Moderate"
        else:
            return "High"
    
    def _get_prediction_message(self, disease: str, prediction: int) -> str:
        """Get human-readable prediction message"""
        messages = {
            'diabetes': {0: "No signs of diabetes detected", 1: "High risk of diabetes detected"},
            'asthma': {0: "Low risk of asthma", 1: "High risk of asthma detected"},
            'cardio': {0: "Low risk of cardiovascular disease", 1: "High risk of cardiovascular disease detected"},
            'stroke': {0: "Low risk of stroke", 1: "High risk of stroke detected"},
            'hypertension': {0: "Normal blood pressure range", 1: "High risk of hypertension detected"}
        }
        return messages.get(disease, {}).get(prediction, "Prediction completed")
    
    def _get_diabetes_recommendations(self, data: Dict, prediction: int) -> List[str]:
        """Generate personalized diabetes recommendations"""
        recommendations = []
        
        if prediction == 1:
            recommendations.append("Consult an endocrinologist for proper diabetes management")
            recommendations.append("Monitor blood sugar levels daily using a glucometer")
            recommendations.append("Follow prescribed medication schedule strictly")
        
        if data.get('glucose', 0) > 140:
            recommendations.append("Reduce intake of sugary foods and refined carbohydrates")
            recommendations.append("Consider consulting a nutritionist for meal planning")
        
        if data.get('bmi', 0) > 25:
            recommendations.append("Aim to lose 5-10% of body weight through diet and exercise")
            recommendations.append("Incorporate 30 minutes of moderate exercise daily")
        
        if data.get('age', 0) > 45:
            recommendations.append("Schedule regular diabetes screening every 6 months")
        
        if data.get('blood_pressure', 0) > 140:
            recommendations.append("Monitor blood pressure regularly and reduce sodium intake")
        
        if not recommendations:
            recommendations.append("Continue maintaining a healthy balanced diet")
            recommendations.append("Exercise regularly - at least 150 minutes per week")
            recommendations.append("Get annual health check-ups including blood sugar testing")
        
        return recommendations
    
    def _get_asthma_recommendations(self, data: Dict, prediction: int) -> List[str]:
        """Generate personalized asthma recommendations"""
        recommendations = []
        
        if prediction == 1:
            recommendations.append("Consult a pulmonologist for comprehensive asthma evaluation")
            recommendations.append("Consider pulmonary function testing (spirometry)")
            recommendations.append("Keep rescue inhaler accessible at all times")
        
        if data.get('smoking_ex', 0) == 1 or data.get('smoking_non', 0) == 0:
            recommendations.append("Avoid smoking and second-hand smoke exposure")
        
        if data.get('peak_flow', 0) < 0.5:
            recommendations.append("Monitor peak flow readings daily")
            recommendations.append("Create an asthma action plan with your doctor")
        
        recommendations.append("Identify and avoid personal asthma triggers")
        recommendations.append("Keep home environment dust-free and well-ventilated")
        
        return recommendations
    
    def _get_cardio_recommendations(self, data: Dict, prediction: int) -> List[str]:
        """Generate personalized cardiovascular recommendations"""
        recommendations = []
        
        if prediction == 1:
            recommendations.append("Schedule immediate cardiology consultation")
            recommendations.append("Consider stress test and ECG evaluation")
        
        if data.get('ap_hi', 0) > 140 or data.get('ap_lo', 0) > 90:
            recommendations.append("Monitor blood pressure twice daily")
            recommendations.append("Reduce sodium intake to less than 1500mg per day")
        
        if data.get('cholesterol', 1) > 1:
            recommendations.append("Adopt heart-healthy Mediterranean diet")
            recommendations.append("Include more omega-3 fatty acids in diet")
        
        if data.get('smoke', 0) == 1:
            recommendations.append("Join smoking cessation program")
        
        recommendations.append("Exercise 30-45 minutes daily, 5 days per week")
        recommendations.append("Manage stress through meditation or yoga")
        
        return recommendations
    
    def _get_stroke_recommendations(self, data: Dict, prediction: int) -> List[str]:
        """Generate personalized stroke recommendations"""
        recommendations = []
        
        if prediction == 1:
            recommendations.append("Seek immediate neurological evaluation")
            recommendations.append("Learn FAST warning signs (Face, Arm, Speech, Time)")
        
        if data.get('hypertension', 0) == 1:
            recommendations.append("Strict blood pressure control is essential")
        
        if data.get('avg_glucose_level', 0) > 140:
            recommendations.append("Control blood sugar levels to reduce stroke risk")
        
        recommendations.append("Maintain healthy BMI between 18.5-24.9")
        recommendations.append("Exercise regularly to improve cardiovascular health")
        
        return recommendations
    
    def _get_hypertension_recommendations(self, data: Dict, prediction: int) -> List[str]:
        """Generate personalized hypertension recommendations"""
        recommendations = []
        
        if prediction == 1:
            recommendations.append("Consult cardiologist for BP management plan")
            recommendations.append("Consider 24-hour ambulatory BP monitoring")
        
        if data.get('sysBP', 0) > 140 or data.get('diaBP', 0) > 90:
            recommendations.append("Reduce sodium intake to less than 1500mg daily")
            recommendations.append("Limit alcohol consumption")
        
        if data.get('BMI', 0) > 25:
            recommendations.append("Weight loss of 5-10% can significantly reduce BP")
        
        if data.get('cigsPerDay', 0) > 0:
            recommendations.append("Smoking cessation is critical for BP control")
        
        recommendations.append("Practice DASH diet (rich in fruits, vegetables, low-fat dairy)")
        recommendations.append("Regular aerobic exercise - walking, swimming, cycling")
        
        return recommendations
    
    def _analyze_diabetes_risk_factors(self, data: Dict) -> List[Dict]:
        """Analyze and return diabetes risk factors"""
        risk_factors = []
        
        if data.get('glucose', 0) > 140:
            risk_factors.append({
                'factor': 'Elevated Glucose',
                'value': f"{data['glucose']} mg/dL",
                'risk': 'High',
                'recommendation': 'Monitor blood sugar and reduce sugar intake'
            })
        
        if data.get('bmi', 0) > 25:
            risk_factors.append({
                'factor': 'Overweight/Obese',
                'value': f"BMI {data['bmi']}",
                'risk': 'Moderate',
                'recommendation': 'Weight management through diet and exercise'
            })
        
        if data.get('age', 0) > 45:
            risk_factors.append({
                'factor': 'Age',
                'value': f"{data['age']} years",
                'risk': 'Moderate',
                'recommendation': 'Regular diabetes screening'
            })
        
        return risk_factors
    
    def _analyze_asthma_risk_factors(self, data: Dict) -> List[Dict]:
        """Analyze and return asthma risk factors"""
        risk_factors = []
        
        if data.get('smoking_ex', 0) == 1:
            risk_factors.append({
                'factor': 'Smoking History',
                'value': 'Former Smoker',
                'risk': 'Moderate',
                'recommendation': 'Avoid smoke exposure and monitor symptoms'
            })
        
        if data.get('peak_flow', 0) < 0.5:
            risk_factors.append({
                'factor': 'Reduced Peak Flow',
                'value': f"{data['peak_flow']} L/sec",
                'risk': 'High',
                'recommendation': 'Pulmonary function evaluation recommended'
            })
        
        return risk_factors
    
    def _analyze_cardio_risk_factors(self, data: Dict) -> List[Dict]:
        """Analyze and return cardiovascular risk factors"""
        risk_factors = []
        
        if data.get('ap_hi', 0) > 140:
            risk_factors.append({
                'factor': 'High Systolic BP',
                'value': f"{data['ap_hi']} mmHg",
                'risk': 'High',
                'recommendation': 'Blood pressure management required'
            })
        
        if data.get('cholesterol', 1) > 1:
            risk_factors.append({
                'factor': 'Abnormal Cholesterol',
                'value': 'Above Normal',
                'risk': 'Moderate',
                'recommendation': 'Dietary modification and possible medication'
            })
        
        return risk_factors
    
    def _analyze_stroke_risk_factors(self, data: Dict) -> List[Dict]:
        """Analyze and return stroke risk factors"""
        risk_factors = []
        
        if data.get('hypertension', 0) == 1:
            risk_factors.append({
                'factor': 'Hypertension',
                'value': 'Present',
                'risk': 'High',
                'recommendation': 'Strict blood pressure control'
            })
        
        if data.get('avg_glucose_level', 0) > 140:
            risk_factors.append({
                'factor': 'High Glucose',
                'value': f"{data['avg_glucose_level']} mg/dL",
                'risk': 'Moderate',
                'recommendation': 'Diabetes management to reduce stroke risk'
            })
        
        return risk_factors
    
    def _analyze_hypertension_risk_factors(self, data: Dict) -> List[Dict]:
        """Analyze and return hypertension risk factors"""
        risk_factors = []
        
        if data.get('sysBP', 0) > 140:
            risk_factors.append({
                'factor': 'Elevated Systolic BP',
                'value': f"{data['sysBP']} mmHg",
                'risk': 'High',
                'recommendation': 'Immediate lifestyle modification'
            })
        
        if data.get('BMI', 0) > 25:
            risk_factors.append({
                'factor': 'High BMI',
                'value': f"{data['BMI']}",
                'risk': 'Moderate',
                'recommendation': 'Weight loss program recommended'
            })
        
        return risk_factors
    
    def _calculate_asthma_risk_score(self, data: Dict) -> float:
        """Calculate asthma risk score based on factors"""
        score = 0
        
        if data.get('smoking_ex', 0) == 1:
            score += 20
        
        if data.get('peak_flow', 0) < 0.4:
            score += 30
        elif data.get('peak_flow', 0) < 0.6:
            score += 15
        
        if data.get('age', 0) > 0.7:  # Normalized age > 60
            score += 10
        
        return min(score, 100)
    
    def _calculate_cardio_risk_score(self, data: Dict) -> float:
        """Calculate cardiovascular risk score"""
        score = 0
        
        if data.get('ap_hi', 0) > 140:
            score += 25
        elif data.get('ap_hi', 0) > 130:
            score += 15
        
        if data.get('cholesterol', 1) == 3:
            score += 20
        elif data.get('cholesterol', 1) == 2:
            score += 10
        
        if data.get('smoke', 0) == 1:
            score += 15
        
        if data.get('active', 0) == 0:
            score += 10
        
        return min(score, 100)
    
    def _calculate_stroke_risk_score(self, data: Dict) -> float:
        """Calculate stroke risk score"""
        score = 0
        
        if data.get('hypertension', 0) == 1:
            score += 25
        
        if data.get('heart_disease', 0) == 1:
            score += 20
        
        if data.get('avg_glucose_level', 0) > 140:
            score += 15
        
        if data.get('bmi', 0) > 30:
            score += 10
        
        if data.get('age', 0) > 60:
            score += 15
        elif data.get('age', 0) > 50:
            score += 10
        
        return min(score, 100)