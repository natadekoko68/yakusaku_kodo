import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import japanize_matplotlib
from scipy import stats
import scipy.stats as sps
import itertools as it
import warnings
warnings.simplefilter("ignore")
import numpy as np
import matplotlib.font_manager as fm
FONT_PATH = "/Users/kotaro/PycharmProjects/yakusaku_kodo/input/Noto_Sans_JP/static/NotoSansJP-ExtraLight.ttf"
fm.fontManager.addfont(FONT_PATH)
font_prop = fm.FontProperties(fname=FONT_PATH)
plt.rcParams["font.family"] = font_prop.get_name()
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec


input = '/Users/kotaro/PycharmProjects/yakusaku_kodo/input/data_yakusaku_chintsu2.csv'
df = pd.read_csv(input)
output = "/Users/kotaro/Desktop/yakusaku_output/"
# output = "./output/"

keys = ["saline", "molphine", "naloxone", "ibuprofen"]

dic = {}

for key in keys:
    dic[key] = {}
    for i in range(len(df)):
        t = df.loc[i, "time_after_injection"]
        n = df.loc[i, key + "_n"]
        p = df.loc[i, key + "_p"]
        c = df.loc[i, key + "_c"]
        dic[key][t] = (n + p, c)
        # dic[key][t] = (n, p + c)
    # df = df.drop([key+"_n", key+"_p", key+"_c"], axis=1)

def kai_3(arrs):
    ret = 0
    for i in range(3):
        for j in range(2):
            C = arrs[0][i] + arrs[1][i]
            R = arrs[j][0] + arrs[j][1] + arrs[j][2]
            N = sum(arrs[0]) + sum(arrs[1])
            ret += (arrs[j][i] - (C*R/N))**2/(C*R/N)
    return ret

def kai(arrs):
    ret = 0
    for i in range(2):
        for j in range(2):
            C = arrs[0][i] + arrs[1][i]
            R = arrs[j][0] + arrs[j][1]
            N = sum(arrs[0]) + sum(arrs[1])
            ret += (arrs[j][i] - ((C*R)/N))**2/(C*R/N)
    return ret

def kai_rev(arrs):
    a = arrs[0][0]
    b = arrs[0][1]
    c = arrs[1][0]
    d = arrs[1][1]
    N = a + b + c + d
    ret = (a*d-b*c)**2*N/((a+b)*(c+d)*(a+c)*(b+d))
    return ret


results = np.zeros((4, 3))
times = [15, 30, 60, 90]
print(results)
draws = ["molphine", "naloxone", "ibuprofen"]
for j in range(len(draws)):
    q = draws[j]
    for i in range(len(times)):
        time = times[i]
        kai_val = kai_rev((dic["saline"][time], dic[q][time]))
        print(f"{time}sec: {kai_val:.3f}", end=" ")
        results[i,j] = f"{kai_val:.3f}"
        if sps.chi2.ppf(q=0.999, df=1) < kai_val:
            print("p=0.001")
        elif sps.chi2.ppf(q=0.99, df=1) < kai_val:
            print("p=0.01")
        elif sps.chi2.ppf(q=0.95, df=1) < kai_val:
            print("p=0.05")
        else:
            print("ns")

for key in keys:
    dic[key] = {}
    for i in range(len(df)):
        t = df.loc[i, "time_after_injection"]
        n = df.loc[i, key + "_n"]
        p = df.loc[i, key + "_p"]
        c = df.loc[i, key + "_c"]
        dic[key][t] = (n, p + c)
    df = df.drop([key+"_n", key+"_p", key+"_c"], axis=1)

results2 = np.zeros((4, 3))
times = [15, 30, 60, 90]
draws = ["molphine", "naloxone", "ibuprofen"]
for j in range(len(draws)):
    q = draws[j]
    for i in range(len(times)):
        time = times[i]
        kai_val = kai_rev((dic["saline"][time], dic[q][time]))
        print(f"{time}sec: {kai_val:.3f}", end=" ")
        results2[i,j] = f"{kai_val:.3f}"
        if sps.chi2.ppf(q=0.999, df=1) < kai_val:
            print("p=0.001")
        elif sps.chi2.ppf(q=0.99, df=1) < kai_val:
            print("p=0.01")
        elif sps.chi2.ppf(q=0.95, df=1) < kai_val:
            print("p=0.05")
        else:
            print("ns")

print(results)
print(results2)

col_labels = ['molphine', 'molphine\n+naloxone', 'ibuprofen']
row_labels = ['15min', '30min', '60min', "90min"]

color_high = "#ff7f7f"
color_medium = "#ffb2b2"
color_low = "#ffc1c1"

fig = plt.figure(figsize=(10, 5))
gs_master = GridSpec(nrows=2, ncols=2, height_ratios=[20, 1])
gs_1 = GridSpecFromSubplotSpec(nrows=1, ncols=1, subplot_spec=gs_master[0, 0])
fig.suptitle("実験II(鎮痛)  $χ^2$検定結果", fontsize=15)
ax = fig.add_subplot(gs_1[:, :])
# ax.set_title(label='作用が強い場合(n+pとcの比較)',fontsize=17)
plt.title('作用が強い場合(n+pとcの比較)')
table = plt.table(cellText=results,
                      colWidths=[0.5]*3,
                      rowLabels=row_labels,
                      colLabels=col_labels,
                      loc='center')
for i in range(0, 3):
    for j in range(1, 5):
        if results[j-1, i] > sps.chi2.ppf(q=0.999, df=1):
            table[(j, i)].set_facecolor(color_high)
        elif results[j-1, i] > sps.chi2.ppf(q=0.99, df=1):
            table[(j, i)].set_facecolor(color_medium)
        elif results[j-1, i] > sps.chi2.ppf(q=0.95, df=1):
            table[(j, i)].set_facecolor(color_low)
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(0.8, 4)
plt.axis("off")

gs_2 = GridSpecFromSubplotSpec(nrows=1, ncols=1, subplot_spec=gs_master[0, 1])
axes_2 = fig.add_subplot(gs_2[:, :])
# ax.set_title(label='作用が弱い場合(nとp+cの比較)',fontsize=17)
plt.title('作用が強い場合(n+pとcの比較)')
table = plt.table(cellText=results2,
                      colWidths=[0.5]*3,
                      rowLabels=row_labels,
                      colLabels=col_labels,
                      loc='center')
for i in range(0, 3):
    for j in range(1, 5):
        if results[j-1, i] > sps.chi2.ppf(q=0.999, df=1):
            table[(j, i)].set_facecolor(color_high)
        elif results[j-1, i] > sps.chi2.ppf(q=0.99, df=1):
            table[(j, i)].set_facecolor(color_medium)
        elif results[j-1, i] > sps.chi2.ppf(q=0.95, df=1):
            table[(j, i)].set_facecolor(color_low)
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(0.8, 4)
plt.axis("off")
plt.tight_layout()

gs_3 = GridSpecFromSubplotSpec(nrows=1, ncols=1, subplot_spec=gs_master[1, 0:2])
axes_3 = fig.add_subplot(gs_3[:, :])
plt.text(0.7, 0.0, r"$\blacksquare$", color=color_high)
plt.text(0.7, 0.0, "     p<0.001")
plt.text(0.8, 0, r"$\blacksquare$", color=color_medium)
plt.text(0.8, 0, "     p<0.01")
plt.text(0.9, 0, r"$\blacksquare$", color=color_low)
plt.text(0.9, 0, "     p<0.05")
plt.axis("off")
plt.tight_layout()

plt.savefig("/Users/kotaro/Desktop/table1.jpg", dpi=400)
# plt.savefig('matplotlib-table', bbox_inches='tight', pad_inches=0.05)
# plt.show()