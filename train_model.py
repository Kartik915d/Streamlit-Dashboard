import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import numpy as np

# Load dataset
df = pd.read_csv('Final_social_media_data_labeled.csv')

# Encode 'location_x'
encoder = LabelEncoder()
encoder.fit(df['location_x'])
with open('location_x_label_encoder.pkl', 'wb') as f:
    pickle.dump(encoder, f)
print("✅ Saved location_x_label_encoder.pkl")

df['location_x_encoded'] = encoder.transform(df['location_x'])

# Date columns list
date_cols = [
    'date_of_login_x', 'date_of_logout_x',
    'date_of_login_y', 'date_of_logout_y',
    'date_of_login_x', 'date_of_logout_z'
]

# Convert dates to numeric timestamps, fill missing with 0
for col in date_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce').astype(np.int64) // 10**9
        df[col] = df[col].fillna(0).astype(int)

# Drop non-numeric columns except encoded and date columns
drop_cols = [
    'email', 'username_x', 'username_y', 'username_z',
    'location_x', 'location_y', 'location_z',
    'interest_x', 'interest_y', 'interest_z'
]

# Create features X
X = df.drop(columns=drop_cols + ['target'])
X['location_x_encoded'] = df['location_x_encoded']

# Drop any column in X that may still have non-numeric types just in case
for col in X.columns:
    if X[col].dtype == 'object':
        print(f"Dropping non-numeric column: {col}")
        X = X.drop(columns=[col])

y = df['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

with open('model.pkl', 'wb') as f:
    pickle.dump(clf, f)

print("✅ Model and encoder saved")
print(f"Train accuracy: {clf.score(X_train, y_train):.4f}")
print(f"Test accuracy: {clf.score(X_test, y_test):.4f}")
