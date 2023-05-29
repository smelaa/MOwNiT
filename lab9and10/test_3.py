import equations_set as eq
from equations_set import TridiagonalMatrix
import pandas as pd
import numpy as np
from time import time

n = [i for i in range(3, 20)] + [50, 100, 150, 200, 300, 500, 1000]

x = [eq.get_x_probe(i) for i in n]

A_Gauss = [None for i in range(len(n))]
b_Gauss = [None for i in range(len(n))]
A_Thomas = []
b_Thomas = []

x_solved_Gauss = []
x_solved_Thomas = []

times_Gauss = []
times_Thomas = []

comp_max_Gauss = []
comp_max_Thomas = []

comp_sq_Gauss = []
comp_sq_Thomas = []

for i in range(len(n)):
    A_Gauss[i], b_Gauss[i] = eq.get_Ab_v3(n[i], x[i])
    A_Thomas.append(TridiagonalMatrix(A_Gauss[i]))
    b_Thomas.append(b_Gauss[i].copy())

    # solving Gauss
    start = time()
    res_Gauss = eq.gaussian_elimination(A_Gauss[i], b_Gauss[i])
    end = time()
    times_Gauss.append(end - start)

    x_solved_Gauss.append(res_Gauss.copy())

    # solving Thomas
    start = time()
    res_Thomas = eq.thomas(A_Thomas[i], b_Thomas[i])
    end = time()
    times_Thomas.append(end - start)

    x_solved_Thomas.append(res_Thomas.copy())

    comp_max_Gauss.append(eq.max_norm(x[i], x_solved_Gauss[i]))
    comp_sq_Gauss.append(eq.sq_norm(x[i], x_solved_Gauss[i]))
    comp_max_Thomas.append(eq.max_norm(x[i], x_solved_Thomas[i]))
    comp_sq_Thomas.append(eq.sq_norm(x[i], x_solved_Thomas[i]))

df_cmp_sq = dict()
df_cmp_max = dict()
df_cmp_times = dict()
for i in range(len(n)):
    df_cmp_sq["n={ni}".format(ni=n[i])] = {
        "Thomas algorithm": comp_sq_Thomas[i],
        "Gauss elimination": comp_sq_Gauss[i]
    }

    df_cmp_max["n={ni}".format(ni=n[i])] = {
        "Thomas algorithm": comp_max_Thomas[i],
        "Gauss elimination": comp_max_Gauss[i]
    }

    df_cmp_times["n={ni}".format(ni=n[i])] = {
        "Thomas algorithm": times_Thomas[i],
        "Gauss elimination": times_Gauss[i]
    }


data_frame_sq = pd.DataFrame(df_cmp_sq)
data_frame_max = pd.DataFrame(df_cmp_max)
data_frame_times = pd.DataFrame(df_cmp_times)

data_frame_sq.T.to_excel(excel_writer="./zadIII_sq.xlsx", sheet_name="norm")
data_frame_max.T.to_excel(excel_writer="./zadIII_max.xlsx", sheet_name="norm")
data_frame_times.T.to_excel(excel_writer="./zadIII_times.xlsx", sheet_name="times")
