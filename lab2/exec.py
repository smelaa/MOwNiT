import interpolation as inter
import numpy as np
import pandas as pd
import dataframe_image as dfi

def f(x):
    return np.sin(x) * np.sin(2 * x ** 2 / np.pi)

def generate_plots(f, n_nodes, nodes_reg, nodes_czyb, interval):
    for i in range(len(n_nodes)):
        inter.draw_interpolation(f, inter.lagrange_interpolation(nodes_reg[i]), interval, nodes_reg[i],
                                 "lagrange; " + str(n_nodes[i]) + " węzłów równomiernych",
                                 "./plots/lt_reg" + str(n_nodes[i]) + ".png")
        inter.draw_interpolation(f, inter.newton_interpolation(nodes_reg[i]), interval, nodes_reg[i],
                                 "newton; " + str(n_nodes[i]) + " węzłów równomiernych",
                                 "./plots/nt_reg" + str(n_nodes[i]) + ".png")
        inter.draw_interpolation(f, inter.lagrange_interpolation(nodes_czyb[i]), interval, nodes_czyb[i],
                                 "lagrange; " + str(n_nodes[i]) + " węzłów zg. z 0 Czybyszewa",
                                 "./plots/lt_czyb" + str(n_nodes[i]) + ".png")
        inter.draw_interpolation(f, inter.newton_interpolation(nodes_czyb[i]), interval, nodes_czyb[i],
                                 "newton; " + str(n_nodes[i]) + " węzłów zg. z 0 Czybyszewa",
                                 "./plots/nt_czyb" + str(n_nodes[i]) + ".png")

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
n_nodes = [3,4,5,7,8,9,10,11,12,13,14,15,20]
nodes_reg = []
nodes_czyb = []
for i in n_nodes:
    nodes_reg.append(inter.generate_points(i, interval, inter.generate_regularly, f))
    nodes_czyb.append(inter.generate_points(i, interval, inter.generate_czybyszow, f))

generate_plots(f, n_nodes, nodes_reg, nodes_czyb, interval)
generate_error_table(f,inter.lagrange_interpolation,inter.max_error,n_nodes, nodes_reg, nodes_czyb, interval, "Lagrange; bład maksymalny", "./tables/lt_max.png")
generate_error_table(f,inter.lagrange_interpolation,inter.mean_squared_error,n_nodes, nodes_reg, nodes_czyb, interval, "Lagrange; bład średniokwadratowy", "./tables/lt_mes.png")
generate_error_table(f,inter.newton_interpolation,inter.max_error,n_nodes, nodes_reg, nodes_czyb, interval, "Newton; bład maksymalny", "./tables/nt_max.png")
generate_error_table(f,inter.newton_interpolation,inter.mean_squared_error,n_nodes, nodes_reg, nodes_czyb, interval, "Newton; bład średniokwadratowy", "./tables/nt_mes.png")


