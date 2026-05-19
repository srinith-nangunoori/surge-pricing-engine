import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

print("1. Loading historical data...")
# Load the CSV we generated
df = pd.read_csv('historical_pricing_data.csv')

# In Machine Learning, AI can only understand NUMBERS, not text.
# Our 'Weather' column has text ('Rain', 'Snow', 'Clear').
# get_dummies() converts these text categories into binary columns (1s and 0s).
df = pd.get_dummies(df, columns=['Weather'])

print("2. Splitting data into Features (X) and Target (y)...")
# FEATURES (X): The information the AI is allowed to look at to make a guess.
# TARGET (y): The final answer we want the AI to predict (The Price).
X = df.drop('Final_Price', axis=1) # Everything EXCEPT the price
y = df['Final_Price']              # ONLY the price

print("3. Creating Training and Testing sets...")
# We split our 5000 rows. 
# 80% (4000 rows) is used to TRAIN the AI.
# 20% (1000 rows) is hidden from the AI to TEST it later like a final exam.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("4. Training the Random Forest AI...")
# A Random Forest creates hundreds of virtual "Decision Trees" and averages their guesses.
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train) # <-- THIS is where the AI actually learns.

print("5. Testing the AI on unseen data...")
# We ask the AI to guess the prices for the 1000 rows it has never seen
predictions = model.predict(X_test)

# We check how far off its guesses were from the real answers
error = mean_absolute_error(y_test, predictions)
print(f"-> AI Accuracy: On average, the AI's price guess is off by ${error:.2f}")

print("6. Saving the AI brain to disk...")
# We save the trained model so our web server can load it later
joblib.dump(model, 'surge_model.joblib')

# We also save the EXACT names of the columns (Features) the AI was trained on.
# The server will need this to format web requests correctly.
joblib.dump(list(X.columns), 'model_features.joblib')

print("Done! Model saved as 'surge_model.joblib'")