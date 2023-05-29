import random
from numpy.linalg import inv
import numpy as np

class TridiagonalMatrix():
    def __init__(self, A=None):
        self.lower = []
        self.upper = []
        self.diag = []
        if A is not None:
            self.lower = [0]
            self.upper = []
            self.diag = [A[0][0]]
            self.n = len(A)
            for i in range(1, len(A)):
                self.diag.append(A[i][i])
                self.lower.append(A[i][i - 1])
                self.upper.append(A[i-1][i])
            self.upper.append(0)


def gaussian_elimination(A, b):
    if not all([len(row) == len(A) for row in A]):
        return None  # if the A matrix is not square - solution does not exist
    if len(b) != len(A): return None  # if the b vector is smaller then matrix - solution does not exist
    n = len(A)

    for i in range(n):
        p = -1
        for j in range(i, n):
            if A[j][i] != 0:
                p = j
                break
        if p == -1: return None  # solution does not exist
        if p != i:
            A[p], A[i] = A[i], A[p]
            b[p], b[i] = b[i], b[p]
        for j in range(i + 1, n):
            m = A[j][i] / A[i][i]
            b[j] -= m * b[i]
            for k in range(i, n):
                A[j][k] -= m * A[i][k]

    if A[n - 1][n - 1] == 0: return None  # solution does not exist

    x = [None for _ in range(n)]
    x[n - 1] = b[n - 1] / A[n - 1][n - 1]
    for i in range(n - 2, -1, -1):
        sum = 0
        for j in range(i + 1, n): sum += A[i][j] * x[j]
        x[i] = (b[i] - sum) / A[i][i]
    return x


def thomas(A: TridiagonalMatrix, b):
    c = A.upper
    d = A.diag
    a = A.lower
    gamma = [c[0] / d[0]]
    rho = [b[0] / d[0]]
    for i in range(1, A.n - 1):
        gamma.append(c[i] / (d[i] - a[i] * gamma[i - 1]))
        rho.append((b[i] - a[i] * rho[i - 1]) / (d[i] - a[i] * gamma[i - 1]))
    i=A.n - 1
    rho.append((b[i] - a[i] * rho[i - 1]) / (d[i] - a[i] * gamma[i - 1]))

    x = [None for _ in range(A.n)]
    x[i] = rho[i]
    for i in range(A.n - 2, -1, -1):
        x[i] = rho[i] - gamma[i] * x[i + 1]

    return x

def get_x_probe(n, prec_f=lambda x: x):
    return [prec_f(random.choice((-1, 1))) for _ in range(n)]


def get_b_vector(A, x):
    n = len(A)
    b = []
    for i in range(n):
        b.append(sum([A[i][j] * x[j] for j in range(n)]))
    return b


def get_Ab_v1(n, prec_f, x=None):
    if x is None:
        x = get_x_probe(n, prec_f)
    elif len(x) != n:
        return None
    A = [[prec_f(1) for _ in range(n)]]
    for i in range(1, n):
        A.append([prec_f(1 / (i + j + 1)) for j in range(n)])
    b = get_b_vector(A, x)
    return A, b


def get_Ab_v2(n, prec_f, x=None):
    if x is None:
        x = get_x_probe(n)
    elif len(x) != n:
        return None
    A = []
    for i in range(n):
        row = [A[j][i] for j in range(i)]
        row.extend([prec_f(2 * (i + 1) / (j + 1)) for j in range(i, n)])
        A.append(row.copy())
    b = get_b_vector(A, x)
    return A, b


def get_Ab_v3(n, x=None):
    if x is None:
        x = get_x_probe(n)
    elif len(x) != n:
        return None
    A = []
    for i in range(n):
        row = []
        for j in range(n):
            if j < i - 1 or j > i + 1:
                row.append(0)
            elif i == j:
                row.append(4)
            elif j == i + 1:
                row.append(1 / (i + 5))
            else:
                row.append(4 / (i + 6))
        A.append(row.copy())
    b = get_b_vector(A, x)
    return A, b


def max_norm(x1_vec, x2_vec):
    if len(x1_vec) != len(x2_vec): return -1
    res = 0
    for i in range(len(x1_vec)):
        curr_norm = abs(x1_vec[i] - x2_vec[i])
        res = max(curr_norm, res)
    return res


def sq_norm(x1_vec, x2_vec):
    if len(x1_vec) != len(x2_vec): return -1
    res = 0
    for i in range(len(x1_vec)):
        curr_norm = (x1_vec[i] - x2_vec[i]) ** 2
        res += curr_norm
    return (res ** (0.5))


def cond_number(A):
    norm_A = 0
    norm_Ainv = 0
    Ainv = inv(A)
    for i in range(len(A)):
        max_A = 0
        max_Ainv = 0
        for j in range(len(A)):
            max_A = max(max_A, A[i][j])
            max_Ainv = max(max_Ainv, Ainv[i][j])
        norm_A += max_A
        norm_Ainv += max_Ainv
    return norm_A * norm_Ainv
