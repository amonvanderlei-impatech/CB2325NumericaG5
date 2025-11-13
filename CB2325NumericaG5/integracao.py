"""
Módulo de integração numérica — cálculo e visualização de integrais definidas.

Este módulo fornece ferramentas para o cálculo numérico de integrais definidas
de funções reais em um intervalo [a, b], utilizando dois métodos clássicos:
- Regra dos Trapézios
- Regra de Simpson (1/3)

Além de realizar o cálculo, gera representações gráficas
da área sob a curva, facilitando a visualização dos conceitos de integração.

Exemplo de uso:
---------------
>>> from CB2325NumericaG5.integracao import integral
>>> resultado = integral(lambda x: x**2, 0, 2, n=10, metodo="simpson", plot=True)
>>> print(resultado)
2.6667
"""

from typing import Callable, Union
import matplotlib.pyplot as plt
import numpy as np
import math

def _validar_valor_funcao(valor: Union[float, np.ndarray, complex]) -> float:
    """
    Valida se o valor retornado pela função é um número real finito.
    
    Args:
        valor: Valor retornado pela função a ser integrada
        
    Returns:
        float: Valor convertido para float se for válido
        
    Raises:
        ValueError: Se o valor for infinito, NaN ou complexo
    """
    try:
        # Tenta converter para float
        valor_float = float(valor)
        
        # Verifica se é finito (não é inf, -inf ou nan)
        if not np.isfinite(valor_float) and not math.isinf(valor_float) and not math.isnan(valor_float):
            raise ValueError("A função retornou um valor infinito ou NaN")
            
        return valor_float
        
    except (TypeError, ValueError) as e:
        # Se não conseguiu converter para float ou é complexo
        raise ValueError("A função deve retornar números reais em todo o intervalo [a, b] da integral") from e

def _plot_parabola(x0: float, x1: float, x2: float, y0: float, y1: float, y2: float) -> None:
    """
    Gera a representação gráfica de uma parábola que passa por (x0,y0), (x1,y1) e (x2,y2) no intervalo [x0,x2],
    preenchendo a área entre a curva e o eixo x.
    
    Esta função não retorna valor, apenas gera uma representação gráfica da parábola.

    Args:
        x0 (float): x do primeiro ponto da parábola
        x1 (float): x do segundo ponto da parábola
        x2 (float): x do terceiro ponto da parábola
        y0 (float): y do primeiro ponto da parábola
        y1 (float): y do segundo ponto da parábola
        y2 (float): y do terceiro ponto da parábola
    """
    # Encontrando coeficientes a, b, c da parábola y = ax² + bx + c:
    A = np.array([[x0**2, x0, 1],
                  [x1**2, x1, 1], 
                  [x2**2, x2, 1]])
    y_vec = np.array([y0, y1, y2])
    a, b, c = np.linalg.solve(A, y_vec)
    
    # Pontos da parábola
    x_para = np.linspace(x0, x2, 50)
    y_para = a*x_para**2 + b*x_para + c
    
    plt.plot(x_para, y_para, 'r--', alpha=0.7, linewidth=1)
    plt.fill_between(x_para, 0, y_para, alpha=0.2, color='red')

def integral(
        funcao: Callable[[Union[float, np.ndarray]], Union[float, np.ndarray]],
        a: float,
        b: float,
        n: int,
        aprox: int = 4,
        metodo: str = "simpson",
        plot: bool = True
    ) -> float:
    """
    Calcula numericamente a integral definida de uma função no intervalo [a, b],
    utilizando o método dos trapézios ou a regra de Simpson (1/3) e 
    gera uma representação gráfica da integral.
    
    Se `a > b`, o resultado será negativo, seguindo a convenção matemática.

    O método dos trapézios aproxima a área sob a curva dividindo o intervalo em
    `n` subintervalos igualmente espaçados e somando as áreas dos trapézios formados
    entre os pontos consecutivos.

    Já a regra de Simpson aproxima a integral pela soma das áreas sob polinômios quadráticos
    que interpolam a função, proporcionando maior precisão com o mesmo número de
    subdivisões — desde que `n` seja par.

    Args:
        funcao (Callable[[Union[float, np.ndarray]], Union[float, np.ndarray]]): Função a ser integrada.
        a (float): Limite inferior de integração.
        b (float): Limite superior de integração.
        n (int): Número de subdivisões (intervalos) utilizados na aproximação. Para o método de Simpson, `n` deve ser par.
        aprox (int, optional): Número de casas decimais para arredondamento do resultado. O padrão é 4.
        metodo (str, optional): Método de integração numérica a ser utilizado: `"trapezios"` ou `"simpson"`. O padrão é `"simpson"`.
        plot (bool, optional): Se True, exibe a representação gráfica da integral. O padrão é True.
        
    Raises:
        ValueError: Se o método for `"simpson"` e `n` for ímpar.
        ValueError: Se o argumento `metodo` não for `"trapezios"` nem `"simpson"`.
        ValueError: Se `n` não for um inteiro positivo.
        ValueError: Se `aprox` não for um inteiro não negativo.
        TypeError: Se os limites de integração `a` e `b` não forem números reais.
        TypeError: Se `funcao` não for chamável (callable).

    Returns:
        float: Valor aproximado da integral definida de `funcao` no intervalo [a, b],
        arredondado para o número de casas decimais especificado em `aprox`.
    """
    # Validação da entrada
    if not callable(funcao):
        raise TypeError("O argumento 'funcao' deve ser chamável (callable).")
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Os limites de integração 'a' e 'b' devem ser números reais.")
    if not isinstance(n, int) or n <= 0:
        raise ValueError("O número de subdivisões 'n' deve ser um inteiro positivo (> 0).")
    if not isinstance(aprox, int) or aprox < 0:
        raise ValueError("O número de casas decimais 'aprox' deve ser um inteiro não negativo (>= 0).")
    if metodo not in ("trapezios", "simpson"):
        raise ValueError("Método inválido! Use 'trapezios' ou 'simpson'.")
    
    # Valida se a e b são finitos
    if not np.isfinite(a) or not np.isfinite(b):
        raise ValueError("Os limites de integração 'a' e 'b' devem ser números reais finitos.")
    
    # Testa a função nos limites para validação antecipada
    try:
        _validar_valor_funcao(funcao(a))
        _validar_valor_funcao(funcao(b))
    except Exception as e:
        raise ValueError(f"Função inválida nos limites de integração: {e}")

    
    funcao_vec = np.vectorize(funcao, otypes=[float])

    # Cálculo da integral
    dx = (b - a) / n
    soma = 0.0
    
    if metodo == "trapezios":
        for i in range(n):
            x1 = a + i * dx
            x2 = a + (i + 1) * dx
            y1 = _validar_valor_funcao(funcao_vec(x1))
            y2 = _validar_valor_funcao(funcao_vec(x2))
            soma += (y1 + y2) * dx / 2
                
    else: # metodo == "simpson"
        if n % 2 != 0:
            raise ValueError("Para o método de Simpson, o número de subintervalos 'n' deve ser par.")
        for i in range(n + 1):
            x = a + i * dx
            if i == 0 or i == n:
                soma += _validar_valor_funcao(funcao_vec(x))
            elif i % 2 == 1:
                soma += 4 * _validar_valor_funcao(funcao_vec(x))
            else:
                soma += 2 * _validar_valor_funcao(funcao_vec(x))
                
        soma *= dx / 3

    if plot:
        x = np.linspace(a-0.11*(b-a), b + 0.11*(b-a), 100)
        y = funcao_vec(x)

        plt.figure(figsize=(10, 6))

        plt.plot(x, y, label='f(x)', linewidth=2, linestyle='-', color='black')

        plt.title(f"Integração de f(x) = {round(float(soma), aprox)} — método: {metodo.capitalize()}", fontsize=16, fontweight='bold')
        plt.xlabel("x", fontsize=12)
        plt.ylabel("y", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=12)

        # Garantia do eixo x (y=0) estar sempre no gráfico
        y_min = min(np.min(y), 0)
        y_max = max(np.max(y), 0) 

        # Margem para visualização total do gráfico
        margem_y = 0.1 * (y_max - y_min)
        margem_x = 0.1 * (b - a)
        plt.ylim(y_min - margem_y, y_max + margem_y)
        plt.xlim(a-margem_x, b + margem_x)

        #Eixos x e y
        plt.axhline(y=0, color='black', linewidth=1.5, linestyle='-')
        plt.axvline(x=0, color='black', linewidth=1.5, linestyle='-')

        # Limites da integração
        plt.plot([a, a], [0, funcao_vec(a)], color='black', linewidth=1.5, linestyle='-')
        plt.plot([b, b], [0, funcao_vec(b)], color='black', linewidth=1.5, linestyle='-')
        
        # Plot da integral
        if metodo == "trapezios":
            for i in range(n):
                x_i = a + i * dx
                x_i2 = a + (i + 1) * dx
        
                x_trap = [x_i, x_i, x_i2, x_i2, x_i]  # Pontos do trápezio (inf esquerdo, sup esquerdo, sup direito, inf direito)
                y_trap = [0, funcao_vec(x_i), funcao_vec(x_i2), 0, 0] # 5º ponto para fechar o polígono
        
                plt.fill(x_trap, y_trap, alpha=0.3, color='orange', edgecolor='black')

        else: # metodo == "simpson"
            for i in range(0,n,2):
                x_i = a + i * dx
                x_i2 = a + (i + 1) * dx
                x_i3 = a + (i + 2) * dx
                y_i, y_i2, y_i3 = float(funcao_vec(x_i)), float(funcao_vec(x_i2)), float(funcao_vec(x_i3))

                _plot_parabola(x_i, x_i2, x_i3, y_i, y_i2, y_i3)

        plt.show()

    return round(float(soma), aprox)
