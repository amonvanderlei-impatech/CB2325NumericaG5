from typing import Callable

def integral(funcao: Callable[[float], float], a: float, b: float, n: int, aprox: int = 4) -> float:
    """
    Calcula a integral definida de uma função em um intervalo [a, b] utilizando o método dos trapézios.

    A área sob a curva é aproximada pela soma das áreas de `n` trapézios, 
    formados a partir dos valores da função nos pontos igualmente espaçados entre `a` e `b`.

    Args:
        funcao (Callable[[float], float]): Função cujos valores serão integrados.
        a (float): Limite inferior de integração.
        b (float): Limite superior de integração.
        n (int): Número de subdivisões (trapézios) utilizados na aproximação.
        approx (int, optional): Número de casas decimais do resultado. O padrão é 4.

    Returns:
        float: Valor aproximado da integral definida no intervalo [a, b].
    """
    dx = (b - a) / n
    soma = 0.0
    
    for i in range(n):
        x1 = a + i * dx
        x2 = a + (i + 1) * dx
        soma += (funcao(x1) + funcao(x2)) * dx / 2
    
    return round(soma, aprox)
