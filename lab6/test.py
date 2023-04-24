import numpy as np
import approximation as approx
import pandas as pd

def f(x):
    return np.sin(x) * np.sin(2 * x ** 2 / np.pi)

interval = [-np.pi, 2 * np.pi]
m_degs= [2,3,5,7,10,15,20,25,30]
n_nodes=[5,7,10,15,20,30,40,50,80,100,200]
nodes = []

for i in n_nodes:
    nodes.append(approx.generate_points(i, interval, f))

errors_max=dict()
errors_mse=dict()
for m in m_degs:
    error_max=dict()
    error_mse=dict()
    for i in range(len(n_nodes)):
        poly=approx.approx(nodes[i], m, interval)
        approx.draw_approx(f, poly, interval, nodes[i],
                                 str(n_nodes[i]) + " punktów; "+str(m) + " st. wielomianów",
                                 "./plots/pt" + str(n_nodes[i])+"st" + str(m) + ".png")
        error_max[str(n_nodes[i])]=approx.max_error(f, poly, interval)
        error_mse[str(n_nodes[i])]=approx.mean_squared_error(f, poly, interval)
    errors_max[str(m)]=error_max.copy()
    errors_mse[str(m)]=error_mse.copy()

data_frame1=pd.DataFrame(errors_max)
data_frame2=pd.DataFrame(errors_mse)
data_frame1.to_excel(excel_writer="./tables/err_max.xlsx", sheet_name="max", float_format="%.4f")
data_frame2.to_excel(excel_writer="./tables/err_mse.xlsx", sheet_name="mse", float_format="%.4f")
