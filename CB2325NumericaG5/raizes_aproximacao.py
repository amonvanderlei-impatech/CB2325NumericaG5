"""coloquei um numero para maximo de iterações"""

import sympy as sp

def bissecao(f,a,b,tol=1e-6,max_iter=100):
    if f(a) * f(b) > 0:
        raise ValueError("f(a) e f(b) devem ter sinais opostos para o método da bisseção.")
    for _ in range(max_iter):
        c = (a+b)/2
        if abs(f(c)) < tol:
            break
        if f(a) * f(c) < 0:
            b=c
        else:
            a=c
    return c

def newton(f,x0,tol=1e-6,max_iter=100):
    xk = x0
    x = sp.Symbol('x')
    expr = sp.sympify(f(x))
    dexpr = sp.diff(expr, x)

    f_num = sp.lambdify(x, expr, 'numpy')
    df_num = sp.lambdify(x, dexpr, 'numpy')

    for _ in range(max_iter):
        fx = f_num(xk)
        dfx = df_num(xk)
        if abs(fx) < tol:
            return xk
        if dfx ==0:
            raise ZeroDivisionError("Derivada nula, método de Newton falhou.")
        xk = xk-fx/dfx
    return xk

def secante(f,a,b,tol=1e-6,max_iter=100):
    fa, fb = f(a), f(b)
    for _ in range(max_iter):
        if abs(fb - fa) < 1e-15:
            raise ZeroDivisionError("Divisão por zero no método da secante.")
        c = b - fb * (b - a) / (fb - fa)
        if abs(f(c)) < tol:
            return c
        a, b = b, c
        fa, fb = fb, f(c)
    return c


def raiz(f, a=None, b=None, x0=None, tol=1e-6, method="bissecao"):
    if method == "bissecao":
        return bissecao(f, a, b, tol)
    elif method == "secante":
        return secante(f, a, b, tol)
    elif method == "newton":
        return newton(f, x0, tol)
    else:
        raise ValueError("Método inválido.")



f = lambda x: x**3 - 9*x + 5

print("Bisseção:", raiz(f, a=0, b=2, method="bissecao"))
print("Secante:", raiz(f, a=0, b=2, method="secante"))
print("Newton:", raiz(lambda x: x**3 - 9*x + 5, x0=1, method="newton"))
