def erro_absoluto(valor_real:float,valor_aprox:float) -> float:
    """Retorna o erro absoluto entre o valor real de um número e seu valor aproximado
    Calcula o erro absoluto entre dois valores de um mesmo número: seu valor real e seu valor
    aproximado. O erro absoluto é calculado por meio do módulo da diferença entre o valor real e o 
    valor aproximado.
    
    Args:
        valor_real (float): É o valor real (ou exato, caso seja) do número
        valor_aprox (float): É o valor proximado do número

    Returns:
        float: Resultado da cálculo do erro absoluto
    """
    erro = abs(valor_real - valor_aprox)
    return erro

def erro_relativo():
    return 1