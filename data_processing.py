import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

# Load your dataset
df = pd.read_csv('Final_social_media_data.csv')

# Replace 'target' with your actual label column name in the dataset
X = df.drop(columns=['target'])
y = df['target']

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# Initialize and train a Random Forest classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Save the trained model
with open('model.pkl', 'wb') as f:
    pickle.dump(clf, f)

print("✅ Model trained and saved as model.pkl")
print(f"Train accuracy: {clf.score(X_train, y_train):.4f}")
print(f"Test accuracy: {clf.score(X_test, y_test):.4f}")
