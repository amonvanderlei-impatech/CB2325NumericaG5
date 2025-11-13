"""
Módulo para cálculo de erros numéricos.

Esse módulo fornece funções para calcular o erro absoluto e o erro relativo entre um valor real e um valor aproximado.
"""
from typing import List


def erro_absoluto(valor_real: float, valor_aprox: float, casas_decimais: int = 6) -> float:
    """
    Retorna o erro absoluto entre o valor real de um número e seu valor aproximado,
    de acordo com a quantidade desejada de casas decimais.
    Calcula o erro absoluto entre dois valores de um mesmo número: seu valor real e seu valor
    aproximado. O erro absoluto é calculado por meio do módulo da diferença entre o valor real e o 
    valor aproximado.
    
    Args:
        valor_real (float): É o valor real (ou exato, caso seja) do número
        valor_aprox (float): É o valor aproximado do número
        casas_decimais (int, optional): Número de casas decimais do resultado. Por padrão, é 6.

    Returns:
        float: Resultado do cálculo do erro absoluto
        
    Raises:
        TypeError: se o `valor_real` e o `valor_aprox` não forem float ou int
        ValueError: se `casas_decimais` não for um inteiro não negativo
    """
    if not isinstance(valor_aprox, (int, float)) or not isinstance(valor_real, (int, float)):
        raise TypeError("O valor real e o valor aproximado devem ser números reais.")
    if not isinstance(casas_decimais, int) or casas_decimais<0:
        raise ValueError("O número de casas decimais deve ser um inteiro não-negativo.")
    erro = abs(valor_real - valor_aprox)
    return round(erro, casas_decimais)

def erro_relativo(valor_real: float, valor_aprox: float, casas_decimais: int = 6) -> float:
    """
    Retorna o erro relativo entre o valor real de um número e seu valor aproximado, de acordo 
    com a quantidade desejada de casas decimais.
    O erro relativo é o erro absoluto dividido pelo valor absoluto do valor real.
    Fórmula: E_r=|(valor_real-valor_aprox)/valor_real|

    Args:
        valor_real (float): O valor exato ou de referência. Deve ser diferente de zero.
        valor_aprox (float): O valor obtido por medição ou aproximação.
        casas_decimais (int, optional): Número de casas decimais do resultado. Por padrão, é 6.
        
    Returns:
        float: O erro relativo calculado, arredondado para o número de casas decimais 
        especificado em `casas_decimais`.
        
    Raises:
        ValueError: Se o `valor_real` for zero, o que causaria divisão por zero.
        TypeError: se o `valor_real` e o `valor_aprox` não forem float ou int
        ValueError: se `casas_decimais` não for um inteiro não negativo
    """
    
    if valor_real==0:
        raise ValueError("O valor real não pode ser zero para o cálculo do erro relativo.")
    if not isinstance(valor_aprox, (int, float)) or not isinstance(valor_real, (int, float)):
        raise TypeError("O valor real e o valor aproximado devem ser números reais.")
    if not isinstance(casas_decimais, int) or casas_decimais<0:
        raise ValueError("O número de casas decimais deve ser um inteiro não-negativo.")
    
    return round(abs((valor_real-valor_aprox)/valor_real), casas_decimais)

def soma_de_kahan(lista_de_valores: List[float]) -> float:
    """
    O algoritmo de soma de Kahan é um método de análise numérica que
    visa minimizar o erro numérico (erro de arredondamento) ao somar 
    uma sequência de números de ponto flutuante de precisão finita. 
    Se o usuário decidir somar uma lista de números que possua valores 
    muito grandes e valores muito pequenos, como a precisão dos computadores
    é limitida, os dígitos de baixa ordem (menos significativos) do número 
    pequeno podem ser perdidos durante a operação de adição devido ao 
    arrendondamento. Para minimizar essa falha, o algoritmo da soma de Kahan
    mantém uma variável de "compensação" durante a realização da soma, a qual
    acumula os dígitos de baixa ordem "perdidos" a cada etapa da operação. A
    cada nova etapa de adição, esse erro é usado para "ajustar" o próximo número
    que será somado, compensando a perda de precisão do anterior.

    Args:
        lista_de_valores (float[]): A lista dos valores de ponto fluante que se deseja somar

    Returns:
        float: Retorna a soma compensada dos números de ponto flutuante fornecidos
        
    Raises:
        TypeError: Se `lista_de_valores` não for uma lista.
    """
    
    if not isinstance(lista_de_valores, list):
        raise TypeError ("a lista de valores fornecida deve ser uma lista")
    
    soma_total = 0.0 # a soma corrente 
    compensação = 0.0 # a variável que será a compensação
    
    for valor in lista_de_valores: 
        if not isinstance(valor, float) and not isinstance(valor, int): # se o valor fornecido não for um float ou um inteiro, a operação não é realizada
            continue 
        
        v = valor - compensação # a cada valor, desconta-se a compensação
        soma_auxiliar = soma_total + v # a soma auxiliar pega a soma total corrente e adicona o valor após a compensação
        compensação = (soma_auxiliar - soma_total) - v # a compensação é atualizada 
        soma_total = soma_auxiliar # a soma total corrente é atualizada com o valor da soma armazenada na variável auxiliar
    
    return soma_total 
