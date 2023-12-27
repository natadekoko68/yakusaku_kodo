import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
import japanize_matplotlib
import warnings
warnings.simplefilter("ignore")

input = "/Users/kotaro/PycharmProjects/yakusaku1/input/"
df = pd.read_csv(input + "data_yakusaku_gakusyu.csv").drop('group_num', axis=1)
# output = "/Users/kotaro/Desktop/"
# output = "/Users/kotaro/Desktop/yakusaku_output/"
output = "./output/"

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

def make_dict(df):
    ret = {}
    a, b = make_label_value(df)
    for key in ["att", "fix", "rev"]:
        dict_temp = dict(labels=a[key], values=b[key])
        ret[key] = pd.DataFrame(dict_temp)
    return ret


def graph_all(df):
    dict = make_dict(df)
    cnt = 0
    lab = ["獲得","固定","再生"]
    fig = plt.figure(figsize=(12,5))
    order = ["1日目\n生理食塩水", "2日目\n生理食塩水", "1日目\nスコポラミン", "2日目\nスコポラミン"]
    for key in dict:
        ax = plt.subplot(1, 3, cnt+1)
        sns.swarmplot(dict[key], x="labels", y="values", order=order, palette="Set2", size=5, legend=False)
        sns.boxplot(dict[key], x="labels", y="values", color="white", order=order, legend=False)
        plt.title("実験1(" + lab[cnt] + ")")
        ax.set(xlabel='', ylabel='時間(sec)')
        plt.xticks(size=5)
        cnt += 1
    plt.tight_layout()
    plt.savefig(output + "実験1_all.jpg", dpi=300)

def graphs(df):
    dict = make_dict(df)
    cnt = 0
    lab = ["獲得", "固定", "再生"]
    order = ["1日目\n生理食塩水", "2日目\n生理食塩水", "1日目\nスコポラミン", "2日目\nスコポラミン"]
    for key in dict:
        fig = plt.figure()
        ax = plt.subplot(1, 1, 1)
        sns.swarmplot(dict[key], x="labels", y="values", order=order, palette="Set2", size=5)
        sns.boxplot(dict[key], x="labels", y="values", color="white", order=order)
        plt.title("実験1(" + lab[cnt] + ")")
        # plt.xticks(size=5)
        ax.set(xlabel='', ylabel='時間(sec)')
        plt.tight_layout()
        plt.savefig(output + "実験1("+lab[cnt]+").jpg", dpi=300)
        plt.close()
        cnt += 1

graph_all(df)
graphs(df)

