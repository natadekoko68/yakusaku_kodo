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
print(font_prop.get_name())


input = '/Users/kotaro/PycharmProjects/yakusaku_kodo/input/data_yakusaku_chintsu.csv'
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
row_labels = ['15sec', '30sec', '60sec', "90sec"]

fig = plt.figure(figsize=(10, 5))
fig.suptitle("実験II(鎮痛)  $χ^2$検定結果",fontsize=20)
ax = fig.add_subplot(121)
ax.set_title(label='作用が強い場合(n+pとcの比較)',fontsize=17)
the_table = plt.table(cellText=results,
                      colWidths=[0.5]*3,
                      rowLabels=row_labels,
                      colLabels=col_labels,
                      loc='center')
the_table.auto_set_font_size(False)
the_table.set_fontsize(12)
the_table.scale(0.8, 4)
plt.axis("off")

ax = fig.add_subplot(122)
ax.set_title(label='作用が弱い場合(nとp+cの比較)',fontsize=17)
the_table = plt.table(cellText=results2,
                      colWidths=[0.5]*3,
                      rowLabels=row_labels,
                      colLabels=col_labels,
                      loc='center')
the_table.auto_set_font_size(False)
the_table.set_fontsize(12)
the_table.scale(0.8, 4)
plt.axis("off")
plt.tight_layout()

plt.savefig("/Users/kotaro/Desktop/table1.jpg", dpi=300)
# plt.savefig('matplotlib-table', bbox_inches='tight', pad_inches=0.05)
# plt.show()