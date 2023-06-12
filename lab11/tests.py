import equations_set as eq
import pandas as pd

maxit=1000

n = [3,4,5,7,10,12,15,20,30,40,50,75,100,125,150,175,200,250,300,500]

eps=[1e-15, 1e-12, 1e-10, 1e-8, 1e-5, 0.01, 0.1]

x = [eq.get_x_probe(i) for i in n]
A = [eq.get_A_matrix(i) for i in n]
b = [eq.get_b_vector(a_i, b_i) for a_i, b_i in zip(A,x)]

#PROMIEN SPEKTRALNY
spec_rad=dict()
for i, A_i in enumerate(A):
    spec_rad["n={size}".format(size=n[i])]=eq.spectral_radius(A_i)
spec_rad={"promien spektralny": spec_rad}
data_frame_srad = pd.DataFrame(spec_rad)
data_frame_srad.to_excel(excel_writer="./spec_rad.xlsx", sheet_name="srad")

#LICZENIE UKLADOW
x0_close=[[0 for j in range (i)] for i in n]
x0_far=[[i*(-10) for i in x_i] for x_i in x]
x0_further=[[i*(-100) for i in x_i] for x_i in x]

times=dict()
prec=dict()
iter_n=dict()

for i, n_i in enumerate(n):
    for epsilon in eps:
        p, t, it=eq.jacobi_comparision(A[i], b[i], x0_close[i], x[i], maxit, epsilon)
        prec["n={size}, eps={precision}, x0 - 0".format(size=n_i, precision=epsilon)] = p
        times["n={size}, eps={precision}, x0 - 0".format(size=n_i, precision=epsilon)]=t
        iter_n["n={size}, eps={precision}, x0 - 0".format(size=n_i, precision=epsilon)]=it

        p, t, it = eq.jacobi_comparision(A[i], b[i], x0_far[i], x[i], maxit, epsilon)
        prec["n={size}, eps={precision}, x0 - x*(-10)".format(size=n_i, precision=epsilon)] = p
        times["n={size}, eps={precision}, x0 - x*(-10)".format(size=n_i, precision=epsilon)] = t
        iter_n["n={size}, eps={precision}, x0 - x*(-10)".format(size=n_i, precision=epsilon)] = it

        p, t, it = eq.jacobi_comparision(A[i], b[i], x0_further[i], x[i], maxit, epsilon)
        prec["n={size}, eps={precision}, x0 - x*(-100)".format(size=n_i, precision=epsilon)] = p
        times["n={size}, eps={precision}, x0 - x*(-100)".format(size=n_i, precision=epsilon)] = t
        iter_n["n={size}, eps={precision}, x0 - x*(-100)".format(size=n_i, precision=epsilon)] = it

data_frame_prec = pd.DataFrame(prec)
data_frame_times = pd.DataFrame(times)
data_frame_iter = pd.DataFrame(iter_n)

data_frame_prec.T.to_excel(excel_writer="./prec.xlsx", sheet_name="prec")
data_frame_times.T.to_excel(excel_writer="./times.xlsx", sheet_name="times")
data_frame_iter.T.to_excel(excel_writer="./iter.xlsx", sheet_name="iter")

