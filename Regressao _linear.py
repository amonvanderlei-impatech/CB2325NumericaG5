def media(dado: list) -> float:
    """Esta função retorna a média dos elementos da lista dada.

    Args:
        dado (list): Números (inteiros ou float).

    Returns:
        float: A média aritmética dos dados fornecidos.
    """    

    if len(dado) == 0:

        return 0
    
    else:

        soma = 0

        for i in dado:


            soma += i
        
        return float(soma/(len(dado)))
    

def regressão_linear(xizes:list, ypsilons:list) -> tuple :
    """Calcula os coeficientes (angular,linear) da reta que melhor se ajusta aos dados.
    Args:
        xiszes (list): Coordenada x de cada ponto.
        ypsilons (list): Coordenada y de cada ponto.

    Raises:
        KeyError: A quantidade de abcissas deve ser igual à de ordenadas.

    Returns:
        tuple: Coeficientes da reta de regressão linear. (Coeficiente angular,Coeficiente linear)
    """
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

def aproximacao_polinomial(lista_de_coordenadas:list, grau_do_polinomio:int) -> list:
    """Utiliza MMQ para fazer a regressão polinomial dos pontos dados. Tudo no plano. Retorna os coeficientes.

    Args:
        lista_de_coordenadas (list): Uma lista dos pontos cuja função vai aproximar.
        grau_do_polinomio (int): Qual tipo de polinômio a função retornará. 1 é linear, por exemplo.

    Raises:
        KeyError: Caso haja menos dados do que o número do grau do polinômio requerido, existirão infinitas "soluções". 

    Returns:
        list: Lista dos coeficientes em ordem crescente de grau.
    """    
    quantidade_de_pontos = len(lista_de_coordenadas)

    if quantidade_de_pontos < grau_do_polinomio: #Condição necessária para que um polinômio seja encontrado.

        raise KeyError("A quantidade de dados deve ser maior ou igual ao grau do polinômio desejado.")
    #(
    xiszes = [e for e,ee in lista_de_coordenadas]

    ypsilons = [ee for e,ee in lista_de_coordenadas]

    # )Isola cada conjunto de dados de cada coordenada num vetor.

    matriz_xiszes = [[e**i for e in xiszes] for i in range(grau_do_polinomio+1)]

    #Feita a matriz de cada xis nos devidos graus para que o polinômio seja encontrado.
    def produto_de_rows(row1:list, row2:list) -> int: #Retorna o elemento da matriz resultado, quando se trata do produto de matrizes.
        """Executa uma operação entre listas do mesmo tamanho.

        Args:
            row1 (list): Lista de floats.
            row2 (list): Lista de floats.

        Returns:
            int: O resultado do "produto interno" dos "vetores" fornecidos.
        """        
        if len(row1) == len(row2):

            contador = 0

            for i in range(len(row1)):



                contador += row1[i]*row2[i]

        return contador
    
    matriz_produto_xiszes = [[produto_de_rows(matriz_xiszes[i],matriz_xiszes[ii]) for i in range(len(matriz_xiszes))] for ii in range(len(matriz_xiszes[0])+1 - len(xiszes)+grau_do_polinomio)] #Menos um ou menos 2? Talvez 1 - (quantidade de dados - grau do polinomio)


    #A matriz que define o sistema de equações que deve ser resolvido. A outra é:

    vetor_ypsilons_do_sistema = [produto_de_rows(ypsilons,matriz_xiszes[i]) for i in range(len(matriz_xiszes))]


    vetor_solucao = gauss_jordan(matriz_produto_xiszes,vetor_ypsilons_do_sistema)

    return vetor_solucao



def txt_aproximacao_polinomial(lista_de_coordenadas:list, grau_do_polinômio:int) -> str:
    """Utiliza MMQ para fazer a regressão polinomial dos pontos dados. Tudo no plano. Retorna o polinômio.

    Args:
        lista_de_coordenadas (list): Uma lista dos pontos cuja função vai aproximar.
        grau_do_polin (_type_): Qual tipo de polinômio a função retornará. 1 é linear, por exemplo.

    Returns:
        str: O polinômio na sua forma por extenso.
    """    
    k = str()

    a = aproximacao_polinomial(lista_de_coordenadas,grau_do_polinômio)

    for i in range(len(a)):


        if a[len(a)-1-i] > 0:


            k+=f"+ {a[len(a)-1-i]:.3}*x^{len(a)-i-1} "

        elif a[len(a)-1-i] == 0:

            continue

        else:


            k+=f" {a[len(a)-1-i]:.3}*x^{len(a)-i-1} "

    return k

bolha = [(1,2),(-1,-1),(0,8),(2,2),(5,8),(-21,-44),(-17,-7),(13,4),(35,53),(-3,2),(9,-9),(.12,-.04),(.09,-.009)]
a = aproximacao_polinomial(bolha,3)
print(a)
a = txt_aproximacao_polinomial(bolha,3)
print(a)
