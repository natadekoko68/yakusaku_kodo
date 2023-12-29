import pandas as pd
import pylab as p
import seaborn as sns
import matplotlib.pyplot as plt
import japanize_matplotlib
from scipy import stats
import scipy.stats as sps
import itertools as it
import warnings

warnings.simplefilter("ignore")
import numpy as np

df_init = pd.read_csv('/Users/kotaro/PycharmProjects/yakusaku_kodo/input/data_yakusaku_writhing.csv')
df_init = df_init.drop(columns=['Unnamed: 0'])

labels = []
values = []
for col in df_init.columns:
    for i in range(len(df_init)):
        labels.append(col[:-1])
        values.append(df_init.loc[i, col])

dic = dict(labels=labels, values=values)

df = pd.DataFrame(dic)

fig = plt.figure()
sns.swarmplot(data=df, x='labels', y='values', palette="Set2", size=4)
sns.violinplot(data=df, x='labels', y='values', color="white", inner="quart")
plt.title("投与薬剤ごとのWrithing応答回数")
plt.xlabel("投与薬剤")
plt.ylabel("Writhing応答(回/10分)")
plt.plot([1, 2], [72, 72], marker="|", color="k")
plt.plot([0, 1], [77, 77], marker="|", color="k")
plt.plot([0, 2], [83, 83], marker="|", color="k")
plt.text(1.5, 72.7, "p < 0.05", horizontalalignment="center", verticalalignment="bottom")
plt.text(0.5, 77.7, "p < 0.001", horizontalalignment="center", verticalalignment="bottom")
plt.text(1, 83.7, "p < 0.001", horizontalalignment="center", verticalalignment="bottom")
plt.ylim([-18, 90])

plt.tight_layout()
plt.savefig('/Users/kotaro/Desktop/writhing.jpg', dpi=400)
plt.show()

stat = {}

for key in ["saline", "morphine", "ibuprofen"]:
    stat[key] = df[(df["labels"] == key) & (~df["values"].isna())]["values"].values

from scipy.stats import tukey_hsd

print(tukey_hsd(stat["saline"], stat["morphine"], stat["ibuprofen"]))

print(f"saline  平均:{stat['saline'].mean():.3f}  分散:{stat['saline'].std()**2:.3f}")
print(f"morphine  平均:{stat['morphine'].mean():.3f}  分散:{stat['morphine'].std()**2:.3f}")
print(f"ibuprofen  平均:{stat['ibuprofen'].mean():.3f}  分散:{stat['ibuprofen'].std()**2:.3f}")
