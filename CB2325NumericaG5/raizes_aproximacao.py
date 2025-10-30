"""coloquei um numero para maximo de iterações"""

import sympy as sp
from typing import Callable


def bissecao(f: Callable[[float], float], a: float, b: float, tol: float = 1e-6, max_iter: int = 100) -> float:
    """
    Método da bisseção para encontrar uma raiz de uma função contínua em um intervalo [a, b].

    O método da bisseção assume que f(a) e f(b) têm sinais opostos e procede dividindo o
    intervalo ao meio repetidamente até que a função no ponto médio seja menor que a tolerância
    desejada ou até atingir o número máximo de iterações.

    Args:
        f (Callable[[float], float]): Função contínua que recebe um número real e retorna um número real.
        a (float): Ponto inicial do intervalo à esquerda.
        b (float): Ponto inicial do intervalo à direita.
        tol (float, optional): Tolerância para a convergência (critério em |f(c)|). Por padrão 1e-6.
        max_iter (int, optional): Número máximo de iterações a serem executadas. Por padrão 100.

    Raises:
        ValueError: Se f(a) e f(b) não tiverem sinais opostos.

    Returns:
        float: Uma aproximação da raiz encontrada no intervalo [a, b].
    """
    if f(a) * f(b) > 0:
        raise ValueError("f(a) e f(b) devem ter sinais opostos para o método da bisseção.")
    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol:
            break
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return c


def newton(f: Callable[..., object], x0: float, tol: float = 1e-6, max_iter: int = 100) -> float:
    """
    Método de Newton (Newton-Raphson) para encontrar uma raiz de uma função utilizando
    derivadas simbólicas via SymPy.

    A função `f` deve ser tal que `f(x)` produza uma expressão manipulável pelo SymPy
    quando `x` for um `sympy.Symbol`, ou simplesmente uma função que possa ser avaliada
    numericamente quando lambdificada.

    Args:
        f (Callable[..., object]): Função que define a expressão de interesse. Deve aceitar um símbolo
            SymPy ou ser compatível com `sympify`/`lambdify`.
        x0 (float): Chute inicial para o método de Newton.
        tol (float, optional): Tolerância para o critério de parada em |f(x_k)|. Por padrão 1e-6.
        max_iter (int, optional): Número máximo de iterações a serem executadas. Por padrão 100.

    Raises:
        ZeroDivisionError: Se a derivada num ponto for zero (divisão por zero no método).

    Returns:
        float: Aproximação da raiz obtida pelo método de Newton.
    """
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
        if dfx == 0:
            raise ZeroDivisionError("Derivada nula, método de Newton falhou.")
        xk = xk - fx / dfx
    return xk


def secante(f: Callable[[float], float], a: float, b: float, tol: float = 1e-6, max_iter: int = 100) -> float:
    """
    Método da secante para encontrar uma raiz de uma função.

    O método da secante é um método iterativo que aproxima a derivada por uma diferença
    finita usando dois pontos consecutivos. Requer dois chutes iniciais a e b.

    Args:
        f (Callable[[float], float]): Função que recebe e retorna números reais.
        a (float): Primeiro chute inicial.
        b (float): Segundo chute inicial.
        tol (float, optional): Tolerância para o critério de parada em |f(c)|. Por padrão 1e-6.
        max_iter (int, optional): Número máximo de iterações a serem executadas. Por padrão 100.

    Raises:
        ZeroDivisionError: Se ocorrer divisão por zero ao calcular o próximo iterando.

    Returns:
        float: Aproximação da raiz obtida pelo método da secante.
    """
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


def raiz(f: Callable[..., object], a: float = None, b: float = None, x0: float = None, tol: float = 1e-6, method: str = "bissecao") -> float:
    """
    Função auxiliar para selecionar o método de busca de raiz desejado.

    Esta função encaminha para um dos métodos implementados: bisseção, secante ou newton,
    dependendo do parâmetro `method`.

    Args:
        f (Callable[..., object]): Função alvo cuja raiz se deseja encontrar.
        a (float, optional): Limite esquerdo ou primeiro chute inicial (quando aplicável).
        b (float, optional): Limite direito ou segundo chute inicial (quando aplicável).
        x0 (float, optional): Chute inicial para o método de Newton (quando aplicável).
        tol (float, optional): Tolerância para os métodos. Por padrão 1e-6.
        method (str, optional): Método a ser utilizado: "bissecao", "secante" ou "newton". Por padrão "bissecao".

    Raises:
        ValueError: Se o método especificado for inválido.

    Returns:
        float: Aproximação da raiz obtida pelo método selecionado.
    """
    if method not in ("bissecao", "secante", "newton"):
        raise ValueError("Método inválido.")
    if method == "bissecao":
        return bissecao(f, a, b, tol)
    elif method == "secante":
        return secante(f, a, b, tol)
    elif method == "newton":
        return newton(f, x0, tol)


f = lambda x: x**3 - 9*x + 5

print("Bisseção:", raiz(f, a=0, b=2, method="bissecao"))
print("Secante:", raiz(f, a=0, b=2, method="secante"))
print("Newton:", raiz(lambda x: x**3 - 9*x + 5, x0=1, method="newton"))