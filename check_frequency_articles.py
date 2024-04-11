import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("articles.csv")

df['date'] = pd.to_datetime(df['date'])

df['year'] = df['date'].dt.year

year_counts = df.groupby('year').size()

plt.figure(figsize=(10, 6))
year_counts.plot(kind='bar')
plt.title('Frequency of Titles by Year')
plt.xlabel('Year')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
