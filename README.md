# SURGE | AI-Powered Dynamic Pricing Engine

An enterprise-grade, full-stack predictive pricing platform that calculates real-time taxi fares using machine learning. The system simulates live ride-hailing demand patterns, analyzing variables like trip distance, traffic congestion, time of day, and weather anomalies to generate optimal price points.

Developed with a decoupled architecture featuring a **Python (FastAPI) Machine Learning Service** and a **React (Vite + Tailwind CSS) Analytics Dashboard**.

---

## System Architecture

The application is split into two independent microservices communicating over local REST endpoints:

1. **The Core ML API (Backend):** Built with Python and FastAPI. It loads a serialized Random Forest model into memory on startup and exposes a low-latency `/predict` POST endpoint to serve inference requests.
2. **The Analytics Dashboard (Frontend):** Built with React.js and Tailwind CSS. It features highly responsive state controls (sliders and buttons) that trigger asynchronous network requests (Axios) to plot real-time predictive charts (Recharts).

---

## Machine Learning Pipeline

The predictive brain of SURGE is a supervised regression model built using **Scikit-Learn**:

*   **Dataset:** 5,000 synthetically generated historical ride records mimicking urban transport surge patterns.
*   **Feature Engineering:** Raw categorical text values (e.g., Weather conditions like `Clear`, `Rain`, `Snow`) are transformed using **One-Hot Encoding** to maintain mathematical compatibility with the model.
*   **Algorithm:** **Random Forest Regressor** (100 Decision Trees).
*   **Evaluation Metric:** Mean Absolute Error (MAE), achieving a highly accurate predictive boundary within **~$1.21** of historical dynamic price limits.
*   **Serialization:** Model weights and target feature lists are serialized into `.joblib` pipelines for instant serving.

---

## Technical Stack

*   **Machine Learning & Data Science:** Python, Scikit-Learn, Pandas, NumPy, Joblib
*   **Backend Server:** FastAPI, Uvicorn (ASGI Web Server), Pydantic
*   **Frontend Dashboard:** React.js, Vite, Tailwind CSS, Recharts (Data Visualization), Axios
*   **Workflow & DevOps:** Git, GitHub (Strict Feature-Branch Git Workflows, Pull Requests)

---

## Installation & Local Execution

### Prerequisites
*   macOS (Optimized) / Linux
*   Python 3.10+
*   Node.js v18+

---

### Step 1: Backend Setup & ML Service

Open your terminal, navigate to the project directory, and run:

```bash
# Navigate to backend
cd backend

# Initialize and activate isolated Python environment
python -m venv venv
source venv/bin/activate

# Install exact dependency pipeline
pip install pandas numpy scikit-learn fastapi uvicorn joblib

# Run data generation and train the ML model
python generate_data.py
python train_model.py

# Launch the FastAPI Uvicorn Server
python -m uvicorn main:app --reload
```
*   **API Live Server:** `http://127.0.0.1:8000`
*   **Interactive Swagger API Docs:** `http://127.0.0.1:8000/docs`

---

### Step 2: Frontend Setup & Web Dashboard

Open a **new** terminal tab/window and run:

```bash
# Navigate to frontend
cd frontend

# Install UI and networking libraries
npm install

# Start the Vite React local development server
npm run dev
```
*   **Web Application URL:** `http://localhost:5173`

---
