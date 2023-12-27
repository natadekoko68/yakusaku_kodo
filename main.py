import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
import sys
import japanize_matplotlib

input = "/Users/kotaro/PycharmProjects/yakusaku1/input/"
df = pd.read_csv(input + "data_yakusaku_gakusyu.csv").drop('group_num', axis=1)

print(df.columns)

att_col = []
fix_col = []
rev_col = []

for col in df.columns:
    if "att" in col:
        att_col.append(col)
    if "fix" in col:
        fix_col.append(col)
    if "rev" in col:
        rev_col.append(col)

for string in att_col:
    print(re.search("day[0-9]_.+_.+", string))

labels_att = []
values_att = []
labels_fix = []
values_fix = []
labels_rev = []
values_rev = []
for col in df.columns:
    if re.search("day[0-9]_att_.+", col):
        for i in range(len(df[col])):
            label = ""
            if "day1" in col:
                label += "1日目"
            else:
                label += "2日目"
            label += "\n"
            if "sa" in col:
                label += "生理食塩水"
            else:
                label += "スコポラミン"
            labels_att.append(label)
            values_att.append(df.loc[i, col])
    elif re.search("day[0-9]_fix_.+", col):
        for i in range(len(df[col])):
            label = ""
            if "day1" in col:
                label += "1日目"
            else:
                label += "2日目"
            label += "\n"
            if "sa" in col:
                label += "生理食塩水"
            else:
                label += "スコポラミン"
            labels_fix.append(label)
            values_fix.append(df.loc[i, col])
    elif re.search("day[0-9]_rev_.+", col):
        for i in range(len(df[col])):
            label = ""
            if "day1" in col:
                label += "1日目"
            else:
                label += "2日目"
            label += "\n"
            if "sa" in col:
                label += "生理食塩水"
            else:
                label += "スコポラミン"
            labels_rev.append(label)
            values_rev.append(df.loc[i, col])

def make_label_value(df):
    labels = {}
    values = {}
    for key in ["att", "fix", "rev"]:
        labels[key] = []
        values[key] = []
        for col in df.columns:
            for i in range(len(df[col])):
                if re.search("day[0-9]_" + key + "_.+", col):
                    label = ""
                    if "day1" in col:
                        label += "1日目"
                    else:
                        label += "2日目"
                    label += "\n"
                    if "sa" in col:
                        label += "生理食塩水"
                    else:
                        label += "スコポラミン"
                    labels[key].append(label)
                    values[key].append(df.loc[i, col])
    return labels, values



dict_att = dict(labels=labels_att, values=values_att)
df_att = pd.DataFrame(dict_att)
sns.swarmplot(df_att, x="labels", y="values", palette="Set2")
sns.boxplot(df_att, x="labels", y="values", color="white")
plt.title("実験1(獲得)")
plt.tight_layout()
plt.savefig("/Users/kotaro/Desktop/獲得.jpg", dpi=300)
plt.show()

dict_fix = dict(labels=labels_fix, values=values_fix)
df_fix = pd.DataFrame(dict_fix)
sns.swarmplot(df_fix, x="labels", y="values", palette="Set2")
sns.boxplot(df_fix, x="labels", y="values", color="white")
plt.title("実験1(固定)")
plt.tight_layout()
plt.savefig("/Users/kotaro/Desktop/固定.jpg", dpi=300)
plt.show()

dict_rev = dict(labels=labels_rev, values=values_rev)
df_rev = pd.DataFrame(dict_rev)
sns.swarmplot(df_rev, x="labels", y="values", palette="Set2")
sns.boxplot(df_rev, x="labels", y="values", color="white")
plt.title("実験1(再生)")
plt.tight_layout()
plt.savefig("/Users/kotaro/Desktop/再生.jpg", dpi=300)
plt.show()
