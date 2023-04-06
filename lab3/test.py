import interpolation as inter
import hermite
import numpy as np
import pandas as pd
import dataframe_image as dfi

def f(x):
    return np.sin(x) * np.sin(2 * x ** 2 / np.pi)

def der(x):
    return 4*x*np.sin(x)*np.cos(2*x**2/np.pi)/np.pi + np.sin(2*x**2/np.pi)*np.cos(x)

def generate_plots(f, n_nodes, nodes_reg_1der, nodes_czyb_1der, interval):
    for i in range(len(n_nodes)):
        inter.draw_interpolation(f, hermite.hermite_interpolation(nodes_reg_1der[i]), interval, nodes_reg_1der[i],
                                 "hermite; " + str(n_nodes[i]) + " węzłów równomiernych",
                                 "./plots/ht_reg1d" + str(n_nodes[i]) + ".png")
        inter.draw_interpolation(f, hermite.hermite_interpolation(nodes_czyb_1der[i]), interval, nodes_czyb_1der[i],
                                 "hermite; " + str(n_nodes[i]) + " węzłów Czybyszewa",
                                 "./plots/ht_czyb1d" + str(n_nodes[i]) + ".png")

def generate_error_table(f, inter_f, error_f, n_nodes, nodes_reg, nodes_czyb, interval, table_name, file_name):
    reg_errors=[]
    czyb_errors=[]

    for i in range(len(n_nodes)):
        reg_errors.append(error_f(f, inter_f(nodes_reg[i]), interval))
        czyb_errors.append(error_f(f, inter_f(nodes_czyb[i]), interval))

    data = {'l. węzłów': n_nodes,
            'równomiernie': reg_errors,
            'zg. z 0 Czyb.': czyb_errors}
    data_frame=pd.DataFrame(data)
    data_frame=np.round(data_frame, decimals=4)
    data_frame = data_frame.style.set_caption(table_name).format({
        'równomiernie': '{:,.4f}'.format,
        'zg. z 0 Czyb.': '{:,.4f}'.format
    })
    dfi.export(data_frame, file_name)

interval = [-np.pi, 2 * np.pi]
n_nodes = [3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20]
nodes_reg_1der = []
nodes_czyb_1der = []

for i in n_nodes:
    nodes_reg_1der.append(hermite.generate_points_1stderiv(i, interval, inter.generate_regularly, f, der))
    nodes_czyb_1der.append(hermite.generate_points_1stderiv(i, interval, inter.generate_czybyszow, f,der))


generate_plots(f, n_nodes, nodes_reg_1der, nodes_czyb_1der, interval)
generate_error_table(f,hermite.hermite_interpolation,inter.max_error,n_nodes, nodes_reg_1der, nodes_czyb_1der, interval, "Hermite; bład maksymalny", "./tables/h_max.png")
generate_error_table(f,hermite.hermite_interpolation,inter.mean_squared_error,n_nodes, nodes_reg_1der, nodes_czyb_1der, interval, "Hermite; bład średniokwadratowy", "./tables/h_mes.png")
