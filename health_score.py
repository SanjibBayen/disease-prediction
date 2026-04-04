"""
Health Score Assessment Module
This module provides a comprehensive health risk assessment through a multi-step questionnaire.
It calculates risks for various diseases and provides personalized recommendations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import json
import os

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize all session state variables needed for the health assessment."""
    
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    
    if 'assessment_data' not in st.session_state:
        st.session_state.assessment_data = {}
    
    if 'results_calculated' not in st.session_state:
        st.session_state.results_calculated = False
    
    if 'risk_data' not in st.session_state:
        st.session_state.risk_data = []
    
    if 'health_score' not in st.session_state:
        st.session_state.health_score = 0
    
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []
    
    if 'assessment_history' not in st.session_state:
        st.session_state.assessment_history = []


# ============================================================================
# ASSESSMENT STEPS DEFINITION
# ============================================================================

steps = [
    {
        "title": "Basic Information", 
        "fields": ["age", "gender", "height", "weight"],
        "description": "Please provide your basic demographic information."
    },
    {
        "title": "Lifestyle Habits", 
        "fields": ["smoking_status", "alcohol_consumption", "physical_activity", "diet_type"],
        "description": "Tell us about your daily lifestyle choices."
    },
    {
        "title": "Medical History", 
        "fields": ["family_history_diabetes", "family_history_heart_disease", 
                   "family_history_hypertension", "previous_diagnoses"],
        "description": "Information about your personal and family medical history."
    },
    {
        "title": "Vital Signs", 
        "fields": ["systolic_bp", "diastolic_bp", "resting_heart_rate"],
        "description": "Enter your latest vital sign measurements."
    },
    {
        "title": "Mental Health Assessment", 
        "fields": ["stress_level", "sleep_quality", "sleep_duration"],
        "description": "Information about your mental wellbeing and sleep patterns."
    },
    {
        "title": "Nutrition", 
        "fields": ["daily_water_intake", "daily_fruit_veg_servings"],
        "description": "Tell us about your daily nutrition habits."
    },
    {
        "title": "Body Composition", 
        "fields": ["waist_circumference", "body_fat_percentage"],
        "description": "Optional measurements for more accurate assessment."
    },
    {
        "title": "Additional Health Information", 
        "fields": ["family_history_asthma", "family_history_obesity", 
                   "family_history_depression", "allergies", 
                   "chronic_pain", "mental_health_history"],
        "description": "Any additional health information you'd like to share."
    }
]


# ============================================================================
# RISK CALCULATION FUNCTIONS
# ============================================================================

def calculate_bmi(weight, height_cm):
    """
    Calculate Body Mass Index (BMI)
    
    Parameters:
    weight (float): Weight in kilograms
    height_cm (float): Height in centimeters
    
    Returns:
    float: Calculated BMI value
    """
    if height_cm <= 0 or weight <= 0:
        return 0
    height_m = height_cm / 100
    bmi = weight / (height_m * height_m)
    return round(bmi, 1)


def get_bmi_category(bmi):
    """
    Get BMI category based on standard WHO classification
    
    Parameters:
    bmi (float): BMI value
    
    Returns:
    str: BMI category
    """
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def calculate_diabetes_risk(data):
    """Calculate risk score for diabetes based on user data."""
    risk = 0
    
    # Age factor
    if data.get("age", 0) > 45:
        risk += 10
    elif data.get("age", 0) > 35:
        risk += 5
    
    # BMI factor
    bmi = data.get("bmi", 0)
    if bmi > 30:
        risk += 15
    elif bmi > 25:
        risk += 8
    
    # Family history
    if data.get("family_history_diabetes", False):
        risk += 15
    
    # Physical activity
    activity = data.get("physical_activity", "")
    if activity == "sedentary":
        risk += 10
    elif activity == "light":
        risk += 5
    
    # Previous diagnoses
    prev_diagnoses = data.get("previous_diagnoses", "").lower()
    if "diabetes" in prev_diagnoses or "prediabetes" in prev_diagnoses:
        risk += 20
    
    return min(risk, 100)


def calculate_heart_disease_risk(data):
    """Calculate risk score for heart disease based on user data."""
    risk = 0
    
    # Age factor
    if data.get("age", 0) > 55:
        risk += 10
    elif data.get("age", 0) > 45:
        risk += 5
    
    # Blood pressure factor
    systolic = data.get("systolic_bp", 0)
    diastolic = data.get("diastolic_bp", 0)
    if systolic > 140 or diastolic > 90:
        risk += 15
    elif systolic > 130 or diastolic > 85:
        risk += 8
    
    # Family history
    if data.get("family_history_heart_disease", False):
        risk += 15
    
    # Smoking status
    if data.get("smoking_status", "") == "current":
        risk += 15
    elif data.get("smoking_status", "") == "former":
        risk += 5
    
    # Physical activity
    if data.get("physical_activity", "") == "sedentary":
        risk += 10
    
    # BMI factor
    if data.get("bmi", 0) > 30:
        risk += 8
    
    return min(risk, 100)


def calculate_hypertension_risk(data):
    """Calculate risk score for hypertension based on user data."""
    risk = 0
    
    # Blood pressure factor
    systolic = data.get("systolic_bp", 0)
    diastolic = data.get("diastolic_bp", 0)
    if systolic > 140 or diastolic > 90:
        risk += 25
    elif systolic > 130 or diastolic > 85:
        risk += 15
    
    # Family history
    if data.get("family_history_hypertension", False):
        risk += 15
    
    # Alcohol consumption
    alcohol = data.get("alcohol_consumption", "")
    if alcohol == "heavy":
        risk += 10
    elif alcohol == "moderate":
        risk += 5
    
    # BMI factor
    if data.get("bmi", 0) > 30:
        risk += 10
    elif data.get("bmi", 0) > 25:
        risk += 5
    
    # Age factor
    if data.get("age", 0) > 60:
        risk += 10
    
    return min(risk, 100)


def calculate_obesity_risk(data):
    """Calculate risk score for obesity based on user data."""
    risk = 0
    
    # BMI factor
    bmi = data.get("bmi", 0)
    if bmi > 35:
        risk += 35
    elif bmi > 30:
        risk += 25
    elif bmi > 25:
        risk += 10
    
    # Physical activity
    if data.get("physical_activity", "") == "sedentary":
        risk += 15
    elif data.get("physical_activity", "") == "light":
        risk += 8
    
    # Family history
    if data.get("family_history_obesity", False):
        risk += 10
    
    # Waist circumference
    waist = data.get("waist_circumference", 0)
    if waist > 102:  # Men > 102cm, Women > 88cm indicates high risk
        risk += 10
    elif waist > 88:
        risk += 5
    
    return min(risk, 100)


def calculate_asthma_risk(data):
    """Calculate risk score for asthma based on user data."""
    risk = 0
    
    # Family history
    if data.get("family_history_asthma", False):
        risk += 25
    
    # Smoking status
    if data.get("smoking_status", "") == "current":
        risk += 15
    elif data.get("smoking_status", "") == "former":
        risk += 8
    
    # Allergies
    allergies = data.get("allergies", "").lower()
    if "pollen" in allergies or "dust" in allergies or "mold" in allergies:
        risk += 10
    
    # Previous diagnoses
    prev_diagnoses = data.get("previous_diagnoses", "").lower()
    if "asthma" in prev_diagnoses or "copd" in prev_diagnoses:
        risk += 20
    
    return min(risk, 100)


def calculate_depression_risk(data):
    """Calculate risk score for depression based on user data."""
    risk = 0
    
    # Family history
    if data.get("family_history_depression", False):
        risk += 15
    
    # Stress level
    stress = data.get("stress_level", 0)
    if stress > 8:
        risk += 20
    elif stress > 6:
        risk += 10
    
    # Sleep quality
    sleep_quality = data.get("sleep_quality", "")
    if sleep_quality == "poor":
        risk += 15
    elif sleep_quality == "fair":
        risk += 8
    
    # Sleep duration
    sleep_duration = data.get("sleep_duration", 0)
    if sleep_duration < 6 or sleep_duration > 9:
        risk += 10
    
    # Mental health history
    mental_health = data.get("mental_health_history", "").lower()
    if "depression" in mental_health or "anxiety" in mental_health:
        risk += 20
    
    # Physical activity (protective factor)
    if data.get("physical_activity", "") == "vigorous":
        risk -= 10
    elif data.get("physical_activity", "") == "moderate":
        risk -= 5
    
    return max(min(risk, 100), 0)


def calculate_risk(disease, data):
    """
    Main risk calculation dispatcher
    
    Parameters:
    disease (str): Name of the disease to calculate risk for
    data (dict): User assessment data
    
    Returns:
    int: Risk score from 0 to 100
    """
    risk_functions = {
        "Diabetes": calculate_diabetes_risk,
        "Heart Disease": calculate_heart_disease_risk,
        "Hypertension": calculate_hypertension_risk,
        "Obesity": calculate_obesity_risk,
        "Asthma": calculate_asthma_risk,
        "Depression": calculate_depression_risk
    }
    
    risk_func = risk_functions.get(disease)
    if risk_func:
        return risk_func(data)
    return 0


# ============================================================================
# RECOMMENDATION GENERATION
# ============================================================================

def generate_recommendations(data):
    """
    Generate personalized health recommendations based on user data
    
    Parameters:
    data (dict): User assessment data
    
    Returns:
    list: List of recommendation strings
    """
    recommendations = []
    
    # Physical activity recommendations
    activity = data.get("physical_activity", "")
    if activity == "sedentary":
        recommendations.append(
            "Start with 10-minute walks daily and gradually increase to 30 minutes "
            "of moderate exercise 5 days per week."
        )
    elif activity == "light":
        recommendations.append(
            "Increase your physical activity to 30-45 minutes of moderate exercise "
            "most days of the week for better health benefits."
        )
    
    # Nutrition recommendations
    fruit_veg = data.get("daily_fruit_veg_servings", 0)
    if fruit_veg < 5:
        recommendations.append(
            f"Increase your fruit and vegetable intake to at least 5 servings per day. "
            f"You currently consume {fruit_veg} servings."
        )
    
    water_intake = data.get("daily_water_intake", 0)
    if water_intake < 2000:
        recommendations.append(
            f"Increase your daily water intake to 2-3 liters. You currently drink "
            f"{water_intake}ml per day."
        )
    elif water_intake > 4000:
        recommendations.append(
            "Your water intake is very high. Consider consulting a doctor as excessive "
            "thirst can be a sign of underlying conditions."
        )
    
    # Sleep recommendations
    sleep_duration = data.get("sleep_duration", 0)
    sleep_quality = data.get("sleep_quality", "")
    
    if sleep_duration < 7:
        recommendations.append(
            f"Aim for 7-9 hours of sleep per night. Your current average is "
            f"{sleep_duration} hours."
        )
    elif sleep_duration > 9:
        recommendations.append(
            f"You're sleeping {sleep_duration} hours which is above the recommended "
            f"7-9 hours. Excessive sleep may indicate underlying health issues."
        )
    
    if sleep_quality in ["poor", "fair"]:
        recommendations.append(
            "Improve sleep quality by maintaining a consistent sleep schedule, "
            "avoiding screens before bed, and creating a relaxing bedtime routine."
        )
    
    # Stress management
    stress = data.get("stress_level", 0)
    if stress > 7:
        recommendations.append(
            "Practice stress reduction techniques such as meditation, deep breathing "
            "exercises, or yoga. Consider talking to a mental health professional."
        )
    elif stress > 5:
        recommendations.append(
            "Incorporate regular stress-relief activities into your routine like "
            "walking, listening to music, or pursuing a hobby."
        )
    
    # Smoking cessation
    smoking = data.get("smoking_status", "")
    if smoking == "current":
        recommendations.append(
            "Quitting smoking is the single best thing you can do for your health. "
            "Consider nicotine replacement therapy, counseling, or prescription medications."
        )
    
    # Alcohol recommendations
    alcohol = data.get("alcohol_consumption", "")
    if alcohol == "heavy":
        recommendations.append(
            "Reduce alcohol consumption to moderate levels (up to 1 drink per day for women, "
            "2 for men) or consider abstaining completely."
        )
    
    # Weight management
    bmi = data.get("bmi", 0)
    if bmi > 30:
        recommendations.append(
            "Work with a healthcare provider to develop a safe weight loss plan. "
            "Even losing 5-10% of body weight can significantly improve health."
        )
    elif bmi > 25:
        recommendations.append(
            "Focus on maintaining a healthy weight through balanced nutrition and "
            "regular physical activity."
        )
    elif bmi < 18.5:
        recommendations.append(
            "Consult a nutritionist to develop a healthy weight gain plan that "
            "includes nutrient-dense foods."
        )
    
    # Blood pressure management
    systolic = data.get("systolic_bp", 0)
    diastolic = data.get("diastolic_bp", 0)
    if systolic > 140 or diastolic > 90:
        recommendations.append(
            "Your blood pressure is elevated. Reduce sodium intake, exercise regularly, "
            "limit alcohol, and consult your doctor for proper management."
        )
    
    # Chronic pain
    chronic_pain = data.get("chronic_pain", "")
    if chronic_pain in ["moderate", "severe"]:
        recommendations.append(
            "Consult with a pain specialist. Consider physical therapy, acupuncture, "
            "or cognitive behavioral therapy for pain management."
        )
    
    # Mental health
    mental_health = data.get("mental_health_history", "")
    if mental_health:
        recommendations.append(
            "Continue prioritizing your mental health. Regular check-ins with a mental "
            "health professional can help maintain wellbeing."
        )
    
    # Return unique recommendations (remove duplicates)
    return list(dict.fromkeys(recommendations))


# ============================================================================
# RESULTS CALCULATION
# ============================================================================

def calculate_results():
    """
    Calculate all health risks, overall score, and generate recommendations
    """
    # Calculate BMI if height and weight are available
    if "bmi" not in st.session_state.assessment_data:
        height = st.session_state.assessment_data.get("height", 170)
        weight = st.session_state.assessment_data.get("weight", 70)
        bmi = calculate_bmi(weight, height)
        st.session_state.assessment_data["bmi"] = bmi
        st.session_state.assessment_data["bmi_category"] = get_bmi_category(bmi)
    
    # Calculate risk for each disease
    diseases = ["Diabetes", "Heart Disease", "Hypertension", "Obesity", "Asthma", "Depression"]
    risk_data = []
    
    for disease in diseases:
        risk = calculate_risk(disease, st.session_state.assessment_data)
        risk_data.append({"disease": disease, "risk": risk})
    
    st.session_state.risk_data = risk_data
    
    # Calculate overall health score (0-100, higher is better)
    total_risk = sum(item["risk"] for item in risk_data)
    max_possible_risk = len(diseases) * 100
    health_score = round(100 * (1 - total_risk / max_possible_risk))
    st.session_state.health_score = max(0, min(100, health_score))
    
    # Generate personalized recommendations
    st.session_state.recommendations = generate_recommendations(st.session_state.assessment_data)
    
    # Save to history
    assessment_record = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "health_score": st.session_state.health_score,
        "risks": risk_data,
        "bmi": st.session_state.assessment_data.get("bmi", 0)
    }
    st.session_state.assessment_history.append(assessment_record)
    
    st.session_state.results_calculated = True


# ============================================================================
# FORM HANDLING FUNCTIONS
# ============================================================================

def process_step(step_index):
    """
    Save current step data and proceed to next step or calculate results
    
    Parameters:
    step_index (int): Index of the current step
    """
    # Save form data to session state
    for field in steps[step_index]["fields"]:
        if field in st.session_state:
            st.session_state.assessment_data[field] = st.session_state[field]
    
    # Move to next step or calculate results
    if step_index < len(steps) - 1:
        st.session_state.current_step += 1
    else:
        calculate_results()


def go_back():
    """Navigate to the previous step"""
    if st.session_state.current_step > 0:
        st.session_state.current_step -= 1


def restart_assessment():
    """Reset all session state variables to start a new assessment"""
    st.session_state.current_step = 0
    st.session_state.assessment_data = {}
    st.session_state.results_calculated = False
    st.session_state.risk_data = []
    st.session_state.health_score = 0
    st.session_state.recommendations = []


def export_results():
    """
    Export assessment results as JSON for download
    """
    export_data = {
        "assessment_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "health_score": st.session_state.health_score,
        "risk_scores": st.session_state.risk_data,
        "recommendations": st.session_state.recommendations,
        "user_data": st.session_state.assessment_data
    }
    
    json_str = json.dumps(export_data, indent=2)
    return json_str


# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def display_risk_bar_chart(risk_data):
    """
    Display bar chart of disease risks
    
    Parameters:
    risk_data (list): List of dictionaries with disease and risk values
    """
    risk_df = pd.DataFrame(risk_data)
    
    # Define color based on risk level
    def get_color(risk):
        if risk < 30:
            return 'green'
        elif risk < 60:
            return 'orange'
        else:
            return 'red'
    
    risk_df['color'] = risk_df['risk'].apply(get_color)
    
    fig = px.bar(
        risk_df, 
        x='disease', 
        y='risk',
        title='Disease Risk Assessment',
        labels={'disease': 'Disease', 'risk': 'Risk Score (%)'},
        color='risk',
        color_continuous_scale=[(0, 'green'), (0.5, 'yellow'), (1, 'red')],
        range_y=[0, 100]
    )
    
    fig.update_layout(
        height=400,
        xaxis_title="Disease",
        yaxis_title="Risk Score (%)",
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_risk_radar_chart(risk_data):
    """
    Display radar chart for comparing disease risks
    
    Parameters:
    risk_data (list): List of dictionaries with disease and risk values
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=[item["risk"] for item in risk_data],
        theta=[item["disease"] for item in risk_data],
        fill='toself',
        name='Your Risk Profile',
        line_color='blue',
        fillcolor='rgba(0, 0, 255, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[0, 25, 50, 75, 100]
            )
        ),
        title="Health Risk Radar Chart",
        height=450,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_health_score_gauge(score):
    """
    Display a gauge chart for overall health score
    
    Parameters:
    score (int): Health score from 0 to 100
    """
    # Determine color based on score
    if score >= 70:
        color = "green"
    elif score >= 40:
        color = "orange"
    else:
        color = "red"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Overall Health Score", 'font': {'size': 24}},
        delta={'reference': 50, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': '#ffcccc'},
                {'range': [30, 70], 'color': '#ffffcc'},
                {'range': [70, 100], 'color': '#ccffcc'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)


def display_bmi_info(bmi, bmi_category):
    """
    Display BMI information with interpretation
    
    Parameters:
    bmi (float): BMI value
    bmi_category (str): BMI category
    """
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure(go.Indicator(
            mode="number",
            value=bmi,
            title={"text": "Your BMI"},
            number={"font": {"size": 40}}
        ))
        fig.update_layout(height=150)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.metric("BMI Category", bmi_category)
        
        # BMI interpretation
        if bmi_category == "Underweight":
            st.warning("You are underweight. Consider consulting a nutritionist.")
        elif bmi_category == "Normal weight":
            st.success("Your weight is in the healthy range. Keep it up!")
        elif bmi_category == "Overweight":
            st.warning("You are overweight. Focus on healthy eating and exercise.")
        else:
            st.error("You are in the obese range. Please consult a healthcare provider.")


def display_risk_summary(risk_data):
    """
    Display a summary table of risk levels
    
    Parameters:
    risk_data (list): List of dictionaries with disease and risk values
    """
    summary_data = []
    for item in risk_data:
        risk = item["risk"]
        if risk < 30:
            level = "Low"
            icon = "🟢"
        elif risk < 60:
            level = "Moderate"
            icon = "🟡"
        else:
            level = "High"
            icon = "🔴"
        
        summary_data.append({
            "Disease": item["disease"],
            "Risk Score": f"{risk}%",
            "Risk Level": f"{icon} {level}"
        })
    
    summary_df = pd.DataFrame(summary_data)
    st.table(summary_df)


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def show_health_score():
    """
    Main function to display the health score assessment interface
    """
    st.title("Health Score Assessment")
    st.markdown("---")
    
    # Initialize session state
    init_session_state()
    
    # Display results if calculated
    if st.session_state.results_calculated:
        st.header("Your Health Assessment Results")
        st.markdown(f"**Assessment Date:** {datetime.now().strftime('%B %d, %Y')}")
        st.markdown("---")
        
        # Display health score gauge prominently
        display_health_score_gauge(st.session_state.health_score)
        
        # Create two columns for charts
        col1, col2 = st.columns(2)
        
        with col1:
            display_risk_bar_chart(st.session_state.risk_data)
        
        with col2:
            display_risk_radar_chart(st.session_state.risk_data)
        
        # Display BMI information
        if "bmi" in st.session_state.assessment_data:
            st.subheader("Body Mass Index (BMI)")
            display_bmi_info(
                st.session_state.assessment_data["bmi"],
                st.session_state.assessment_data.get("bmi_category", "Unknown")
            )
        
        st.markdown("---")
        
        # Risk summary table
        st.subheader("Risk Level Summary")
        display_risk_summary(st.session_state.risk_data)
        
        st.markdown("---")
        
        # Personalized recommendations
        st.subheader("Personalized Health Recommendations")
        st.markdown("Based on your responses, here are actionable recommendations:")
        
        for i, recommendation in enumerate(st.session_state.recommendations, 1):
            st.markdown(f"{i}. {recommendation}")
        
        st.markdown("---")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Start New Assessment", use_container_width=True):
                restart_assessment()
                st.rerun()
        
        with col2:
            # Export results as JSON
            json_data = export_results()
            st.download_button(
                label="Download Results (JSON)",
                data=json_data,
                file_name=f"health_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col3:
            # Disclaimer
            with st.expander("Medical Disclaimer"):
                st.markdown("""
                **Important Note:** This assessment is for informational and educational purposes only.
                It is not a substitute for professional medical advice, diagnosis, or treatment.
                Always seek the advice of your physician or other qualified health provider with any 
                questions you may have regarding a medical condition.
                """)
    
    # Display assessment form if results not calculated
    else:
        current_step = st.session_state.current_step
        step = steps[current_step]
        
        # Progress bar
        progress = (current_step + 1) / len(steps)
        st.progress(progress)
        
        # Step header
        st.header(f"Step {current_step + 1} of {len(steps)}: {step['title']}")
        st.markdown(f"*{step['description']}*")
        st.markdown("---")
        
        # Create a centered form container
        col1, form_col, col3 = st.columns([1, 2, 1])
        
        with form_col:
            with st.form(key=f"step_{current_step}_form"):
                # ========== BASIC INFORMATION ==========
                if "age" in step["fields"]:
                    st.number_input(
                        "Age (years)",
                        min_value=18,
                        max_value=120,
                        value=st.session_state.assessment_data.get("age", 30),
                        key="age",
                        help="Your current age in years"
                    )
                
                if "gender" in step["fields"]:
                    gender_options = ["male", "female", "other"]
                    gender_index = gender_options.index(
                        st.session_state.assessment_data.get("gender", "male")
                    )
                    st.selectbox(
                        "Gender",
                        options=gender_options,
                        index=gender_index,
                        key="gender",
                        help="Select your gender"
                    )
                
                if "height" in step["fields"]:
                    st.number_input(
                        "Height (cm)",
                        min_value=100,
                        max_value=250,
                        value=st.session_state.assessment_data.get("height", 170),
                        key="height",
                        help="Your height in centimeters"
                    )
                
                if "weight" in step["fields"]:
                    st.number_input(
                        "Weight (kg)",
                        min_value=30,
                        max_value=300,
                        value=st.session_state.assessment_data.get("weight", 70),
                        key="weight",
                        help="Your weight in kilograms"
                    )
                
                # ========== LIFESTYLE ==========
                if "smoking_status" in step["fields"]:
                    smoking_options = ["never", "former", "current"]
                    smoking_index = smoking_options.index(
                        st.session_state.assessment_data.get("smoking_status", "never")
                    )
                    st.selectbox(
                        "Smoking Status",
                        options=smoking_options,
                        index=smoking_index,
                        key="smoking_status",
                        help="Current smoking status"
                    )
                
                if "alcohol_consumption" in step["fields"]:
                    alcohol_options = ["none", "moderate", "heavy"]
                    alcohol_index = alcohol_options.index(
                        st.session_state.assessment_data.get("alcohol_consumption", "moderate")
                    )
                    st.selectbox(
                        "Alcohol Consumption",
                        options=alcohol_options,
                        index=alcohol_index,
                        key="alcohol_consumption",
                        help="Alcohol consumption level"
                    )
                
                if "physical_activity" in step["fields"]:
                    activity_options = ["sedentary", "light", "moderate", "vigorous"]
                    activity_index = activity_options.index(
                        st.session_state.assessment_data.get("physical_activity", "moderate")
                    )
                    st.selectbox(
                        "Physical Activity Level",
                        options=activity_options,
                        index=activity_index,
                        key="physical_activity",
                        help="Your typical daily physical activity level"
                    )
                
                if "diet_type" in step["fields"]:
                    diet_options = ["balanced", "high-carb", "high-protein", "vegetarian", "vegan"]
                    diet_index = diet_options.index(
                        st.session_state.assessment_data.get("diet_type", "balanced")
                    )
                    st.selectbox(
                        "Diet Type",
                        options=diet_options,
                        index=diet_index,
                        key="diet_type",
                        help="Your typical dietary pattern"
                    )
                
                # ========== MEDICAL HISTORY ==========
                if "family_history_diabetes" in step["fields"]:
                    st.checkbox(
                        "Family History of Diabetes",
                        value=st.session_state.assessment_data.get("family_history_diabetes", False),
                        key="family_history_diabetes",
                        help="Check if any immediate family member has diabetes"
                    )
                
                if "family_history_heart_disease" in step["fields"]:
                    st.checkbox(
                        "Family History of Heart Disease",
                        value=st.session_state.assessment_data.get("family_history_heart_disease", False),
                        key="family_history_heart_disease",
                        help="Check if any immediate family member has heart disease"
                    )
                
                if "family_history_hypertension" in step["fields"]:
                    st.checkbox(
                        "Family History of Hypertension",
                        value=st.session_state.assessment_data.get("family_history_hypertension", False),
                        key="family_history_hypertension",
                        help="Check if any immediate family member has high blood pressure"
                    )
                
                if "previous_diagnoses" in step["fields"]:
                    st.text_input(
                        "Previous Diagnoses",
                        value=st.session_state.assessment_data.get("previous_diagnoses", ""),
                        key="previous_diagnoses",
                        help="List any previous medical diagnoses (comma separated)"
                    )
                
                # ========== VITAL SIGNS ==========
                if "systolic_bp" in step["fields"]:
                    st.number_input(
                        "Systolic Blood Pressure (mmHg)",
                        min_value=70,
                        max_value=220,
                        value=st.session_state.assessment_data.get("systolic_bp", 120),
                        key="systolic_bp",
                        help="Upper number in blood pressure reading"
                    )
                
                if "diastolic_bp" in step["fields"]:
                    st.number_input(
                        "Diastolic Blood Pressure (mmHg)",
                        min_value=40,
                        max_value=130,
                        value=st.session_state.assessment_data.get("diastolic_bp", 80),
                        key="diastolic_bp",
                        help="Lower number in blood pressure reading"
                    )
                
                if "resting_heart_rate" in step["fields"]:
                    st.number_input(
                        "Resting Heart Rate (bpm)",
                        min_value=40,
                        max_value=120,
                        value=st.session_state.assessment_data.get("resting_heart_rate", 70),
                        key="resting_heart_rate",
                        help="Heart rate when completely at rest"
                    )
                
                # ========== MENTAL HEALTH ==========
                if "stress_level" in step["fields"]:
                    st.slider(
                        "Stress Level (1-10)",
                        min_value=1,
                        max_value=10,
                        value=st.session_state.assessment_data.get("stress_level", 5),
                        key="stress_level",
                        help="1 = No stress, 10 = Extremely stressed"
                    )
                
                if "sleep_quality" in step["fields"]:
                    sleep_options = ["poor", "fair", "good", "excellent"]
                    sleep_index = sleep_options.index(
                        st.session_state.assessment_data.get("sleep_quality", "good")
                    )
                    st.selectbox(
                        "Sleep Quality",
                        options=sleep_options,
                        index=sleep_index,
                        key="sleep_quality",
                        help="How would you rate your sleep quality?"
                    )
                
                if "sleep_duration" in step["fields"]:
                    st.number_input(
                        "Sleep Duration (hours)",
                        min_value=3.0,
                        max_value=12.0,
                        value=float(st.session_state.assessment_data.get("sleep_duration", 7.0)),
                        step=0.5,
                        key="sleep_duration",
                        help="Average hours of sleep per night"
                    )
                
                # ========== NUTRITION ==========
                if "daily_water_intake" in step["fields"]:
                    st.number_input(
                        "Daily Water Intake (ml)",
                        min_value=0,
                        max_value=5000,
                        value=st.session_state.assessment_data.get("daily_water_intake", 2000),
                        step=100,
                        key="daily_water_intake",
                        help="Recommended: 2000-3000ml per day"
                    )
                
                if "daily_fruit_veg_servings" in step["fields"]:
                    st.number_input(
                        "Daily Fruit & Vegetable Servings",
                        min_value=0,
                        max_value=10,
                        value=st.session_state.assessment_data.get("daily_fruit_veg_servings", 3),
                        key="daily_fruit_veg_servings",
                        help="Recommended: 5 or more servings per day"
                    )
                
                # ========== BODY COMPOSITION ==========
                if "waist_circumference" in step["fields"]:
                    st.number_input(
                        "Waist Circumference (cm)",
                        min_value=50,
                        max_value=200,
                        value=st.session_state.assessment_data.get("waist_circumference", 80),
                        key="waist_circumference",
                        help="Measure at the narrowest point of your waist"
                    )
                
                if "body_fat_percentage" in step["fields"]:
                    st.number_input(
                        "Body Fat Percentage",
                        min_value=5.0,
                        max_value=50.0,
                        value=float(st.session_state.assessment_data.get("body_fat_percentage", 20.0)),
                        step=0.5,
                        key="body_fat_percentage",
                        help="Optional: If you know your body fat percentage"
                    )
                
                # ========== ADDITIONAL HEALTH INFO ==========
                if "family_history_asthma" in step["fields"]:
                    st.checkbox(
                        "Family History of Asthma",
                        value=st.session_state.assessment_data.get("family_history_asthma", False),
                        key="family_history_asthma",
                        help="Check if any immediate family member has asthma"
                    )
                
                if "family_history_obesity" in step["fields"]:
                    st.checkbox(
                        "Family History of Obesity",
                        value=st.session_state.assessment_data.get("family_history_obesity", False),
                        key="family_history_obesity",
                        help="Check if any immediate family member is obese"
                    )
                
                if "family_history_depression" in step["fields"]:
                    st.checkbox(
                        "Family History of Depression",
                        value=st.session_state.assessment_data.get("family_history_depression", False),
                        key="family_history_depression",
                        help="Check if any immediate family member has depression"
                    )
                
                if "allergies" in step["fields"]:
                    st.text_input(
                        "Allergies",
                        value=st.session_state.assessment_data.get("allergies", ""),
                        key="allergies",
                        help="List any known allergies (comma separated)"
                    )
                
                if "chronic_pain" in step["fields"]:
                    pain_options = ["none", "mild", "moderate", "severe"]
                    pain_index = pain_options.index(
                        st.session_state.assessment_data.get("chronic_pain", "none")
                    )
                    st.selectbox(
                        "Chronic Pain Level",
                        options=pain_options,
                        index=pain_index,
                        key="chronic_pain",
                        help="Level of chronic pain you experience"
                    )
                
                if "mental_health_history" in step["fields"]:
                    st.text_area(
                        "Mental Health History",
                        value=st.session_state.assessment_data.get("mental_health_history", ""),
                        key="mental_health_history",
                        help="Any history of mental health conditions or concerns",
                        height=100
                    )
                
                # ========== FORM BUTTONS ==========
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    if current_step > 0:
                        if st.form_submit_button("Previous", use_container_width=True):
                            go_back()
                            st.rerun()
                
                with col2:
                    if current_step < len(steps) - 1:
                        if st.form_submit_button("Next", use_container_width=True):
                            process_step(current_step)
                            st.rerun()
                    else:
                        if st.form_submit_button("Submit Assessment", type="primary", use_container_width=True):
                            process_step(current_step)
                            st.rerun()
