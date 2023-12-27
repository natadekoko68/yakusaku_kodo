import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import japanize_matplotlib
import warnings
warnings.simplefilter("ignore")

input = '/Users/kotaro/PycharmProjects/yakusaku_kodo/input/data_yakusaku_saimin.csv'
df_exp2 = pd.read_csv(input).drop("group_num", axis=1)
output = "/Users/kotaro/Desktop/yakusaku_output/"
output = "./output/"

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
    sns.violinplot(df, x="labels", y="values", color="white")
    sns.swarmplot(df, x="labels", y="values", palette="Set2")
    ax.set(xlabel="投与薬物", ylabel="時間(sec)")
    plt.title("投与薬物と正向反射消失時間の関係")

    plt.tight_layout()
    plt.savefig(output + '実験2.jpg',dpi=300)
    plt.show()

if __name__ == '__main__':
    graph_exp2(df_exp2)



