import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
import japanize_matplotlib
import warnings
warnings.simplefilter("ignore")

input = "/Users/kotaro/PycharmProjects/yakusaku_kodo/input/"
df = pd.read_csv(input + "data_yakusaku_gakusyu.csv").drop('group_num', axis=1)
output = "/Users/kotaro/Desktop/yakusaku_output/"
# output = "./output/"

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


def graph_all(df, datatype=sns.violinplot):
    dict = make_dict(df)
    cnt = 1
    lab = ["獲得", "固定", "再生"]
    fig = plt.figure(figsize=(10,10))
    fig.suptitle("学習実験",size=18)
    order = ["1日目\n生理食塩水", "2日目\n生理食塩水", "1日目\nスコポラミン", "2日目\nスコポラミン"]
    for key in dict:
        ax = plt.subplot(2, 2, cnt)
        sns.swarmplot(dict[key], x="labels", y="values", order=order, palette="Set2", size=5, legend=False)
        datatype(dict[key], x="labels", y="values", color="white", order=order, legend=False, inner="quartile")
        plt.title("実験1(" + lab[cnt-1] + ")", fontsize=13)
        ax.set(xlabel='', ylabel='時間(sec)')
        plt.xticks(size=10)
        plt.ylim([-20, 350])
        plt.plot([0.5, 2.5], [320, 320], marker="|", color="black")
        if cnt == 1:
            plt.text(1.5, 325, "p < 0.001", color="black", horizontalalignment="center", verticalalignment="bottom")
        else:
            plt.text(1.5, 325, "n.s.", color="black", horizontalalignment="center", verticalalignment="bottom")
        cnt += 1
    plt.tight_layout()
    plt.savefig(output + f"実験1_all({str(datatype).split()[-3]}).jpg", dpi=300)

def graphs(df):
    dict = make_dict(df)
    cnt = 0
    lab = ["獲得", "固定", "再生"]
    order = ["1日目\n生理食塩水", "2日目\n生理食塩水", "1日目\nスコポラミン", "2日目\nスコポラミン"]
    for key in dict:
        fig = plt.figure()
        ax = plt.subplot(1, 1, 1)
        sns.swarmplot(dict[key], x="labels", y="values", order=order, palette="Set2", size=5)
        sns.violinplot(dict[key], x="labels", y="values", color="white", order=order, inner="quartile")
        plt.title("実験1(" + lab[cnt] + ")")
        ax.set(xlabel='', ylabel='時間(sec)')
        plt.tight_layout()
        plt.savefig(output + "実験1("+lab[cnt]+").jpg", dpi=300)
        plt.close()
        cnt += 1


if __name__ == "__main__":
    graph_all(df, datatype=sns.violinplot)
    # print(make_dict(df))
