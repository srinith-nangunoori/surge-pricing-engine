from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# 1. Create the FastAPI app
app = FastAPI()

# 2. Load the AI brain and the list of features it needs
model = joblib.load('surge_model.joblib')
model_features = joblib.load('model_features.joblib')

# 3. Define what a "Request" looks like (The Order Form)
class RideRequest(BaseModel):
    hour: int
    weather: str
    distance: float
    traffic_multiplier: float

@app.get("/")
def home():
    return {"message": "Surge Pricing API is Running"}

# 4. The Prediction Endpoint (The main task)
@app.post("/predict")
def predict_price(request: RideRequest):
    # a. Convert the incoming request into a Format the AI understands
    # Remember: the AI needs those 1s and 0s for Weather
    input_data = {
        'Hour': [request.hour],
        'Distance_Miles': [request.distance],
        'Traffic_Multiplier': [request.traffic_multiplier],
        'Weather_Clear': [1 if request.weather == 'Clear' else 0],
        'Weather_Rain': [1 if request.weather == 'Rain' else 0],
        'Weather_Snow': [1 if request.weather == 'Snow' else 0]
    }
    
    # b. Convert to a DataFrame
    df_input = pd.DataFrame(input_data)
    
    # c. Make sure the columns are in the EXACT same order as when we trained
    df_input = df_input[model_features]
    
    # d. Get the prediction from the AI
    prediction = model.predict(df_input)
    
    # e. Return the answer as JSON
    return {"predicted_price": round(float(prediction[0]), 2)}