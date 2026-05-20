from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <--- NEW
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# --- CORS MIDDLEWARE (NEW) ---
# This gives our React app permission to talk to our Python server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # React's URL
    allow_credentials=True,
    allow_methods=["*"], # Allow all requests (GET, POST, etc.)
    allow_headers=["*"],
)

# Load the AI brain
model = joblib.load('surge_model.joblib')
model_features = joblib.load('model_features.joblib')

class RideRequest(BaseModel):
    hour: int
    weather: str
    distance: float
    traffic_multiplier: float

@app.get("/")
def home():
    return {"message": "Surge Pricing API is Running"}

@app.post("/predict")
def predict_price(request: RideRequest):
    input_data = {
        'Hour': [request.hour],
        'Distance_Miles': [request.distance],
        'Traffic_Multiplier': [request.traffic_multiplier],
        'Weather_Clear': [1 if request.weather == 'Clear' else 0],
        'Weather_Rain': [1 if request.weather == 'Rain' else 0],
        'Weather_Snow': [1 if request.weather == 'Snow' else 0]
    }
    df_input = pd.DataFrame(input_data)
    df_input = df_input[model_features]
    prediction = model.predict(df_input)
    return {"predicted_price": round(float(prediction[0]), 2)}