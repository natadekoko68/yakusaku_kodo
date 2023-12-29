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

input = '/Users/kotaro/PycharmProjects/yakusaku_kodo/input/data_yakusaku_chintsu.csv'
df = pd.read_csv(input)
output = "/Users/kotaro/Desktop/yakusaku_output/"
# output = "/Users/kotaro/PycharmProjects/yakusaku_kodo/output/"

keys = ["saline", "molphine", "naloxone", "ibuprofen"]

dic = {}

# print(df.shape)

for key in keys:
    dic[key] = {}
    n = []
    p = []
    c = []
    for i in range(len(df)):
        n.append(df.loc[i, key + "_n"])
        p.append(df.loc[i, key + "_p"])
        c.append(df.loc[i, key + "_c"])
        dic[key]["n"] = n
        dic[key]["p"] = p
        dic[key]["c"] = c
    df = df.drop([key+"_n", key+"_p", key+"_c"], axis=1)

ind = np.arange(4)    # the x locations for the groups
width = 0.35
ind_p = ind + width/2
ind_m = ind - width/2
ind_line = np.sort(np.concatenate([ind_p, ind_m]))
cnt = 1
fig = plt.figure(figsize=(12, 5))
fig.suptitle("投与薬剤と鎮痛効果の関係", fontsize=15)
fig.supxlabel("時間(min)")
fig.supylabel("匹")
for key in keys:
    ax = fig.add_subplot(1, 4, cnt)
    A = np.array(dic[key]["c"])
    B = np.array(dic[key]["p"])
    C = np.array(dic[key]["n"])
    p1 = ax.bar(ind, A, width, zorder=2, color=sns.color_palette("Blues", 3)[2], label="c")
    p2 = ax.bar(ind, B, width, bottom=A, zorder=2, color=sns.color_palette("Blues", 3)[1], label="p")
    p3 = ax.bar(ind, C, width, bottom=A+B, zorder=2, color=sns.color_palette("Blues", 3)[0], label="n")
    A_line = (np.insert(A, np.arange(4), A))
    B_line = (np.insert(B, np.arange(4), B)) + A_line
    C_line = (np.insert(C, np.arange(4), C)) + B_line
    ax.plot(ind_line, A_line, "k:", zorder=1)
    ax.plot(ind_line, B_line, "k:", zorder=1)
    ax.plot(ind_line, C_line, "k:", zorder=1)
    # plt.xlabel('時間(sec)')
    if key == "naloxone":
        key = f"molphine+\n{key}"
    plt.title(key)
    plt.xticks(ind, ('15', '30', '60', '90'))
    plt.yticks(np.arange(0, 31, 5))
    plt.legend(loc='upper left')
    plt.tight_layout()
    cnt += 1
plt.savefig(output + f"実験3_all.png",dpi=400)
plt.close()