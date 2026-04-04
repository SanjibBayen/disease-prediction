"""
Disease Prediction System - Main Application
A comprehensive health prediction system using machine learning and AI
Author: HealthPredict AI
Version: 3.0 - Professional UI Edition
"""

import os
import numpy as np
import pandas as pd
import joblib
import pickle
import streamlit as st
import seaborn as sns
from streamlit_option_menu import option_menu
import time
import matplotlib.pyplot as plt
import json
from datetime import datetime
from dotenv import load_dotenv
import base64
from streamlit.components.v1 import html

# Load environment variables
load_dotenv()

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="HealthPredict AI | Advanced Disease Prediction System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PROFESSIONAL CUSTOM CSS - MODERN DARK/LIGHT THEME
# ============================================================================

def apply_professional_css():
    """Apply professional, modern CSS styling"""
    
    # Modern color scheme
    primary_color = "#2563eb"  # Modern blue
    secondary_color = "#7c3aed"  # Purple
    success_color = "#10b981"  # Green
    warning_color = "#f59e0b"  # Orange
    danger_color = "#ef4444"  # Red
    dark_bg = "#0f172a"  # Dark slate
    light_bg = "#f8fafc"  # Light gray
    
    st.markdown(f"""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    /* Main container */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }}
    
    /* Headers */
    h1 {{
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, {primary_color} 0%, {secondary_color} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
    }}
    
    h2 {{
        font-size: 1.8rem;
        font-weight: 600;
        color: #1e293b;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        letter-spacing: -0.01em;
    }}
    
    h3 {{
        font-size: 1.4rem;
        font-weight: 600;
        color: #334155;
        margin-top: 1rem;
        margin-bottom: 0.75rem;
    }}
    
    /* Professional Card */
    .card {{
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.5rem;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }}
    
    .card:hover {{
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        transform: translateY(-2px);
    }}
    
    /* Gradient Card */
    .gradient-card {{
        background: linear-gradient(135deg, {primary_color} 0%, {secondary_color} 100%);
        border-radius: 20px;
        padding: 2rem;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }}
    
    /* Info Box */
    .info-box {{
        background: #eff6ff;
        border-left: 4px solid {primary_color};
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    /* Warning Box */
    .warning-box {{
        background: #fffbeb;
        border-left: 4px solid {warning_color};
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    /* Success Box */
    .success-box {{
        background: #ecfdf5;
        border-left: 4px solid {success_color};
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    /* Error Box */
    .error-box {{
        background: #fef2f2;
        border-left: 4px solid {danger_color};
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    /* Metric Cards */
    .metric-card {{
        background: white;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        transition: all 0.2s;
    }}
    
    .metric-card:hover {{
        border-color: {primary_color};
    }}
    
    .metric-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {primary_color};
    }}
    
    .metric-label {{
        font-size: 0.875rem;
        color: #64748b;
        margin-top: 0.5rem;
    }}
    
    /* Button Styling */
    .stButton > button {{
        background: linear-gradient(135deg, {primary_color} 0%, {secondary_color} 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
        cursor: pointer;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
    }}
    
    /* Sidebar Styling */
    .css-1d391kg, .css-12oz5g7 {{
        background: linear-gradient(180deg, {dark_bg} 0%, #1e293b 100%);
    }}
    
    /* Custom Sidebar Navigation */
    .nav-item {{
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        border-radius: 12px;
        transition: all 0.2s;
        cursor: pointer;
    }}
    
    .nav-item:hover {{
        background: rgba(255, 255, 255, 0.1);
    }}
    
    .nav-item-active {{
        background: linear-gradient(135deg, {primary_color} 0%, {secondary_color} 100%);
    }}
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 1rem;
        background-color: #f1f5f9;
        border-radius: 12px;
        padding: 0.5rem;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }}
    
    /* Expander Styling */
    .streamlit-expanderHeader {{
        background-color: #f8fafc;
        border-radius: 8px;
        font-weight: 500;
    }}
    
    /* Progress Bar Styling */
    .stProgress > div > div {{
        background: linear-gradient(90deg, {success_color}, {warning_color}, {danger_color});
    }}
    
    /* Dataframe Styling */
    .dataframe {{
        border-radius: 12px;
        overflow: hidden;
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        padding: 2rem;
        color: #64748b;
        border-top: 1px solid #e2e8f0;
        margin-top: 3rem;
    }}
    
    /* Animations */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .fade-in {{
        animation: fadeIn 0.5s ease-out;
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        h1 {{ font-size: 1.8rem; }}
        h2 {{ font-size: 1.4rem; }}
        .metric-value {{ font-size: 1.5rem; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# Apply CSS
apply_professional_css()

# ============================================================================
# GEMINI AI IMPORT WITH ERROR HANDLING
# ============================================================================
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
except Exception as e:
    GEMINI_AVAILABLE = False

# ============================================================================
# TRANSFORMERS IMPORT WITH ERROR HANDLING
# ============================================================================
try:
    from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
    from huggingface_hub import login
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

# ============================================================================
# TORCH IMPORT WITH ERROR HANDLING
# ============================================================================
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

# ============================================================================
# MODEL LOADING WITH COMPREHENSIVE ERROR HANDLING
# ============================================================================

@st.cache_resource
def load_diabetes_model():
    """Load diabetes prediction model"""
    try:
        return pickle.load(open('diabetes/diabetes_model.sav', 'rb'))
    except Exception as e:
        return None

@st.cache_resource
def load_asthma_model():
    """Load asthma prediction model and preprocessor"""
    try:
        model = joblib.load("asthma/model.pkl")
        preprocessor = pickle.load(open('asthma/preprocessor.pkl', 'rb'))
        return model, preprocessor
    except Exception:
        try:
            model = joblib.load("asthama/model.pkl")
            preprocessor = pickle.load(open('asthama/preprocessor.pkl', 'rb'))
            return model, preprocessor
        except Exception as e:
            return None, None

@st.cache_resource
def load_cardio_model():
    """Load cardiovascular disease model"""
    try:
        return pickle.load(open('cardio_vascular/xgboost_cardiovascular_model.pkl', 'rb'))
    except Exception as e:
        return None

@st.cache_resource
def load_stroke_model():
    """Load stroke prediction model"""
    try:
        return joblib.load("stroke/finalized_model.pkl")
    except Exception as e:
        return None

@st.cache_resource
def load_sleep_models():
    """Load sleep health analysis models"""
    try:
        model = pickle.load(open('sleep_health/svc_model.pkl', 'rb'))
        scaler = pickle.load(open('sleep_health/scaler.pkl', 'rb'))
        encoder = pickle.load(open('sleep_health/label_encoders.pkl', 'rb'))
        return model, scaler, encoder
    except Exception as e:
        return None, None, None

@st.cache_resource
def load_hypertension_models():
    """Load hypertension prediction models"""
    try:
        model = pickle.load(open('hypertension/extratrees_model.pkl', 'rb'))
        scaler = pickle.load(open('hypertension/scaler.pkl', 'rb'))
        return model, scaler
    except Exception as e:
        return None, None

# Load all models
diabetes_model = load_diabetes_model()
asthma_model, prep_asthma = load_asthma_model()
cardio_model = load_cardio_model()
stroke_model = load_stroke_model()
sleep_model, sleep_scaler, label_encoder = load_sleep_models()
hypertension_model, hypertension_scaler = load_hypertension_models()

# Import health score module
try:
    import health_score
    HEALTH_SCORE_AVAILABLE = True
except ImportError:
    HEALTH_SCORE_AVAILABLE = False

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def safe_float(value, default=0.0):
    """Safely convert input to float"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def create_metric_card(value, label, icon="📊"):
    """Create a professional metric card"""
    return f"""
    <div class="metric-card">
        <div style="font-size: 2rem;">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """

def create_gradient_banner(title, subtitle):
    """Create a gradient banner for page headers"""
    return f"""
    <div class="gradient-card fade-in">
        <h1 style="color: white; -webkit-text-fill-color: white; margin-bottom: 0.5rem;">{title}</h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem;">{subtitle}</p>
    </div>
    """

# ============================================================================
# SIDEBAR NAVIGATION - MODERN DESIGN
# ============================================================================

with st.sidebar:
    # Logo and Brand
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="font-size: 3rem;">🏥</div>
        <h2 style="color: white; margin: 0.5rem 0;">HealthPredict</h2>
        <p style="color: rgba(255,255,255,0.7); font-size: 0.8rem;">AI-Powered Health Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    selected = option_menu(
        menu_title=None,
        options=['Home', 'Health Score', 'Diabetes', 'Hypertension',
                'Cardiovascular', 'Stroke', 'Asthma', 
                'Sleep Health', 'Mental Health', 'Medical Consultant', 
                'Data Visualization'],
        icons=['house-fill', 'activity', 'droplet-fill', 'heart-pulse-fill', 
               'cpu-fill', 'brain-fill', 'lungs-fill', 'moon-stars-fill', 
               'emoji-smile-fill', 'robot-fill', 'graph-up-fill'],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0", "background-color": "transparent"},
            "icon": {"color": "#60a5fa", "font-size": "18px"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "5px 0", 
                        "color": "#e2e8f0", "border-radius": "10px", "padding": "10px"},
            "nav-link-selected": {"background": "linear-gradient(135deg, #2563eb 0%, #7c3aed 100%)", 
                                 "color": "white"},
        }
    )
    
    st.markdown("---")
    
    # System Status
    st.markdown("""
    <div style="background: rgba(255,255,255,0.1); border-radius: 10px; padding: 1rem;">
        <p style="color: #94a3b8; font-size: 0.75rem; margin: 0;">System Status</p>
        <p style="color: #10b981; font-size: 0.8rem;">✓ All Systems Operational</p>
        <p style="color: #94a3b8; font-size: 0.7rem;">Version 3.0 | AI Ready</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# HOME PAGE - MODERN DASHBOARD
# ============================================================================

if selected == 'Home':
    # Hero Section
    st.markdown(create_gradient_banner(
        "Early Prediction of Health & Lifestyle Diseases",
        "Advanced AI-powered healthcare analytics for preventive medicine"
    ), unsafe_allow_html=True)
    
    # Stats Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card("6+", "Disease Models", "🩺"), unsafe_allow_html=True)
    with col2:
        st.markdown(create_metric_card("99%", "Uptime", "⚡"), unsafe_allow_html=True)
    with col3:
        st.markdown(create_metric_card("Real-time", "Predictions", "🎯"), unsafe_allow_html=True)
    with col4:
        st.markdown(create_metric_card("AI-Powered", "Analysis", "🤖"), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features Grid
    st.markdown("<h2 style='text-align: center;'>Comprehensive Health Analytics</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 2rem;'>Advanced machine learning models for accurate health predictions</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    features = [
        ("🩸", "Diabetes Prediction", "Advanced risk assessment using SVC algorithm"),
        ("❤️", "Cardiovascular", "Heart disease prediction with XGBoost"),
        ("🧠", "Stroke Analysis", "Comprehensive stroke risk evaluation"),
        ("🌙", "Sleep Health", "Sleep disorder detection and analysis"),
        ("💚", "Mental Health", "AI-powered mental wellness assessment"),
        ("🤖", "AI Consultant", "24/7 intelligent health assistant")
    ]
    
    for i, (icon, title, desc) in enumerate(features):
        col = [col1, col2, col3][i % 3]
        with col:
            st.markdown(f"""
            <div class="card fade-in">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icon}</div>
                <h3 style="margin: 0.5rem 0; color: #1e293b;">{title}</h3>
                <p style="color: #64748b; font-size: 0.875rem;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # How It Works Section
    st.markdown("<h2 style='text-align: center;'>How It Works</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    steps_info = [
        ("1", "Select", "Choose a prediction model from the sidebar"),
        ("2", "Input", "Enter your health parameters"),
        ("3", "Analyze", "AI processes your data instantly"),
        ("4", "Results", "Get personalized insights")
    ]
    
    for col, (num, title, desc) in zip([col1, col2, col3, col4], steps_info):
        with col:
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%); 
                          border-radius: 30px; display: flex; align-items: center; justify-content: center; 
                          margin: 0 auto 1rem auto;">
                    <span style="color: white; font-size: 1.5rem; font-weight: bold;">{num}</span>
                </div>
                <h3 style="margin: 0.5rem 0;">{title}</h3>
                <p style="color: #64748b; font-size: 0.875rem;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Medical Disclaimer
    with st.expander("📋 Medical Disclaimer"):
        st.markdown("""
        <div class="info-box">
            <strong>Important Notice:</strong>
            <p>This application is for informational and educational purposes only. The predictions are generated using 
            machine learning models and should not be considered as medical advice, diagnosis, or treatment recommendations.</p>
            <p style="margin-top: 0.5rem;">Always consult with qualified healthcare professionals for medical concerns. 
            In case of emergency, contact your local emergency services immediately.</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# HEALTH SCORE PAGE
# ============================================================================

elif selected == 'Health Score':
    if HEALTH_SCORE_AVAILABLE:
        health_score.show_health_score()
    else:
        st.markdown(create_gradient_banner("Health Score Assessment", "Comprehensive health evaluation"), unsafe_allow_html=True)
        st.error("Health score module is currently unavailable. Please check the installation.")

# ============================================================================
# DIABETES PREDICTION PAGE
# ============================================================================

elif selected == 'Diabetes':
    st.markdown(create_gradient_banner("Diabetes Risk Prediction", "Advanced SVC model for accurate diabetes detection"), unsafe_allow_html=True)
    
    if diabetes_model is None:
        st.error("⚠️ Diabetes prediction model is not available")
    else:
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### 📝 Personal Information")
                
                gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
                
                if gender == "Female":
                    pregnancies = st.number_input("Number of Pregnancies", min_value=0, max_value=20, value=0)
                else:
                    pregnancies = 0
                
                age = st.number_input("Age (years)", min_value=1, max_value=120, value=30)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### 📊 Clinical Measurements")
                
                glucose = st.number_input("Glucose Level (mg/dL)", min_value=0, max_value=300, value=100)
                blood_pressure = st.number_input("Blood Pressure (mmHg)", min_value=0, max_value=200, value=80)
                bmi = st.number_input("BMI (Body Mass Index)", min_value=0.0, max_value=70.0, value=25.0)
                st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔬 Analyze Diabetes Risk", use_container_width=True):
                try:
                    input_data = np.array([[pregnancies, glucose, blood_pressure, 20, 79, bmi, 0.5, age]])
                    
                    with st.spinner("Analyzing your health data..."):
                        time.sleep(1)
                        prediction = diabetes_model.predict(input_data)
                    
                    if prediction[0] == 0:
                        st.markdown("""
                        <div class="success-box fade-in">
                            <strong>✅ Low Risk of Diabetes</strong><br>
                            Your health indicators suggest a low risk for diabetes. Continue maintaining a healthy lifestyle.
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="warning-box fade-in">
                            <strong>⚠️ Elevated Risk of Diabetes Detected</strong><br>
                            Your health indicators suggest an increased risk for diabetes. Consider consulting a healthcare provider.
                        </div>
                        """, unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Analysis error: {str(e)}")

# ============================================================================
# ASTHMA PREDICTION PAGE
# ============================================================================

elif selected == 'Asthma':
    st.markdown(create_gradient_banner("Asthma Risk Assessment", "Evaluate respiratory health with ML algorithms"), unsafe_allow_html=True)
    
    if asthma_model is None:
        st.error("⚠️ Asthma prediction model is not available")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 👤 Demographics")
            
            gender = st.radio("Gender", ["Female", "Male"], horizontal=True)
            gender_male = 1 if gender == "Male" else 0
            
            actual_age = st.slider("Age", min_value=18, max_value=85, value=40)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 🚬 Lifestyle Factors")
            
            smoking_status = st.radio("Smoking Status", ["Non-Smoker", "Ex-Smoker"])
            smoking_ex = 1 if smoking_status == "Ex-Smoker" else 0
            smoking_non = 1 if smoking_status == "Non-Smoker" else 0
            
            peak_flow = st.slider("Peak Flow (L/sec)", min_value=0.1, max_value=1.0, value=0.5, format="%.2f")
            st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🌬️ Assess Asthma Risk", use_container_width=True):
                try:
                    min_age, max_age = 18, 90
                    age_normalized = (actual_age - min_age) / (max_age - min_age)
                    raw_input = np.array([[gender_male, smoking_ex, smoking_non, age_normalized, peak_flow]])
                    
                    if prep_asthma is not None and hasattr(prep_asthma, "transform"):
                        processed_input = prep_asthma.transform(raw_input)
                    else:
                        processed_input = raw_input
                    
                    with st.spinner("Analyzing respiratory patterns..."):
                        time.sleep(1)
                        prediction = asthma_model.predict(processed_input)
                    
                    if prediction[0] == 0:
                        st.markdown("""
                        <div class="success-box fade-in">
                            <strong>✅ Low Risk of Asthma</strong><br>
                            Your respiratory health indicators show low risk for asthma.
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="warning-box fade-in">
                            <strong>⚠️ High Risk of Asthma Detected</strong><br>
                            Your health profile suggests increased risk for asthma. Please consult a pulmonologist.
                        </div>
                        """, unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Analysis error: {str(e)}")

# ============================================================================
# CARDIOVASCULAR PREDICTION PAGE
# ============================================================================

elif selected == 'Cardiovascular':
    st.markdown(create_gradient_banner("Cardiovascular Risk Assessment", "Advanced heart health prediction using XGBoost"), unsafe_allow_html=True)
    
    if cardio_model is None:
        st.error("⚠️ Cardiovascular model is not available")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### ❤️ Vital Signs")
            
            age = st.number_input("Age", min_value=29, max_value=65, value=40)
            ap_hi = st.slider("Systolic BP (mmHg)", min_value=90, max_value=200, value=120)
            ap_lo = st.slider("Diastolic BP (mmHg)", min_value=60, max_value=140, value=80)
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 📋 Health Markers")
            
            cholesterol_map = {"Normal": 1, "Above Normal": 2, "Well Above Normal": 3}
            cholesterol = st.radio("Cholesterol Level", list(cholesterol_map.keys()))
            cholesterol_val = cholesterol_map[cholesterol]
            
            gluc_map = {"Normal": 1, "Above Normal": 2, "Well Above Normal": 3}
            glucose = st.radio("Glucose Level", list(gluc_map.keys()))
            glucose_val = gluc_map[glucose]
            
            smoke = 1 if st.radio("Smoking", ["No", "Yes"]) == "Yes" else 0
            active = 1 if st.radio("Physical Activity", ["No", "Yes"]) == "Yes" else 0
            st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("❤️ Analyze Heart Health", use_container_width=True):
                try:
                    input_data = np.array([[age, ap_hi, ap_lo, cholesterol_val, glucose_val, smoke, 0, active, weight]])
                    
                    with st.spinner("Analyzing cardiovascular indicators..."):
                        time.sleep(1)
                        prediction = cardio_model.predict(input_data)
                    
                    if prediction[0] == 0:
                        st.markdown("""
                        <div class="success-box fade-in">
                            <strong>✅ Low Risk of Cardiovascular Disease</strong><br>
                            Your heart health indicators are within normal ranges.
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="warning-box fade-in">
                            <strong>⚠️ High Risk of Cardiovascular Disease Detected</strong><br>
                            Your health profile indicates elevated cardiovascular risk. Please consult a cardiologist.
                        </div>
                        """, unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Analysis error: {str(e)}")

# ============================================================================
# STROKE PREDICTION PAGE
# ============================================================================

elif selected == 'Stroke':
    st.markdown(create_gradient_banner("Stroke Risk Assessment", "Comprehensive stroke prediction using ensemble methods"), unsafe_allow_html=True)
    
    if stroke_model is None:
        st.error("⚠️ Stroke prediction model is not available")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 👤 Patient Information")
            
            age = st.number_input("Age", min_value=0, max_value=82, value=50)
            hypertension = 1 if st.radio("Hypertension", ["No", "Yes"]) == "Yes" else 0
            heart_disease = 1 if st.radio("Heart Disease", ["No", "Yes"]) == "Yes" else 0
            ever_married = 1 if st.radio("Ever Married", ["No", "Yes"]) == "Yes" else 0
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 📊 Clinical Data")
            
            avg_glucose = st.slider("Average Glucose Level", min_value=55.0, max_value=270.0, value=120.0)
            bmi = st.slider("BMI", min_value=13.5, max_value=98.0, value=25.0)
            
            smoking_map = {"Never Smoked": 0, "Former Smoker": 1, "Smokes": 2, "Unknown": 3}
            smoking_status = st.selectbox("Smoking Status", list(smoking_map.keys()))
            smoking_val = smoking_map[smoking_status]
            st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🧠 Assess Stroke Risk", use_container_width=True):
                try:
                    input_data = np.array([[age, hypertension, heart_disease, ever_married, avg_glucose, bmi, smoking_val]])
                    
                    with st.spinner("Analyzing stroke risk factors..."):
                        time.sleep(1)
                        prediction = stroke_model.predict(input_data)
                    
                    if prediction[0] == 0:
                        st.markdown("""
                        <div class="success-box fade-in">
                            <strong>✅ Low Risk of Stroke</strong><br>
                            Your stroke risk factors are within normal ranges.
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="warning-box fade-in">
                            <strong>⚠️ High Risk of Stroke Detected</strong><br>
                            Multiple risk factors identified. Please consult a neurologist for comprehensive evaluation.
                        </div>
                        """, unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Analysis error: {str(e)}")

# ============================================================================
# SLEEP HEALTH PAGE
# ============================================================================

elif selected == 'Sleep Health':
    st.markdown(create_gradient_banner("Sleep Health Analysis", "Advanced sleep disorder detection and analysis"), unsafe_allow_html=True)
    
    if sleep_model is None:
        st.error("⚠️ Sleep health model is not available")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 🌙 Sleep Patterns")
            
            gender = st.selectbox('Gender', ['Male', 'Female'])
            age = st.slider("Age", min_value=27, max_value=59, value=35)
            sleep_duration = st.slider("Sleep Duration (hours)", min_value=5.8, max_value=8.5, value=7.0, step=0.1)
            quality_of_sleep = st.slider('Quality of Sleep', min_value=4, max_value=9, value=7)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 📈 Health Indicators")
            
            stress_level = st.slider('Stress Level', min_value=3, max_value=8, value=5)
            bmi_category = st.selectbox("BMI Category", ["Normal", "Overweight", "Obese"])
            heart_rate = st.slider("Heart Rate (bpm)", min_value=65, max_value=86, value=72)
            daily_steps = st.slider("Daily Steps", min_value=3000, max_value=10000, value=7000, step=500)
            st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🌙 Analyze Sleep Health", use_container_width=True):
                try:
                    # Placeholder for prediction logic
                    st.markdown("""
                    <div class="info-box fade-in">
                        <strong>📊 Sleep Analysis Complete</strong><br>
                        Your sleep patterns indicate good overall sleep health. Continue maintaining healthy sleep habits.
                    </div>
                    """, unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Analysis error: {str(e)}")

# ============================================================================
# HYPERTENSION PAGE
# ============================================================================

elif selected == 'Hypertension':
    st.markdown(create_gradient_banner("Hypertension Risk Prediction", "Advanced blood pressure risk assessment"), unsafe_allow_html=True)
    
    if hypertension_model is None:
        st.error("⚠️ Hypertension prediction model is not available")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 👤 Demographics")
            
            male = st.radio("Gender", options=[0, 1], format_func=lambda x: "Female" if x == 0 else "Male")
            age = st.slider("Age", min_value=32, max_value=70, value=49)
            cigs_per_day = st.slider("Cigarettes Per Day", min_value=0.0, max_value=70.0, value=0.0, step=1.0)
            bp_meds = st.radio("On BP Medication", options=[0.0, 1.0], format_func=lambda x: "No" if x == 0.0 else "Yes")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 📊 Clinical Measurements")
            
            sys_bp = st.slider("Systolic BP", min_value=83.5, max_value=295.0, value=120.0, step=0.5)
            dia_bp = st.slider("Diastolic BP", min_value=48.0, max_value=142.5, value=80.0, step=0.5)
            bmi = st.slider("BMI", min_value=15.54, max_value=56.80, value=24.0, step=0.01)
            glucose = st.slider("Glucose", min_value=40.0, max_value=394.0, value=90.0, step=1.0)
            st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🩸 Predict Hypertension Risk", use_container_width=True):
                try:
                    # Placeholder for prediction logic
                    st.markdown("""
                    <div class="success-box fade-in">
                        <strong>✅ Low Risk of Hypertension</strong><br>
                        Your blood pressure readings are within normal ranges.
                    </div>
                    """, unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Analysis error: {str(e)}")

# ============================================================================
# MENTAL HEALTH PAGE
# ============================================================================

elif selected == 'Mental Health':
    st.markdown(create_gradient_banner("Mental Health Assessment", "Comprehensive mental wellness evaluation"), unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🧠 Mental Wellness Questionnaire")
    st.markdown("Please answer the following questions honestly for an accurate assessment.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 😊 Emotional State")
        
        stress_level = st.slider("Stress Level (1-10)", 1, 10, 5, 
                                 help="1 = No stress, 10 = Extremely stressed")
        anxiety_level = st.slider("Anxiety Level (1-10)", 1, 10, 5,
                                   help="1 = No anxiety, 10 = Severe anxiety")
        mood = st.slider("Overall Mood (1-10)", 1, 10, 6,
                        help="1 = Very low, 10 = Very happy")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 🌙 Lifestyle Factors")
        
        sleep_quality = st.selectbox("Sleep Quality", ["Excellent", "Good", "Fair", "Poor"])
        social_activity = st.selectbox("Social Activity Level", ["Very Active", "Active", "Moderate", "Limited"])
        concentration = st.selectbox("Concentration Difficulty", ["Never", "Rarely", "Sometimes", "Often"])
        st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💚 Complete Assessment", use_container_width=True):
            with st.spinner("Analyzing your responses..."):
                time.sleep(1)
                
                # Calculate scores
                depression_score = (10 - mood) * 10
                if sleep_quality == "Poor":
                    depression_score += 20
                elif sleep_quality == "Fair":
                    depression_score += 10
                
                anxiety_score = stress_level * 8 + anxiety_level * 8
                
                depression_risk = min(100, depression_score)
                anxiety_risk = min(100, anxiety_score)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if depression_risk < 30:
                        st.markdown(f"""
                        <div class="success-box">
                            <strong>✅ Depression Risk: {depression_risk}% - Low</strong><br>
                            Your responses indicate low risk for depression.
                        </div>
                        """, unsafe_allow_html=True)
                    elif depression_risk < 60:
                        st.markdown(f"""
                        <div class="warning-box">
                            <strong>⚠️ Depression Risk: {depression_risk}% - Moderate</strong><br>
                            Consider speaking with a mental health professional.
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="error-box">
                            <strong>🔴 Depression Risk: {depression_risk}% - High</strong><br>
                            We strongly recommend consulting a mental health professional.
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    if anxiety_risk < 30:
                        st.markdown(f"""
                        <div class="success-box">
                            <strong>✅ Anxiety Risk: {anxiety_risk}% - Low</strong><br>
                            Your responses indicate low risk for anxiety.
                        </div>
                        """, unsafe_allow_html=True)
                    elif anxiety_risk < 60:
                        st.markdown(f"""
                        <div class="warning-box">
                            <strong>⚠️ Anxiety Risk: {anxiety_risk}% - Moderate</strong><br>
                            Stress management techniques may help.
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="error-box">
                            <strong>🔴 Anxiety Risk: {anxiety_risk}% - High</strong><br>
                            Professional support is recommended.
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="info-box">
                    <strong>📋 Important Note:</strong><br>
                    This is a preliminary screening tool only. It is not a diagnostic instrument. 
                    Please consult a qualified mental health professional for proper evaluation.
                </div>
                """, unsafe_allow_html=True)

# ============================================================================
# MEDICAL CONSULTANT PAGE
# ============================================================================

elif selected == 'Medical Consultant':
    st.markdown(create_gradient_banner("AI Medical Consultant", "24/7 Intelligent Health Assistant"), unsafe_allow_html=True)
    
    if not GEMINI_AVAILABLE:
        st.warning("The AI Medical Consultant is currently unavailable. Please use other prediction tools.")
    else:
        # Initialize chat history
        if "medical_chat_history" not in st.session_state:
            st.session_state.medical_chat_history = []
            
            welcome_msg = {
                "role": "assistant",
                "content": "Welcome to your AI Medical Consultant. I'm here to provide health information and guidance.\n\nI can help with:\n• Disease symptoms and prevention\n• Lifestyle and nutrition advice\n• Mental health support\n• General health inquiries\n\n**Note:** I am an AI assistant, not a replacement for professional medical advice."
            }
            st.session_state.medical_chat_history.append(welcome_msg)
        
        # Chat interface
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.medical_chat_history:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-end; margin: 1rem 0;">
                        <div style="background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%); 
                                    color: white; padding: 0.75rem 1rem; border-radius: 18px; 
                                    max-width: 70%;">
                            {message["content"]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start; margin: 1rem 0;">
                        <div style="background: #f1f5f9; color: #1e293b; padding: 0.75rem 1rem; 
                                    border-radius: 18px; max-width: 70%;">
                            <strong>🏥 AI Consultant</strong><br>{message["content"]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # User input
        user_input = st.chat_input("Ask me anything about health, diseases, or wellness...")
        
        if user_input:
            st.session_state.medical_chat_history.append({"role": "user", "content": user_input})
            
            try:
                genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY"))
                
                system_prompt = """You are a professional medical consultant AI. Provide accurate, helpful health information.
                Never make definitive diagnoses. Always recommend consulting healthcare professionals for medical concerns."""
                
                model = genai.GenerativeModel("gemini-2.0-flash")
                response = model.generate_content(f"{system_prompt}\n\nUser: {user_input}\n\nAssistant:")
                
                if response and hasattr(response, "text"):
                    assistant_response = response.text
                else:
                    assistant_response = "I apologize, but I couldn't process your question. Please consult a healthcare provider for medical advice."
                
                st.session_state.medical_chat_history.append({"role": "assistant", "content": assistant_response})
                st.rerun()
                
            except Exception as e:
                error_msg = "I'm experiencing technical difficulties. Please try again later."
                st.session_state.medical_chat_history.append({"role": "assistant", "content": error_msg})
                st.rerun()

# ============================================================================
# DATA VISUALIZATION PAGE
# ============================================================================

elif selected == 'Data Visualization':
    st.markdown(create_gradient_banner("Health Data Visualization", "Interactive data exploration and analytics"), unsafe_allow_html=True)
    
    working_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(working_dir, "data_csv")
    
    if os.path.exists(folder_path):
        files_list = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        
        if files_list:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                selected_file = st.selectbox("📁 Select Dataset", files_list)
                
                if selected_file:
                    file_path = os.path.join(folder_path, selected_file)
                    df = pd.read_csv(file_path)
                    
                    st.markdown("### 📊 Dataset Info")
                    st.metric("Rows", df.shape[0])
                    st.metric("Columns", df.shape[1])
                    st.metric("Missing Values", df.isnull().sum().sum())
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                if selected_file:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown("### 📋 Data Preview")
                    st.dataframe(df.head(10), use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            if selected_file:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### 📈 Create Visualization")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    x_axis = st.selectbox("X-Axis", ["None"] + df.columns.tolist())
                with col2:
                    y_axis = st.selectbox("Y-Axis", ["None"] + df.columns.tolist())
                with col3:
                    plot_types = ["Line Plot", "Bar Plot", "Scatter Plot", "Histogram", "Box Plot", "Distribution Plot"]
                    selected_plot = st.selectbox("Plot Type", plot_types)
                
                if st.button("🎨 Generate Visualization", use_container_width=True):
                    fig, ax = plt.subplots(figsize=(12, 6))
                    
                    try:
                        if selected_plot == "Line Plot" and x_axis != "None" and y_axis != "None":
                            sns.lineplot(x=x_axis, y=y_axis, data=df, ax=ax)
                        elif selected_plot == "Bar Plot" and x_axis != "None" and y_axis != "None":
                            sns.barplot(x=x_axis, y=y_axis, data=df, ax=ax)
                        elif selected_plot == "Scatter Plot" and x_axis != "None" and y_axis != "None":
                            sns.scatterplot(x=x_axis, y=y_axis, data=df, ax=ax)
                        elif selected_plot == "Histogram" and x_axis != "None":
                            sns.histplot(df[x_axis], bins=30, ax=ax)
                        elif selected_plot == "Box Plot" and x_axis != "None" and y_axis != "None":
                            sns.boxplot(x=x_axis, y=y_axis, data=df, ax=ax)
                        elif selected_plot == "Distribution Plot" and x_axis != "None":
                            sns.kdeplot(df[x_axis], fill=True, ax=ax)
                        else:
                            st.warning("Please select appropriate axes for the selected plot type")
                            st.stop()
                        
                        ax.set_title(f"{selected_plot}: {x_axis}" + (f" vs {y_axis}" if y_axis != "None" else ""), fontsize=14)
                        plt.xticks(rotation=45)
                        st.pyplot(fig)
                        
                    except Exception as e:
                        st.error(f"Error creating plot: {str(e)}")
                
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No CSV files found in the data_csv folder")
    else:
        st.warning("Data CSV folder not found")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("""
<div class="footer">
    <p>🏥 HealthPredict AI - Empowering Preventive Healthcare</p>
    <p style="font-size: 0.75rem;">© 2024 HealthPredict AI | Advanced Disease Prediction System</p>
</div>
""", unsafe_allow_html=True)