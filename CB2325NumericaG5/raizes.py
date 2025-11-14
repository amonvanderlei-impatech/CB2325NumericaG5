import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from typing import Callable
import math


def bissecao(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-6,
    max_iter: int = 100,
    plot: bool = True
  ) -> float:
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
        plot (bool, optional): Se True, exibe o gráfico das iterações. Padrão: True.

    Raises:
        ValueError: Se `a` ou `b` forem inválidos (NaN, infinito ou não finitos).
        ValueError: Se `f(a)` ou `f(b)` forem inválidos.
        ValueError: Se não houver mudança de sinal no intervalo.
        ValueError: Se algum valor no meio das iterações resultar em NaN/infinito.
        RuntimeError: Se o método não convergir após `max_iter` iterações.

    Returns:
        float: Uma aproximação da raiz encontrada no intervalo [a, b].
    """
    if math.isnan(a) or math.isnan(b) or math.isinf(a) or math.isinf(b):
        raise ValueError
    if not all(map(math.isfinite, [a, b])):
        raise ValueError    
    
    fa, fb = f(a), f(b)
    if any(math.isnan(val) or math.isinf(val) for val in [fa, fb]):
        raise ValueError
    if math.isnan(fa) or math.isnan(fb) or math.isinf(fa) or math.isinf(fb):
        raise ValueError
    if f(a) * f(b) > 0:
        raise ValueError("f(a) e f(b) devem ter sinais opostos para o método da bisseção.")

    x = np.linspace(a - abs(b - a) * 0.3, b + abs(b - a) * 0.3, 500)
    y = np.array([f(xi) for xi in x])

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, linewidth=2, label='f(x)')
    plt.axhline(0, color='black', linestyle='--', linewidth=1)
    plt.title('Método da Bisseção')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True, linestyle=':', linewidth=0.6)
    plt.legend()

    for i in range(max_iter):
        c = (a + b) / 2

        plt.axvline(a, color='red', linestyle=':', alpha=0.5)
        plt.axvline(b, color='green', linestyle=':', alpha=0.5)
        plt.axvline(c, color='orange', linestyle='--', alpha=0.8)

        # pontos
        plt.scatter([a, b, c], [f(a), f(b), f(c)],
                    color=['red', 'green', 'orange'], s=50)

        # anotação do ponto médio
        plt.text(c, f(c), f"c{i+1}", fontsize=8, color='orange', ha='left', va='bottom')

        if abs(f(c)) < tol:
            break

        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
        fc = f(c)
        if math.isnan(fc) or math.isinf(fc):
            raise ValueError
    else:
        raise RuntimeError
    
    plt.tight_layout()
    if plot:
        plt.show()
    else:
        plt.close()
    if math.isnan(f(c)) or math.isinf(f(c)):
        raise ValueError
    return c

def newton(
    f: Callable[[sp.Symbol | float], sp.Expr | float],
    x0: float,
    tol: float = 1e-6,
    max_iter: int = 100,
    plot: bool = True
) -> float:
    """
    Método de Newton (Newton-Raphson) para encontrar uma raiz de uma função utilizando
    derivadas simbólicas via SymPy.

    A função `f` deve ser tal que `f(x)` produza uma expressão manipulável pelo SymPy
    quando `x` for um `sympy.Symbol`, ou simplesmente uma função que possa ser avaliada
    numericamente quando lambdificada.

    Usa o SymPy para calcular a derivada automaticamente e itera até que |f(x_k)| < tol
    ou até atingir o número máximo de iterações.

    Args:
        f (Callable[[sp.Symbol | float], sp.Expr | float]): Função que define a expressão de interesse. Deve aceitar um símbolo
            SymPy ou ser compatível com `sympify`/`lambdify`.
        x0 (float): Chute inicial para o método de Newton.
        tol (float, optional): Tolerância para o critério de parada em |f(x_k)|. Por padrão 1e-6.
        max_iter (int, optional): Número máximo de iterações a serem executadas. Por padrão 100.
        plot (bool, optional): Se True, exibe o gráfico das tangentes sucessivas. Padrão: True.

    Raises:
        ZeroDivisionError: Se a derivada num ponto for zero (divisão por zero no método).
        ValueError: Se, após as iterações, |f(x_k)| ainda for maior que a tolerância.

    Returns:
        float: Aproximação da raiz obtida pelo método de Newton.
    """

    x = sp.Symbol('x')
    expr = sp.sympify(f(x))
    dexpr = sp.diff(expr, x)
    f_num = sp.lambdify(x, expr, 'numpy')
    df_num = sp.lambdify(x, dexpr, 'numpy')

    xk = x0
    history = [x0]

    for _ in range(max_iter):
        fx = f_num(xk)
        dfx = df_num(xk)

        if abs(fx) < tol:
            break
        if dfx == 0:
            raise ZeroDivisionError("Derivada nula, método de Newton falhou.")

        xk = xk - fx / dfx
        history.append(xk)

    if plot:
        x_vals = np.linspace(min(history) - 2, max(history) + 2, 800)
        y_vals = f_num(x_vals)

        plt.figure(figsize=(9, 6))
        plt.plot(x_vals, y_vals, 'b', linewidth=1.8, label='f(x)')
        plt.axhline(0, color='black', linestyle='--', linewidth=1)

        for i in range(len(history) - 1):
            x0 = history[i]
            f0 = f_num(x0)
            df0 = df_num(x0)
            x1 = history[i + 1]

            xs = np.linspace(x0 - 1.5, x0 + 1.5, 50)
            ys = f0 + df0 * (xs - x0)
            plt.plot(xs, ys, 'orange', linestyle='--', alpha=0.8)
            plt.scatter(x0, f0, color='red')
            plt.scatter(x1, 0, color='purple', marker='x', s=80)
            plt.text(x1, 0, f"x{i+1}", color='purple', fontsize=9, va='bottom')

        plt.title('Método de Newton-Raphson – Tangentes sucessivas')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.legend()
        plt.grid(True, linestyle=':', alpha=0.5)
        plt.tight_layout()
        plt.show()
    if abs(f(xk)) > tol:
        raise ValueError
    return xk

def secante(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-6,
    max_iter: int = 100,
    plot: bool = True
) -> float:
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
        plot (bool, optional): Se True, exibe o gráfico das iterações. Padrão: True.

    Raises:
        ZeroDivisionError: Se ocorrer divisão por zero ao calcular o próximo iterando.
        ValueError: Se `a`, `b`, `f(a)` ou `f(b)` forem inválidos ou resultarem em infinito/NaN.
        RuntimeError: Se não convergir.

    Returns:
        float: Aproximação da raiz obtida pelo método da secante.
    """
    if math.isnan(a) or math.isnan(b) or math.isinf(a) or math.isinf(b):
        raise ValueError
    
    
    fa, fb = f(a), f(b)
    history = [(a, fa), (b, fb)]
    if any(math.isnan(val) or math.isinf(val) for val in [fa, fb]):
        raise ValueError
    if not all(map(math.isfinite, [a, b])):
        raise ValueError
    if math.isnan(fa) or math.isnan(fb) or math.isinf(fa) or math.isinf(fb):
        raise ValueError
    for _ in range(max_iter):
        if abs(fb - fa) < 1e-15:
            raise ZeroDivisionError("Divisão por zero no método da secante.")

        c = b - fb * (b - a) / (fb - fa)

        if abs(f(c)) < tol:
            history.append((c, f(c)))
            break

        a, b = b, c
        fa, fb = fb, f(c)
        history.append((b, fb))
        fc = f(c)
        if math.isnan(fc) or math.isinf(fc):
            raise ValueError

    if plot:
        x_vals = np.linspace(min(a, b) - 2, max(a, b) + 2, 800)
        y_vals = f(x_vals)

        plt.figure(figsize=(9, 6))
        plt.plot(x_vals, y_vals, 'b', linewidth=1.8, label='f(x)')
        plt.axhline(0, color='black', linestyle='--', linewidth=1)

        for i in range(len(history) - 1):
            x0, f0 = history[i]
            x1, f1 = history[i + 1]
            m = (f1 - f0) / (x1 - x0)

            xs = np.linspace(min(x0, x1) - 0.5, max(x0, x1) + 0.5, 50)
            ys = f1 + m * (xs - x1)
            plt.plot(xs, ys, 'orange', linestyle='--', alpha=0.7)

            plt.scatter([x0, x1], [f0, f1], color=['red', 'green'])
            plt.scatter(x1, 0, color='purple', marker='x', s=80)
            plt.text(x1, 0, f"x{i+1}", color='purple', fontsize=9, va='bottom')

        plt.title('Método da Secante – Aproximações sucessivas')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.legend()
        plt.grid(True, linestyle=':')
        plt.tight_layout()
        plt.show()
    if f(c) > tol:
        raise RuntimeError
    if math.isnan(f(c)) or math.isinf(f(c)):
        raise ValueError
    return c

def raiz(f: Callable[..., object], 
         a: float | None = None,
         b: float | None = None,
         x0: float | None = None,
         tol: float = 1e-6, 
         method: str = "bissecao", 
         max_iter: int = 100, 
         aprox: int = 4,
         plot: bool = True
    ) -> float:
    """
    Função auxiliar para selecionar o método de busca de raiz desejado.

    Encaminha a execução para um dos métodos disponíveis:
    - "bissecao"
    - "secante"
    - "newton"

    Args:
        f (Callable[..., object]): Função alvo cuja raiz se deseja encontrar.
        a (float | None, optional): Limite esquerdo ou primeiro chute inicial (quando aplicável).
        b (float | None, optional): Limite direito ou segundo chute inicial (quando aplicável).
        x0 (float | None, optional): Chute inicial para o método de Newton (quando aplicável).
        tol (float, optional): Tolerância para os métodos. Por padrão 1e-6.
        method (str, optional): Método a ser utilizado: "bissecao", "secante" ou "newton". Por padrão "bissecao".
        max_iter (int, optional): Número máximo de iterações. Padrão: 100.
        aprox (int, optional): Número de casas decimais para arredondamento do resultado. Padrão: 4.
        plot (bool, optional): Se True, exibe gráficos. Padrão: True.

    Raises:
        ValueError: Se o método especificado for inválido.

    Returns:
        float: Aproximação da raiz obtida pelo método selecionado.
    """
    if method not in ("bissecao", "secante", "newton"):
        raise ValueError("Método inválido.")
    if method == "bissecao":
        return round(bissecao(f, a, b, tol, max_iter, plot), aprox) # type: ignore
    elif method == "secante":
        return round(secante(f, a, b, tol, max_iter, plot), aprox) # type: ignore
    elif method == "newton":
        return round(newton(f, x0, tol, max_iter, plot), aprox) # type: ignore
