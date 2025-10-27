def media(dado): #recebe uma lista de inteiros e retorna a sua média
    if len(dado) == 0:
        return 0
    else:
        soma = 0

        for i in dado:
            soma += i
        
        return soma/(len(dado))
def regressão_linear(xizes,ypsilons):
    if len(xizes) != len(ypsilons):
        raise KeyError(" A quantidade de abcissas deve ser igual à de ordenadas.")
    

    den_beta_chapeu =  -len(xizes)*(media(xizes)*media(xizes))
    num_beta_chapeu =  -len(xizes)*media(xizes)*media(ypsilons)


    for k in range(len(xizes)):

        den_beta_chapeu += xizes[k]*xizes[k]

        num_beta_chapeu += xizes[k]*ypsilons[k] 
    
    beta_chapeu = num_beta_chapeu/den_beta_chapeu

    alpha_chapeu = media(ypsilons) - beta_chapeu*media(xizes)

    return (beta_chapeu,alpha_chapeu)

x = [0,1,2,3,4]
y = [1.1,1.9,3.0,3.9,5.2]
b,a = regressão_linear(x,y)
print(f"y = {b:.2f}x + {a:.2f}")

def gauss_jordan(A, b, tol=1e-12):
    """
    Resolve o sistema linear Ax = b pelo método de Gauss-Jordan, sem usar numpy.

    Parâmetros:
    ------------
    A : lista de listas (n x n)
        Matriz dos coeficientes.
    b : lista (n)
        Vetor dos termos independentes.
    tol : float
        Tolerância para detectar pivôs nulos.

    Retorna:
    ---------
    x : lista
        Solução do sistema linear.
    """

    # Número de equações
    n = len(A)

    # Monta a matriz aumentada [A|b]
    for i in range(n):
        A[i] = A[i] + [b[i]]

    # Eliminação de Gauss-Jordan
    for i in range(n):
        # Encontra o pivô máximo (para estabilidade numérica)
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k

        # Verifica se o pivô é nulo
        if abs(A[max_row][i]) < tol:
            raise ValueError("Sistema sem solução única (pivô nulo).")

        # Troca de linha se necessário
        A[i], A[max_row] = A[max_row], A[i]

        # Normaliza a linha do pivô
        pivot = A[i][i]
        A[i] = [a / pivot for a in A[i]]

        # Elimina as outras linhas
    for j in range(n):
        if j != i:
            fator = A[j][i]
            A[j] = [A[j][k] - fator * A[i][k] for k in range(n+1)]

    # Extrai a solução (última coluna)
    x = [A[i][-1] for i in range(n)]
    return x