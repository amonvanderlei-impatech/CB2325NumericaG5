"""
Módulo para cálculo de erros numéricos.

Esse módulo fornece funções para calcular o erro absoluto e o erro relativo entre um valor real e um valor aproximado.
"""

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
    """
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
        ValueError: Se o valor_real for zero, o que causaria divisão por zero.
    """
    
    if valor_real==0:
        raise ValueError("O valor real não pode ser zero para o cálculo do erro relativo.")
    
    return round(abs((valor_real-valor_aprox)/valor_real), casas_decimais)
