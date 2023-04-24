import numpy as np
import matplotlib.pyplot as plt

#points - tablica krotek (x, f(x)))
def approx(points, m, interval):
    #if m>len(points): return None
    x = [point[0] for point in points]
    y = [point[1] for point in points]

    a=-2*np.pi/(interval[1]-interval[0])
    b=2*np.pi*interval[0]/(interval[1]-interval[0])
    #x_new=a*x_old+b
    #x_old=(x_new-b)/a

    def translate_x(x_p):
        return a*x_p+b

    A=[]
    B=[]
    for i in range(m):
        sum_a=0
        sum_b=0
        for j in range(len(points)):
            x_new=translate_x(x[j])
            sum_a+=y[j]*np.cos(i*x_new)
            sum_b+=y[j]*np.sin(i*x_new)
        A.append(2/(len(points)+1)*sum_a)
        B.append(2/(len(points)+1)*sum_b)

    def F(x_p):
        res=A[0]/2
        new_x=translate_x(x_p)
        for i in range(1,m):
            res+=A[i]*np.cos(i*new_x)
            res+=B[i]*np.sin(i*new_x)
        return res

    return F

def generate_points(n, interval, f_x):
    x=np.linspace(interval[0],interval[1],n, endpoint=True)
    points=[(x[i],f_x(x[i])) for i in range (n)]
    return points

def draw_approx(inter_fun, polynomial, interval, nodes, plot_name, file_name):
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