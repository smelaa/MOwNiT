import interpolation as inter
import spline
import numpy as np
import pandas as pd
import dataframe_image as dfi

#3-ci stopień: wersja I - free boundries; wersja II - cube
#2-gi stopień: wersja I - natural; wersja II - clamped

def f(x):
    return np.sin(x) * np.sin(2 * x ** 2 / np.pi)

def der(x):
    return 4*x*np.sin(x)*np.cos(2*x**2/np.pi)/np.pi + np.sin(2*x**2/np.pi)*np.cos(x)

def generate_plots(f, n_nodes, nodes_reg, interval):
    for i in range(len(n_nodes)):
        inter.draw_interpolation(f, spline.cubic_spline(nodes_reg[i], 'free boundry'), interval, nodes_reg[i],
                                 "funkcja sklejana 3-ego stopnia; " + str(n_nodes[i]) + " węzłów; warunek I",
                                 "./plots/cubspl_fb" + str(n_nodes[i]) + ".png")
        inter.draw_interpolation(f, spline.cubic_spline(nodes_reg[i], 'cube'), interval, nodes_reg[i],
                                 "funkcja sklejana 3-ego stopnia; " + str(n_nodes[i]) + " węzłów; warunek II",
                                 "./plots/cubspl_c" + str(n_nodes[i]) + ".png")
        inter.draw_interpolation(f, spline.quadratic_spline(nodes_reg[i], 'natural'), interval, nodes_reg[i],
                                 "funkcja sklejana 2-ego stopnia; " + str(n_nodes[i]) + " węzłów; warunek I",
                                 "./plots/quadspl_n" + str(n_nodes[i]) + ".png")
        inter.draw_interpolation(f, spline.quadratic_spline(nodes_reg[i], 'clamped'), interval, nodes_reg[i],
                                 "funkcja sklejana 2-ego stopnia; " + str(n_nodes[i]) + " węzłów; warunek II",
                                 "./plots/quadspl_c" + str(n_nodes[i]) + ".png")

def generate_error_table(f, cubic_fb, cubic_c, quadratic_n, quadratic_c, error_f, n_nodes, nodes_reg, interval, table_name, file_name):
    cubic_fb_errors=[]
    cubic_c_errors = []
    quadratic_n_errors = []
    quadratic_c_errors = []

    for i in range(len(n_nodes)):
        cubic_fb_errors.append(error_f(f, cubic_fb(nodes_reg[i]), interval))
        cubic_c_errors.append(error_f(f, cubic_fb(nodes_reg[i]), interval))
        quadratic_n_errors.append(error_f(f, quadratic_n(nodes_reg[i]), interval))
        quadratic_c_errors.append(error_f(f, quadratic_c(nodes_reg[i]), interval))


    data = {'l. węzłów': n_nodes,
            'funkcja sklejana 3-ego stopnia: warunek I': cubic_fb_errors,
            'funkcja sklejana 3-ego stopnia: warunek II': cubic_c_errors,
            'funkcja sklejana 2-ego stopnia: warunek I': quadratic_n_errors,
            'funkcja sklejana 2-ego stopnia: warunek II': quadratic_c_errors}
    data_frame=pd.DataFrame(data)
    data_frame=np.round(data_frame, decimals=4)
    data_frame = data_frame.style.set_caption(table_name).format({
        'funkcja sklejana 3-ego stopnia: warunek I': '{:,.4f}'.format,
        'funkcja sklejana 3-ego stopnia: warunek II': '{:,.4f}'.format,
        'funkcja sklejana 2-ego stopnia: warunek I': '{:,.4f}'.format,
        'funkcja sklejana 2-ego stopnia: warunek II': '{:,.4f}'.format
    })
    dfi.export(data_frame, file_name)

interval = [-np.pi, 2 * np.pi]
n_nodes = [4,5,6,7,9,10,12,13,15,17,18,20,22,25,30,40,50]
nodes_reg = []


for i in n_nodes:
    nodes_reg.append(inter.generate_points(i, interval, inter.generate_regularly, f))


generate_plots(f, n_nodes, nodes_reg, interval)
generate_error_table(f, spline.cubic_spline_fb, spline.cubic_spline_c, spline.quadratic_spline_n, spline.quadratic_spline_c, inter.max_error,n_nodes, nodes_reg, interval, "bład maksymalny", "./tables/max_err.png")
generate_error_table(f, spline.cubic_spline_fb, spline.cubic_spline_c, spline.quadratic_spline_n, spline.quadratic_spline_c, inter.mean_squared_error,n_nodes, nodes_reg, interval, "bład średniokwadratowy", "./tables/mse_err.png")
