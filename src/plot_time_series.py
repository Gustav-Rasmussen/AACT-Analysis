from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
# from scipy.optimize import curve_fit

# load file
df = pd.read_csv("Obesity_time_series.csv")

# convert to datetime
df.drop(columns = ["Unnamed: 0"], inplace=True)
df['Date'] = pd.to_datetime(df['Date'], format="%Y%m%d")

# Plot
print(df.head())

# plt.figure(figsize=(12, 6))

'''
ax = sns.lineplot(x="Date",
                  y="Obesity",
                  data=df
                  )
'''

'''
ax = sns.lineplot(x="Date",
                     y="Obesity",
                     data=df,
                     marker=11
                     )
'''

# ax.axes.set_title(f"AACT project - Obesity - US", fontsize=25)
# l = ax.set_xticklabels(ax.get_xticklabels(), rotation=75, fontsize=15)
# ax.set_xlabel("Date", fontsize=20)
# ax.set_ylabel("Counts", fontsize=20)
# plt.tight_layout()
# plt.savefig('img/obesity_us.png')


# Tail-rolling average transform

# df.Obesity = df.Obesity.ewm(span=3, adjust=False).mean()  # rolling(21).mean()
#df.Obesity = df.Obesity.mean()
print(df.Obesity.head(10))
# plot original and transformed dataset

ax = sns.lineplot(x="Date",
                     y="Obesity",
                     data=df,
                     marker=11
                     )

plt.show()

