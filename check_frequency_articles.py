import pandas as pd

import matplotlib.pyplot as plt

df = pd.read_csv("articles.csv")

df['date'] = pd.to_datetime(df['date'])
df['year_month'] = df['date'].dt.to_period('M')

year_month_counts = df.groupby('year_month').size()

plt.figure(figsize=(10, 6))
year_month_counts.plot(kind='bar')
plt.title('Frequency of Titles by Year and Month')
plt.xlabel('Year and Month')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
