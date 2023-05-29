from math import inf

def newton_solving_diff(f, f_der, x_start, epsilon=0, max_it=1000): # x(i+1)-x(i)<=epsilon
    x_prev=-inf
    x_curr=x_start
    it=0
    while abs(x_curr-x_prev)>epsilon and it<max_it:
        x_prev=x_curr
        it+=1
        x_curr=x_prev-(f(x_prev)/f_der(x_prev))
    return x_curr, it

def newton_solving_fval(f, f_der, x_start, epsilon=0, max_it=1000): # f(xi)<epsilon
    x_prev=-inf
    x_curr=x_start
    it=0
    while abs(f(x_curr))>epsilon and it<max_it:
        x_prev=x_curr
        it+=1
        x_curr=x_prev-(f(x_prev)/f_der(x_prev))
    return x_curr, it

def secant_solving_diff(f, x_1, x_2, epsilon=0, max_it=1000): # x(i+1)-x(i)<=epsilon
    if x_1==x_2: return 0,0
    x_prevprev=inf
    x_prev=x_1
    x_curr=x_2
    it=0
    while abs(x_curr-x_prev)>epsilon and it<max_it:
        x_prevprev, x_prev=x_prev, x_curr
        it+=1
        x_curr=x_prev-f(x_prev)*(x_prev-x_prevprev)/(f(x_prev)-f(x_prevprev))
    return x_curr, it

def secant_solving_fval(f, x_1, x_2, epsilon=0, max_it=1000): # f(xi)<epsilon
    if x_1==x_2: return 0,0
    x_prevprev=inf
    x_prev=x_1
    x_curr=x_2
    it=0
    while abs(f(x_curr))>epsilon and it<max_it:
        x_prevprev, x_prev=x_prev, x_curr
        it+=1
        x_curr=x_prev-f(x_prev)*(x_prev-x_prevprev)/(f(x_prev)-f(x_prevprev))
    return x_curr, it