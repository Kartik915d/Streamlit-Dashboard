import pandas as pd

df = pd.read_csv('Final_social_media_data.csv')
df['target'] = (df['followers_x'] > 1000).astype(int)  # Example label based on followers_x threshold
df.to_csv('Final_social_media_data_labeled.csv', index=False)

print("Created labeled dataset: Final_social_media_data_labeled.csv")
