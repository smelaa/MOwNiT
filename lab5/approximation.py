import numpy as np
import matplotlib.pyplot as plt

#points - tablica krotek (x, f(x), w(x))
def approx(points, m):
    if m>len(points): return None
    x = [point[0] for point in points]
    y = [point[1] for point in points]
    w = [point[2] for point in points]

    wx=[0 for _ in range (2*m)]
    wyx=[0 for _ in range (m)]
    for i in range (len(points)):
        for j in range (m):
            wyx[j]+=w[i] * y[i] * x[i] ** j
            wx[j] += w[i] * x[i] ** j
        for j in range (m, len(wx)):
            wx[j]+=w[i]*x[i]**j

    B=np.array(wyx)
    B=np.reshape(B, (-1,1))
    G=np.array([[wx[i+j] for i in range (m)] for j in range (m)])
    A = np.linalg.solve(G, B)
    A=np.reshape(A,-1)

    def F(x_p):
        y_p=0
        x_pow=1
        for i in range (m):
            y_p+=A[i]*x_pow
            x_pow*=x_p
        return y_p

    return F

def generate_points(n, interval, f_x):
    x=np.linspace(interval[0],interval[1],n, endpoint=True)
    points=[(x[i],f_x(x[i]), 1) for i in range (n)]
    return points

def draw_interpolation(inter_fun, polynomial, interval, nodes, plot_name, file_name):
    plt.clf()
    plt.title(plot_name)
    plt.xlabel('x')
    plt.ylabel('y')
    points = generate_points(1000, interval, inter_fun)
    x = [point[0] for point in points]
    y = [point[1] for point in points]
    plt.plot(x, y, label="f(x)", color="dodgerblue")
    points = generate_points(1000, interval, polynomial)
    x = [point[0] for point in points]
    y = [point[1] for point in points]
    plt.plot(x, y, label="f_inter(x)", color="deeppink")
    x = [point[0] for point in nodes]
    y = [point[1] for point in nodes]
    plt.scatter(x,y, color='darkviolet')
    plt.savefig(file_name)

def max_error(f1, f2, interval):
    res=0
    x=np.linspace(interval[0],interval[1],1000, endpoint=True)
    for xi in x:
        res=max(res, abs(f1(xi)-f2(xi)))
    return res

def mean_squared_error(f1, f2, interval):
    res=0
    x = np.linspace(interval[0],interval[1],1000, endpoint=True)
    for xi in x:
        res += (f1(xi)-f2(xi))**2
    res=res**(1/2)
    res/=500
    return res