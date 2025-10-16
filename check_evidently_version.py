import pickle

# Assume your encoder variable is named 'encoder'
with open('platform_label_encoder.pkl', 'wb') as f:
    pickle.dump(encoder, f)

print("Saved platform_label_encoder.pkl")