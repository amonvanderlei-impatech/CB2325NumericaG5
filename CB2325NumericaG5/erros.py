"""
Módulo para cálculo de erros numéricos.

Esse módulo fornece funções para calcular o erro absoluto e o erro relativo entre um valor real e um valor aproximado
"""

def erro_absoluto(valor_real, valor_aprox):
    return 0

def erro_relativo(valor_real, valor_aprox):
    """
    Calcula o erro relativo entre dois valores.
    O erro relativo é o erro absoluto dividido pelo valor absoluto do valor real.
    Fórmula: E_r=|(valor_real-valor_aprox)/valor_real|

    Args:
        valor_real (float): O valor exato ou de referência. Deve ser diferente de zero.
        valor_aprox (_type_): O valor obtido por medição ou aproximação.
        
    Returns:
        float: O erro relativo calculado.
        
    Raises:
        ValueError: Se o valor_real for zero, o que causaria divisão por zero.
    """
    
    if valor_real==0:
        raise ValueError("O valor real não pode ser zero para o cálculo do erro relativo.")
    
    return abs((valor_real-valor_aprox)/valor_real)

if __name__=='__main__':
    # exemplos de uso, conforme solicitado
    erro_rel=erro_relativo(3.141592, 3.14)
    print(f'Erro relativo: {erro_rel:.7f}')