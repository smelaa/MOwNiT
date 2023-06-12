import numpy as np
from time import time
import random


def max_norm(x1_vec, x2_vec):
    res = np.max(np.abs(np.array(x1_vec) - np.array(x2_vec)))
    return res

def jacobi_eq(A, b, xt):
    res=[]
    for i in range (len(xt)):
        sum=0
        for j in range (len(xt)):
            if i!=j:
                sum+=A[i][j]*xt[j]
        res.append(1/A[i][i]*(b[i]-sum))
    return res

def mul_A_xt(A, xt):
    res=[]
    for i in range (len(A)):
        sum=0
        for j in range(len(xt)):
            sum+=xt[j]*A[i][j]
        res.append(sum)
    return res

def jacobi_incremental(A, b, x0, maxit, eps):
    x_prev = x0
    x_curr = jacobi_eq(A,b,x_prev)
    cnt = 0
    while cnt < maxit and max_norm(x_prev, x_curr) >= eps:
        x_prev = x_curr
        x_curr = jacobi_eq(A,b,x_prev)
        cnt += 1
    return x_curr, cnt


def jacobi_resdiual(A, b, x0, maxit, eps):
    x_curr = x0
    cnt = 0
    while cnt < maxit and max_norm(mul_A_xt(A,x_curr), b) >= eps:
        x_curr = jacobi_eq(A,b,x_curr)
        cnt += 1
    return x_curr, cnt


def jacobi_comparision(A, b, x0, x, maxit, eps):
    start = time()
    res_x, res_it = jacobi_resdiual(A, b, x0, maxit, eps)
    end = time()
    res_time = end - start
    res_prec = max_norm(x, res_x)

    start = time()
    inc_x, inc_it = jacobi_incremental(A, b, x0, maxit, eps)
    end = time()
    inc_time = end - start
    inc_prec = max_norm(x, inc_x)

    times = {
        "kryterium rezydualne": res_time,
        "kryterium przyrostowe": inc_time
    }

    iterations = {
        "kryterium rezydualne": res_it,
        "kryterium przyrostowe": inc_it
    }

    precission = {
        "kryterium rezydualne": res_prec,
        "kryterium przyrostowe": inc_prec
    }

    return precission, times, iterations

def spectral_radius(A):
    LU = np.tril(A) + np.triu(A)
    np.fill_diagonal(LU, 0)
    D = np.linalg.inv(np.eye(len(A))*np.diag(A))
    M=-D@LU
    return np.max(np.abs(np.linalg.eigvals(M)))

def get_x_probe(n):
    return [random.choice((-1, 1)) for _ in range(n)]

def get_A_matrix(n):
    A=[[None for _ in range (n)] for i in range (n)]
    for i in range (n):
        A[i][i]=10
        for j in range (n):
            if j!=i:
                A[i][j]=1/(abs(i-j)+4)
    return A

def get_b_vector(A, x):
    n = len(A)
    b = []
    for i in range(n):
        b.append(sum([A[i][j] * x[j] for j in range(n)]))
    return b