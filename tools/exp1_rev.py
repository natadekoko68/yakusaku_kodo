import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
import japanize_matplotlib
import numpy as np
import warnings
warnings.simplefilter("ignore")
import sys
from scipy.stats import tukey_hsd

input = "/Users/kotaro/PycharmProjects/yakusaku_kodo/input/"
df = pd.read_csv(input + "data_yakusaku_gakusyu.csv").drop('group_num', axis=1)
output = "/Users/kotaro/Desktop/"

print(df)


dic = {}

labs = ["att", "fix", "rev"]
days = ["day1", "day2"]
groups = ["sa", "sco"]

for key in labs:
    dic[key] = {}
    for group in groups:
        dic[key][group] = {}
        for day in days:
            for col in df.columns:
                if (key in col) & (day in col) & (group in col):
                    dic[key][group][day] = list(df[col])
# print(dic)

diff = {}
for lab in labs:
    diff[lab] = {}
    for group in groups:
        diff[lab][group] = {}


for lab in labs:
    for group in groups:
        diff[lab][group] = (np.array(list(dic[lab][group]["day2"])) - np.array(list(dic[lab][group]["day1"])))

for lab in labs:
    print(tukey_hsd(diff[lab]["sa"], diff[lab]["sco"]))



