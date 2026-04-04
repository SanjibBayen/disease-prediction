# Early Prediction of Health & Lifestyle Diseases

An AI-powered healthcare prediction system that leverages machine learning and natural language processing to assess disease risks and provide personalized health insights.

---

## Overview

This application provides early prediction and analysis of multiple health conditions using trained machine learning models. It enables users to understand potential health risks based on medical indicators, lifestyle factors, and symptoms through an interactive web interface.

The system integrates predictive analytics, mental health assessment, and an AI-powered medical assistant into a unified platform.

---

## Features

### Disease Prediction Models

- Diabetes Risk Prediction
- Hypertension Risk Assessment
- Cardiovascular Disease Prediction
- Stroke Risk Analysis
- Asthma Detection
- Sleep Disorder Analysis

### Additional Functionalities

- Mental Health Assessment using transformer-based NLP models
- Comprehensive Health Score System (8-step evaluation)
- AI-powered Medical Consultant chatbot
- Interactive Data Visualization dashboard

---

## Technology Stack

Frontend:
- Streamlit

Machine Learning:
- Scikit-learn
- XGBoost

Natural Language Processing:
- Transformers (Hugging Face)

Visualization:
- Matplotlib
- Seaborn
- Plotly

Data Processing:
- Pandas
- NumPy

AI Integration:
- Google Gemini API

---

## Project Structure

disease-prediction/

├── app.py  
├── health_score.py  

├── diabetes/  
├── asthma/  
├── cardio_vascular/  
├── stroke/  
├── sleep_health/  
├── hypertension/  
├── mental/  

├── data_csv/  
├── requirements.txt  
└── .env  

---

## Installation

### Prerequisites

- Python 3.10 or 3.11 recommended
- pip package manager

### Setup Instructions

1. Clone the repository

git clone https://github.com/MOHITRAJDEO12345/early-prediction-for-ml_proj.git  
cd early-prediction-for-ml_proj  

2. Create and activate a virtual environment

python -m venv venv  
venv\Scripts\activate  

3. Install dependencies

pip install -r requirements.txt  

4. Configure environment variables

Create a `.env` file in the root directory:

GOOGLE_API_KEY=your_gemini_api_key  
HF_TOKEN=your_huggingface_token  

5. Run the application

streamlit run app.py  

---

## Usage

Use the sidebar navigation to access different modules:

- Home  
- Health Score  
- Diabetes Prediction  
- Hypertension Prediction  
- Cardiovascular Disease Prediction  
- Stroke Prediction  
- Asthma Prediction  
- Sleep Health Analysis  
- Mental Analysis  
- Medical Consultant  
- Data Visualization  

---

## Health Score System

The Health Score module evaluates users through an 8-step assessment:

1. Basic Information  
2. Lifestyle Habits  
3. Medical History  
4. Vital Signs  
5. Mental Health  
6. Nutrition  
7. Body Composition  
8. Additional Health Information  

### Output

- Overall Health Score (0–100)
- Disease-specific risk probabilities
- Visual analytics and charts
- Personalized health recommendations

---

## Data Sources

The models are trained on publicly available healthcare datasets from Kaggle, including:

- Diabetes Dataset  
- Cardiovascular Disease Dataset  
- Stroke Prediction Dataset  
- Asthma Dataset  
- Sleep Health Dataset  
- Hypertension Dataset  

---

## Disclaimer

This application is intended for educational and informational purposes only.

- It has not undergone clinical validation  
- It should not be used for medical diagnosis or treatment  
- Users should consult qualified healthcare professionals for medical advice  

---

## Future Enhancements

- Integration with wearable devices (e.g., Fitbit)
- Time-series analysis using LSTM models
- User authentication and health tracking
- Automated report generation
- AI-driven fitness and nutrition recommendations

---

## License

This project is developed for educational purposes only.

---

## Author

Sanjib Bayen

GitHub: https://github.com/sanjibbayen  
Email: sanjibbayen11@gmail.com  

---

## Acknowledgments

- Kaggle for providing healthcare datasets  
- Hugging Face for NLP models  
- Google for Gemini API  
- Streamlit for the application framework  
