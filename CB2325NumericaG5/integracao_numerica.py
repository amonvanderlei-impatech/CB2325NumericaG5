from typing import Callable

def integral(funcao: Callable[[float], float], a: float, b: float, n: int, aprox: int = 4, metodo = "simpson") -> float:
    """
    Calcula numericamente a integral definida de uma função no intervalo [a, b],
    utilizando o método dos trapézios ou a regra de Simpson (1/3).

    O método dos trapézios aproxima a área sob a curva dividindo o intervalo em
    `n` subintervalos igualmente espaçados e somando as áreas dos trapézios formados
    entre os pontos consecutivos.

    Já a regra de Simpson aproxima a integral pela soma das áreas sob polinômios quadráticos
    que interpolam a função, proporcionando maior precisão com o mesmo número de
    subdivisões — desde que `n` seja par.

    Args:
        funcao (Callable[[float], float]): Função a ser integrada.
        a (float): Limite inferior de integração.
        b (float): Limite superior de integração.
        n (int): Número de subdivisões (intervalos) utilizados na aproximação. Para o método de Simpson, `n` deve ser par.
        aprox (int, optional): Número de casas decimais do resultado. O padrão é 4.
        metodo (str, optional): Método de integração numérica a ser utilizado: `"trapezios"` ou `"simpson"`. O padrão é `"simpson"`.
        
    Raises:
        ValueError: Se o método for `"simpson"` e `n` for ímpar.
        ValueError: Se o argumento `metodo` não for `"trapezios"` nem `"simpson"`.

    Returns:
        float: Valor aproximado da integral definida de `funcao` no intervalo [a, b],
        arredondado para o número de casas decimais especificado em `aprox`.
    """
    # Validação da entrada
    if not callable(funcao):
        raise TypeError("O argumento 'funcao' deve ser uma função que receba um float e retorne um float.")
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Os limites de integração 'a' e 'b' devem ser números reais.")
    if not isinstance(n, int) or n <= 0:
        raise ValueError("O número de subdivisões 'n' deve ser um inteiro positivo.")
    if metodo not in ("trapezios", "simpson"):
        raise ValueError("Método inválido! Use 'trapezios' ou 'simpson'.")
    
    # Cálculo da integral
    dx = (b - a) / n
    soma = 0.0
    
    if metodo == "trapezios":
        for i in range(n):
            x1 = a + i * dx
            x2 = a + (i + 1) * dx
            soma += (funcao(x1) + funcao(x2)) * dx / 2
                
    else: # metodo == "simpson"
        if n % 2 != 0:
            raise ValueError("Para o método de Simpson, o número de subintervalos 'n' deve ser par.")
        for i in range(n + 1):
            x = a + i * dx
            if i == 0 or i == n:
                soma += funcao(x)
            elif i % 2 == 1:
                soma += 4 * funcao(x)
            else:
                soma += 2 * funcao(x)
                
        soma *= dx / 3

    return round(soma, aprox)
