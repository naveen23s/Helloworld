import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load data
df = pd.read_csv('asl_data.csv')
X = df.drop('label', axis=1).values
y = df['label'].values

# Train the model
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X, y)

# Save the trained model
with open('asl_model.pkl', 'wb') as f:
    pickle.dump(clf, f)

print("Model trained and saved as asl_model.pkl")