import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load dataset
df = pd.read_csv("dataset.csv")

# Encode categorical columns
le_material = LabelEncoder()
le_location = LabelEncoder()
le_type = LabelEncoder()

df["Material"] = le_material.fit_transform(df["Material"])
df["Location"] = le_location.fit_transform(df["Location"])
df["Type"] = le_type.fit_transform(df["Type"])

X = df.drop("Cost", axis=1)
y = df["Cost"]

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model and encoders
joblib.dump(model, "model.pkl")
joblib.dump(le_material, "material.pkl")
joblib.dump(le_location, "location.pkl")
joblib.dump(le_type, "type.pkl")

print("Model trained successfully!")