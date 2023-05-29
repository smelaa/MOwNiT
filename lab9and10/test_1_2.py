import equations_set as eq
import pandas as pd
import numpy as np
from time import time

n = [i for i in range(3, 20)] + [50, 100, 150, 200, 300, 500]

prec = [np.float16, np.float32, np.float64]
prec_names = ["np.float16", "np.float32", "np.float64"]

x = [[eq.get_x_probe(i, q) for q in prec] for i in n]

Av1 = [[None for q in range(len(prec))] for _ in range(len(n))]
bv1 = [[None for q in range(len(prec))] for _ in range(len(n))]
Av2 = [[None for q in range(len(prec))] for _ in range(len(n))]
bv2 = [[None for q in range(len(prec))] for _ in range(len(n))]

x_solved_v1 = [[None for q in range(len(prec))] for _ in range(len(n))]
x_solved_v2 = [[None for q in range(len(prec))] for _ in range(len(n))]

comp_max_v1 = [[None for q in range(len(prec))] for _ in range(len(n))]
comp_max_v2 = [[None for q in range(len(prec))] for _ in range(len(n))]
comp_sq_v1 = [[None for q in range(len(prec))] for _ in range(len(n))]
comp_sq_v2 = [[None for q in range(len(prec))] for _ in range(len(n))]

for i in range(len(n)):
    for j in range(len(prec)):
        Av1[i][j], bv1[i][j] = eq.get_Ab_v1(n[i], prec[j], x[i][j])
        Av2[i][j], bv2[i][j] = eq.get_Ab_v2(n[i], prec[j], x[i][j])

        x_solved_v1[i][j] = eq.gaussian_elimination(Av1[i][j], bv1[i][j])
        x_solved_v2[i][j] = eq.gaussian_elimination(Av2[i][j], bv2[i][j])

        comp_max_v1[i][j] = eq.max_norm(x[i][j], x_solved_v1[i][j])
        comp_max_v2[i][j] = eq.max_norm(x[i][j], x_solved_v2[i][j])
        comp_sq_v1[i][j] = eq.sq_norm(x[i][j], x_solved_v1[i][j])
        comp_sq_v2[i][j] = eq.sq_norm(x[i][j], x_solved_v2[i][j])

df_cmp_sq1 = dict()
df_cmp_max1 = dict()
df_cmp_sq2 = dict()
df_cmp_max2 = dict()
for i in range(len(n)):
    df_cmp_sq1_tmp = dict()
    df_cmp_max1_tmp = dict()
    df_cmp_sq2_tmp = dict()
    df_cmp_max2_tmp = dict()
    for p in range(len(prec)):
        df_cmp_sq1_tmp["prec: " + prec_names[p]] = str(comp_sq_v1[i][p])
        df_cmp_max1_tmp["prec: " + prec_names[p]] = str(comp_max_v1[i][p])
        df_cmp_sq2_tmp["prec: " + prec_names[p]] = str(comp_sq_v2[i][p])
        df_cmp_max2_tmp["prec: " + prec_names[p]] = str(comp_max_v2[i][p])
    df_cmp_sq1["n={ni}".format(ni=n[i])] = df_cmp_sq1_tmp.copy()
    df_cmp_max1["n={ni}".format(ni=n[i])] = df_cmp_max1_tmp.copy()
    df_cmp_sq2["n={ni}".format(ni=n[i])] = df_cmp_sq2_tmp.copy()
    df_cmp_max2["n={ni}".format(ni=n[i])] = df_cmp_max2_tmp.copy()

data_frame_sq1 = pd.DataFrame(df_cmp_sq1)
data_frame_max1 = pd.DataFrame(df_cmp_max1)
data_frame_sq2 = pd.DataFrame(df_cmp_sq2)
data_frame_max2 = pd.DataFrame(df_cmp_max2)
data_frame_sq1.T.to_excel(excel_writer="./zadI_sq.xlsx", sheet_name="norm")
data_frame_max1.T.to_excel(excel_writer="./zadI_max.xlsx", sheet_name="norm")
data_frame_sq2.T.to_excel(excel_writer="./zadII_sq.xlsx", sheet_name="norm")
data_frame_max2.T.to_excel(excel_writer="./zadII_max.xlsx", sheet_name="norm")

df_cmp_cond= dict()
for i in range (len(n)):
    df_cmp_cond["n={ni}".format(ni=n[i])] = {
        "Zadanie I": eq.cond_number(Av1[i][1]),
        "Zadanie II": eq.cond_number(Av2[i][1])
    }
data_frame_cond = pd.DataFrame(df_cmp_cond)

data_frame_cond.T.to_excel(excel_writer="./condI_II.xlsx", sheet_name="cond")