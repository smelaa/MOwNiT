import numpy as np
import matplotlib.pyplot as plt

def lagrange_interpolation(points):
    n=len(points)
    
    x=[point[0] for point in points]
    y=[point[1] for point in points]

    def lagrange_polynomial(x_p,i):
        num, den=1,1
        for j in range (n):
            if j!=i:
                num*=(x_p-x[j])
                den*=(x[i]-x[j])
        return num/den
    
    def polynomial(x_p):
        result=0
        for i in range(n):
            result+=y[i]*lagrange_polynomial(x_p,i)
        return result
    
    return polynomial


def newton_interpolation(points):
    n=len(points)

    x=[point[0] for point in points]
    y=[point[1] for point in points]

    divided_differences = [[y[i] for i in range(n)]]
    for j in range(1, n):
        differences = []
        for i in range(n - j):
            difference = (divided_differences[j - 1][i + 1] - divided_differences[j - 1][i]) / (x[i + j] - x[i])
            differences.append(difference)
        divided_differences.append(differences)

    def polynomial(x_p):
        result=y[0]
        for j in range(1, n):
            term = divided_differences[j][0]
            for i in range(j):
                term *= (x_p - x[i])
            result += term
        return result

    return polynomial


def generate_regularly(n, interval):
    x=np.linspace(interval[0],interval[1],n, endpoint=True)
    return x

def generate_czybyszow(n, interval):
    a,b=interval[0],interval[1]
    x=[(a+b)/2+(b-a)/2*np.cos((2*i-1)/(2*n)*np.pi) for i in range(1,n+1)]
    return x

def generate_points(n, interval, x_generator, f_x):
    x=x_generator(n,interval)
    points=[(x[i],f_x(x[i])) for i in range (n)]
    return points

def draw_points(points, plot_name, file_name, clean=True):
    x = [point[0] for point in points]
    y = [point[1] for point in points]
    if clean: plt.clf()
    plt.plot(x,y)

    plt.title(plot_name)
    plt.xlabel('x')
    plt.ylabel('y')

    plt.savefig(file_name)

def draw_fun(fun, interval, n, plot_name, file_name, clean=True):
    points=generate_points(n, interval, generate_regularly, fun)
    draw_points(points,plot_name,file_name, clean)

def draw_interpolation(inter_fun, polynomial, interval, nodes, plot_name, file_name):
    plt.clf()
    plt.title(plot_name)
    plt.xlabel('x')
    plt.ylabel('y')
    points = generate_points(500, interval, generate_regularly, inter_fun)
    x = [point[0] for point in points]
    y = [point[1] for point in points]
    plt.plot(x, y, label="f(x)", color="mediumblue")
    points = generate_points(500, interval, generate_regularly, polynomial)
    x = [point[0] for point in points]
    y = [point[1] for point in points]
    plt.plot(x, y, label="f_inter(x)", color="firebrick")
    x = [point[0] for point in nodes]
    y = [point[1] for point in nodes]
    plt.scatter(x,y, color='tomato')
    plt.savefig(file_name)


def max_error(f1, f2, interval):
    res=0
    x=generate_regularly(500, interval)
    for xi in x:
        res=max(res, abs(f1(xi)-f2(xi)))
    return res

def mean_squared_error(f1, f2, interval):
    res=0
    x = generate_regularly(500, interval)
    for xi in x:
        res += (f1(xi)-f2(xi))**2
    res=res**(1/2)
    res/=500
    return res