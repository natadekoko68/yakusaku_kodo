import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import japanize_matplotlib
import warnings
warnings.simplefilter("ignore")

input = '/Users/kotaro/PycharmProjects/yakusaku_kodo/input/data_yakusaku_saimin.csv'
df_exp2 = pd.read_csv(input).drop("group_num", axis=1)
output = "/Users/kotaro/Desktop/yakusaku_output/"
# output = "/Users/kotaro/PycharmProjects/yakusaku_kodo/output/"

def graph_exp2(df):
    labels = []
    values = []

    for col in df.columns:
        for i in range(len(df)):
            labels.append(col)
            values.append(df.loc[i,col])

    dic = dict(labels=labels, values=values)
    df = pd.DataFrame.from_dict(dic)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    sns.violinplot(df, x="labels", y="values", color="white",inner="quartile")
    sns.swarmplot(df, x="labels", y="values", palette="Set2")
    ax.set(xlabel="投与薬物", ylabel="時間(sec)")
    plt.title("投与薬物と正向反射消失時間の関係")
    plt.plot([0, 1], [140, 140], marker="|", color="k")
    plt.plot([0, 2], [150, 150], marker="|", color="k")
    plt.plot([0, 3], [160, 160], marker="|", color="k")
    plt.text(0.5, 140.7, "p < 0.001", horizontalalignment="center", verticalalignment="bottom")
    plt.text(1, 150.7, "p < 0.001", horizontalalignment="center", verticalalignment="bottom")
    plt.text(1.5, 160.7, "n.s.", horizontalalignment="center", verticalalignment="bottom")

    plt.tight_layout()
    plt.savefig(output + '実験2.jpg', dpi=400)
    plt.show()

def make_df(df):
    labels = []
    values = []

    for col in df.columns:
        for i in range(len(df)):
            labels.append(col)
            values.append(df.loc[i,col])

    dic = dict(labels=labels, values=values)
    df2 = pd.DataFrame.from_dict(dic)
    return df2


from scipy.stats import tukey_hsd

def stat(df):
    stat_dic = {}
    for key in df["labels"].unique():
        stat_dic[key] = list(df[df["labels"] == key]["values"])
    print(stat_dic)
    a = tukey_hsd(stat_dic['saline'],stat_dic['chlorpromazine'],stat_dic['diazepam'],stat_dic['caffeine'])
    print(a)
    return a


if __name__ == '__main__':
    # df2 = make_df(df_exp2)
    # graph_exp2(df_exp2)
    # # stat(df2)
    # # print(stat(df2).pvalue)
    df = make_df(df_exp2)

    print(f'{df[df["labels"] == "saline"]["values"].mean():.3f}')
    print(f'{df[df["labels"] == "chlorpromazine"]["values"].mean():.3f}')
    print(f'{df[df["labels"] == "diazepam"]["values"].mean():.3f}')
    print(f'{df[df["labels"] == "caffeine"]["values"].mean():.3f}')




