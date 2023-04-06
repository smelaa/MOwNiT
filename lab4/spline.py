import numpy as np

def f(p1, p2):
    return (p2[1]-p1[0])/(p2[0]-p1[0])

def dev_diff_2(p1,p2,p3):
    return (f(p2,p3)-f(p1,p2))/(p2[0]-p1[0])

def dev_diff_3(p1,p2,p3,p4):
    return (dev_diff_2(p2,p3,p4)-dev_diff_2(p1,p2,p3))/(p3[0]-p1[0])

#version: cube lub free boundry
def cubic_spline(points, version='free boundry'):
    if version!='free boundry' and version!='cube': return None
    x = [point[0] for point in points]
    y = [point[1] for point in points]
    h = [x[i + 1] - x[i] for i in range(len(x) - 1)]
    delta = [(y[i + 1] - y[i])/h[i] for i in range(len(x) - 1)]
    Y_vec=np.array([delta[i+1]-delta[i] for i in range (len(delta)-1)])
    A_matrix=np.array([([0 for i in range (j)]+[h[j], 2*(h[j]+h[j+1]), h[j+1]]+[0 for i in range (len(h)-2-j)]) for j in range (len(h)-1)])
    if version=='cube':
        y1=h[0]**2*dev_diff_3((x[0],y[0]),(x[1],y[1]),(x[2],y[2]),(x[3],y[3]))
        yn=-h[len(h)-1]**2*dev_diff_3((x[len(x)-4],y[len(y)-4]),(x[len(x)-3],y[len(y)-3]),(x[len(x)-2],y[len(y)-2]),(x[len(x)-1],y[len(y)-1]))
        Y_vec=np.concatenate(([y1], Y_vec,[yn]))
        A_matrix=np.concatenate(([[1]+[0 for _ in range (len(h))]], A_matrix, [[0 for _ in range (len(h))]+[1]]), axis=0)
    elif version=='free boundry':
        A_matrix = np.concatenate(([[-h[0], h[0]] + [0 for _ in range(len(h) - 1)]], A_matrix,
                                   [[0 for _ in range(len(h) - 1)] + [-h[len(h) - 1], h[len(h) - 1]]]), axis=0)
        Y_vec = np.concatenate(([0], Y_vec, [0]))
    sigma = np.linalg.solve(A_matrix, Y_vec)
    b = [(y[i + 1] - y[i]) / h[i] - h[i] * (sigma[i + 1] + 2 * sigma[i]) for i in range (len(x)-1)]
    c = [3 * sigma[i] for i in range (len(x)-1)]
    d = [(sigma[i + 1] - sigma[i]) / h[i] for i in range (len(x)-1)]

    def polynomial(x_p):
        if x_p<x[0] or x_p>x[len(x)-1]:
            return None
        i=0
        for j in range (len(x)-1):
            if x_p>=x[j] and x_p<=x[j+1]:
                i=j
                break

        return y[i]+b[i]*(x_p-x[i])+c[i]*(x_p-x[i])**2+d[i]*(x_p-x[i])**3

    return polynomial

def cubic_spline_fb(points):
    return cubic_spline(points, version='free boundry')

def cubic_spline_c(points):
    return cubic_spline(points, version='cube')

#version: natural lub clamped
def quadratic_spline(points, version='natural'):
    if version!='natural' and version!='clamped': return None
    x = [point[0] for point in points]
    y = [point[1] for point in points]
    a=y
    gamma=[(y[i]-y[i-1])/(x[i]-x[i-1]) for i in range (1, len(y))]
    if version=='natural':
        Y_vec=np.array([0]+[2*gamma[i] for i in range (len(gamma))])
        A_matrix=np.array([([0 for i in range (j)]+[1,1]+[0 for i in range(len(gamma)-1-j)]) for j in range(len(gamma))])
        A_matrix = np.concatenate(([[1]+[0 for i in range (len(gamma))]], A_matrix), axis=0)
    if version=='clamped':
        Y_vec = np.array([gamma[0]] + [2 * gamma[i] for i in range(len(gamma))])
        A_matrix = np.array(
            [([0 for i in range(j)] + [1, 1] + [0 for i in range(len(gamma) - 1 - j)]) for j in range(len(gamma))])
        A_matrix = np.concatenate(([[1] + [0 for i in range(len(gamma))]], A_matrix), axis=0)
    b = np.linalg.solve(A_matrix, Y_vec)
    c=[]
    for i in range (len(b)-1):
        c.append((b[i+1]-b[i])/(2*(x[i+1]-x[i])))
    def polynomial(x_p):
        if x_p<x[0] or x_p>x[len(x)-1]:
            return None
        i=0
        for j in range (len(x)-1):
            if x_p>=x[j] and x_p<=x[j+1]:
                i=j
                break

        return a[i]+b[i]*(x_p-x[i])+c[i]*(x_p-x[i])**2

    return polynomial

def quadratic_spline_n(points):
    return quadratic_spline(points, version='natural')

def quadratic_spline_c(points):
    return quadratic_spline(points, version='clamped')