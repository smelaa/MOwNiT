import interpolation as inter
import numpy as np


def f0(x):
    return x + 6


def f1(x):
    return np.cos(x)

def f2(x):
    return np.sin(x)


def f3(x):
    return x * x


def f4(x):
    return (x - 1) * (x + 1) * (x - 2)


n_points = [4, 20, 100]
functions = [f0, f1, f2, f3,f4]
f_names = ["x+6", "cos(x)", "sin(x)", "x^2", "(x-2)(x-1)(x+1)"]
points = []
names = []
for i in range(len(n_points)):
    for j in range(len(functions)):
        points.append(inter.generate_points(n_points[i], (-4, 4), inter.generate_regularly, functions[j]))
        names.append(str(n_points[i]) + " węzłów; " + str(f_names[j]) + "; równomiernie")
        points.append(inter.generate_points(n_points[i], (-4, 4), inter.generate_czybyszow, functions[j]))
        names.append(str(n_points[i]) + " węzłów; " + str(
            f_names[j]) + "; zg. z zerami Czybyszewa")

lagrange_polynomial = []
newton_polynomial = []

for i in range(len(points)):
    inter.draw_fun(inter.lagrange_interpolation(points[i]), (-4, 4), 1000, "lagrange; " + names[i],
                   "./plots/lt" + str(i) + ".png")
    inter.draw_fun(inter.newton_interpolation(points[i]), (-4, 4), 1000, "newton; " + names[i],
                   "./plots/nt" + str(i) + ".png")
