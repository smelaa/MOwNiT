import numpy as np

def hermite_interpolation(points):
    n = len(points)*2
    x = np.array([p[0] for p in points])
    x=np.repeat(x, 2)
    y = np.array([p[1] for p in points])
    y=np.repeat(y, 2)
    derivs = np.array([p[2] for p in points])

    divdiffs = np.zeros((n, n))
    divdiffs[:,0]=y
    for i in range (n//2):
        divdiffs[i*2][1] =derivs[i]

    for i in range (n//2-1):
        divdiffs[i*2+1][1] =(divdiffs[i*2+1][0]-divdiffs[i*2+2][0])/(x[i*2]-x[i*2+2])

    for j in range(2, n):
        for i in range(n - j):
            divdiffs[i][j] = (divdiffs[i + 1][j - 1] - divdiffs[i][j - 1]) / (x[i + j] - x[i])

    terms=divdiffs[0]

    def polynomial(x_p):
        result=terms[0]
        for j in range(1, len(terms)):
            term = terms[j]
            for i in range(j):
                term *= (x_p - x[i])
            result += term
        return result

    return polynomial


def generate_points_1stderiv(n, interval, x_generator, f_x, der_x):
    x=x_generator(n,interval)
    points=[(x[i],f_x(x[i]), der_x(x[i])) for i in range (n)]
    return points



