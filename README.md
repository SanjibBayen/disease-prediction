# 🏥 HealthPredict AI  
### Early Prediction of Health & Lifestyle Diseases

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)  
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)  
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5-purple.svg)](https://vitejs.dev/)
[![Render](https://img.shields.io/badge/Deployed-Render-purple.svg)](https://render.com)

An **AI-powered healthcare prediction system** that leverages machine learning to assess disease risks and provide personalized health insights.

---

## 🌐 Live Demo

- **API Endpoint:** https://disease-prediction-72fh.onrender.com  
- **API Docs (Swagger):** https://disease-prediction-72fh.onrender.com/docs  

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [API Endpoints](#api-endpoints)
- [Example Request & Response](#example-request--response)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [Disclaimer](#disclaimer)
- [Future Enhancements](#future-enhancements)
- [Contact](#contact)

---

# Overview

HealthPredict AI is a comprehensive healthcare prediction system that uses machine learning to assess risks for multiple diseases. The platform provides:

- **RESTful API** built with FastAPI
- **React + Vite** frontend application
- **7 ML Models** for disease prediction
- **Mental Health Analysis** using NLP
- **Real-time predictions** with high accuracy

---

## Features

### 🩺 Disease Prediction Models

| Disease | Model | Accuracy |
|---------|-------|----------|
| Diabetes | SVC | 85% |
| Hypertension | Extra Trees | 82% |
| Cardiovascular | XGBoost | 78% |
| Stroke | Ensemble | 80% |
| Asthma | Random Forest | 83% |
| Sleep Disorders | SVC | 76% |
| Mental Health | NLP Transformer | 82% |

### 🎨 Frontend Features (React + Vite)

- Modern, responsive UI with Tailwind CSS
- Interactive dashboards and charts
- Real-time form validation
- Smooth animations with Framer Motion
- API integration with Axios
- TypeScript for type safety

---

## Technology Stack

### Backend
| Component | Technology |
|-----------|------------|
| API Framework | FastAPI |
| ML Models | Scikit-learn, XGBoost |
| NLP | Hugging Face Transformers |
| Server | Uvicorn |
| Deployment | Render |

### Frontend
| Component | Technology |
|-----------|------------|
| Framework | React 18 |
| Build Tool | Vite |
| Language | TypeScript |
| Styling | Tailwind CSS |
| Animations | Framer Motion |
| Charts | Recharts |
| Icons | Lucide React |
| HTTP Client | Axios |
| Forms | React Hook Form |

---

## 🔌 API Endpoints

### System Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/api/health` | Health check |
| GET | `/docs` | Swagger UI |
| GET | `/redoc` | ReDoc UI |

### Prediction Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/predict/diabetes` | Diabetes prediction |
| POST | `/api/predict/asthma` | Asthma prediction |
| POST | `/api/predict/cardio` | Cardiovascular prediction |
| POST | `/api/predict/stroke` | Stroke prediction |
| POST | `/api/predict/hypertension` | Hypertension prediction |
| POST | `/api/predict/mental-health` | Mental health analysis |

---

## 📡 Example Request & Response

### 📤 Example Request

```bash
curl -X POST https://disease-prediction-72fh.onrender.com/api/predict/diabetes \
  -H "Content-Type: application/json" \
  -d '{
    "pregnancies": 1,
    "glucose": 120,
    "blood_pressure": 80,
    "skin_thickness": 20,
    "insulin": 79,
    "bmi": 25.5,
    "diabetes_pedigree": 0.5,
    "age": 35
  }'
```

---

### 📥 Example Response

```json
{
  "success": true,
  "prediction": 0,
  "probability": 75.0,
  "risk_level": "Low",
  "message": "No signs of diabetes detected",
  "recommendations": [
    "Continue maintaining a healthy balanced diet",
    "Exercise regularly - at least 150 minutes per week"
  ],
  "timestamp": "2026-04-04T18:04:09.537662"
}
```

---

## ⚙️ Installation

### 📌 Prerequisites
- Python 3.11+
- pip
- Git

### 🚀 Setup

```bash
git clone https://github.com/SanjibBayen/disease-prediction.git
cd disease-prediction

python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file inside `/backend`:

```env
HOST=0.0.0.0
PORT=8000
DEBUG=False
ENVIRONMENT=production
LOG_LEVEL=info
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## ▶️ Usage

```bash
cd backend
python run.py
```

Access:

- API → http://localhost:8000  
- Docs → http://localhost:8000/docs  

---

## 📁 Project Structure

```text
disease-prediction/
├── backend/
│   ├── app/
│   ├── services/
│   ├── utils/
│   ├── models/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── run.py
├── frontend/
├── data_csv/
├── docker-compose.yml
└── .gitignore
```

---

## 🚀 Deployment

### Render

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Docker

```bash
docker build -t healthpredict-backend ./backend
docker run -p 8000:8000 healthpredict-backend
```

---

## ⚠️ Disclaimer

> This project is for educational purposes only

- Not clinically validated  
- Not for medical diagnosis  
- Predictions may not be accurate  

Always consult a medical professional.

---

## 🔮 Future Enhancements

- Authentication system  
- API rate limiting  
- Database integration  
- Wearable integration  
- LSTM models  
- Email reports  
- Mobile app  

---

## 📬 Contact

- **Author:** Sanjib Bayen  
- **GitHub:** https://github.com/SanjibBayen  
- **Email:** sanjibbayen11@gmail.com  

---

## 🙏 Acknowledgments

- Kaggle  
- Hugging Face  
- FastAPI  
- Render  
- Scikit-learn  

---

**Made with ❤️ by Sanjib Bayen | © 2026**