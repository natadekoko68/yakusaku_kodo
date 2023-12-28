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
        dic[key][t] = (n, p, c)
    df = df.drop([key+"_n", key+"_p", key+"_c"], axis=1)

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

for p, q in it.product(keys, repeat=2):
    if (p == "saline") and (p != q) :
        print(f"{q}")
        for time in [15, 30, 60, 90]:
            kai_val = kai_rev((dic[p][time],dic[q][time]))
            print(f"{time}sec: {kai_val:.3f}", end=" ")
            if sps.chi2.ppf(q=0.999, df=1) < kai_val:
                print("p=0.001")
            elif sps.chi2.ppf(q=0.99, df=1) < kai_val:
                print("p=0.01")
            elif sps.chi2.ppf(q=0.95, df=1) < kai_val:
                print("p=0.05")
            else:
                print("ns")
