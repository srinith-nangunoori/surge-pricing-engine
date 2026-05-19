import pandas as pd
import numpy as np
import random

# We are generating 5000 fake historical taxi rides for the AI to study
NUM_SAMPLES = 5000

data = []
weather_conditions = ['Clear', 'Rain', 'Snow']

for _ in range(NUM_SAMPLES):
    # 1. Randomly pick an hour of the day (0 to 23)
    hour = random.randint(0, 23)
    
    # 2. Randomly pick weather
    weather = random.choice(weather_conditions)
    
    # 3. Randomly generate distance of the ride in miles (1 to 20 miles)
    distance_miles = round(random.uniform(1.0, 20.0), 2)
    
    # 4. Determine traffic based on the hour (Rush hour = high traffic)
    if hour in [7, 8, 9, 16, 17, 18]:
        traffic_multiplier = random.uniform(1.5, 2.5) # Heavy traffic
    elif hour in [0, 1, 2, 3, 4]:
        traffic_multiplier = random.uniform(0.8, 1.0) # Very light traffic (night)
    else:
        traffic_multiplier = random.uniform(1.0, 1.5) # Normal traffic
        
    # 5. Determine weather penalty (Bad weather = higher price)
    if weather == 'Rain':
        weather_multiplier = 1.2
    elif weather == 'Snow':
        weather_multiplier = 1.5
    else:
        weather_multiplier = 1.0 # Clear weather, no extra charge
        
    # 6. CALCULATE THE FINAL HISTORICAL PRICE
    # Base fee + ($2 per mile) * traffic * weather + a little random noise (real life isn't perfect)
    base_fee = 3.00
    price = (base_fee + (distance_miles * 2.0)) * traffic_multiplier * weather_multiplier
    
    # Add random noise between -$2 and +$2 to make it realistic
    price += random.uniform(-2.0, 2.0) 
    
    # Ensure price never drops below a minimum of $5
    price = max(5.0, round(price, 2))
    
    # Save this ride to our list
    data.append([hour, weather, distance_miles, traffic_multiplier, price])

# Convert the list into a Pandas DataFrame (like an Excel sheet)
df = pd.DataFrame(data, columns=['Hour', 'Weather', 'Distance_Miles', 'Traffic_Multiplier', 'Final_Price'])

# Save it to a CSV file
df.to_csv('historical_pricing_data.csv', index=False)
print("Successfully generated 5000 ride records in 'historical_pricing_data.csv'")