import pandas as pd
import equations as eq


def f(x):
    return x**12+x**15

def f_der(x):
    return 12*x**11+15*x**14

interval=(-1.2, 1)

eps_values=[0.1, 1e-03, 1e-05, 1e-07, 1e-09, 1e-12, 1e-15]

it_cnt=dict()
found=dict()

for eps in eps_values:
    x0=-1.2
    while x0<=1:
        unit_found=dict()
        unit_itcnt=dict()
        xf, it=eq.newton_solving_diff(f, f_der, x0, eps)
        unit_found["N; k. przyrostowe"]=xf
        unit_itcnt["N; k. przyrostowe"]=it
        xf, it=eq.newton_solving_fval(f, f_der, x0, eps)
        unit_found["N; k. wartości f"]=xf
        unit_itcnt["N; k. wartości f"]=it
        xf, it=eq.secant_solving_diff(f, x0, interval[1], eps)
        unit_found["S; x0, b; k. przyrostowe"]=xf
        unit_itcnt["S; x0, b; k. przyrostowe"]=it
        xf, it=eq.secant_solving_fval(f, x0, interval[1], eps)
        unit_found["S; x0, b; k. wartości f"]=xf
        unit_itcnt["S; x0, b; k. wartości f"]=it
        xf, it=eq.secant_solving_diff(f, interval[0], x0, eps)
        unit_found["S; a, x0; k. przyrostowe"]=xf
        unit_itcnt["S; a, x0; k. przyrostowe"]=it
        xf, it=eq.secant_solving_fval(f, interval[0], x0, eps)
        unit_found["S; a, x0; k. wartości f"]=xf
        unit_itcnt["S; a, x0; k. wartości f"]=it
        
        it_cnt["x0: {x0}; epsilon: {eps}".format(x0=round(x0,1), eps=eps)]=unit_itcnt.copy()
        found["x0: {x0}; epsilon: {eps}".format(x0=round(x0,1), eps=eps)]=unit_found.copy()
        x0+=0.1

data_frame_found=pd.DataFrame(found)
data_frame_itcnt=pd.DataFrame(it_cnt)
data_frame_found.T.to_excel(excel_writer="./pierwiastki.xlsx", sheet_name="pierw", float_format="%.6f")
data_frame_itcnt.T.to_excel(excel_writer="./iteracje.xlsx", sheet_name="itcnt")
