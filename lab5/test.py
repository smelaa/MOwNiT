import numpy as np
import approximation as approx
import pandas as pd
import dataframe_image as dfi

def f(x):
    return np.sin(x) * np.sin(2 * x ** 2 / np.pi)

interval = [-np.pi, 2 * np.pi]
m_degs= [2,3,4,5,6,7,8,9]
n_nodes=[10,20,30,40,50,60,70,80,90,100]
nodes = []

for i in n_nodes:
    nodes.append(approx.generate_points(i, interval, f))

errors_max= {"l. punktow": n_nodes}
errors_mse={"l. punktow": n_nodes}
for m in m_degs:
    error_max=[]
    error_mse=[]
    for i in range(len(n_nodes)):
        poly=approx.approx(nodes[i], m)
        approx.draw_interpolation(f, poly, interval, nodes[i],
                                 str(n_nodes[i]) + " punktów; "+str(m) + " st. wielomianów",
                                 "./plots/pt" + str(n_nodes[i])+"st" + str(m) + ".png")
        error_max.append(approx.max_error(f, poly, interval))
        error_mse.append(approx.mean_squared_error(f, poly, interval))
    errors_max[str(m)]=error_max.copy()
    errors_mse[str(m)]=error_mse.copy()

data_frame1=pd.DataFrame(errors_max)
data_frame2=pd.DataFrame(errors_mse)
data_frame1 = data_frame1.style.set_caption("błąd maksymalny").format(precision=4)
data_frame2 = data_frame2.style.set_caption("błąd średniokwadratowy").format(precision=4)
dfi.export(data_frame1, "tables/errors_max.png")
dfi.export(data_frame2, "tables/errors_mse.png")

