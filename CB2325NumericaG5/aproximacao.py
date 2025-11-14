import math
from CB2325NumericaG5.graficos_aproximacao import grafico_ajuste_linear, grafico_ajuste_polinomial 

def media(dado: list) -> float:
    """Esta função retorna a média dos elementos da lista dada.

    Args:
        dado (list): Números (inteiros ou float).

    Raises:
        ValueError: A lista está vazia.    
        ValueError: A lista não é composta por números.
        
    Returns:
        float: A média aritmética dos dados fornecidos.
    """    
    if len(dado) == 0:
        raise ValueError("A lista está vazia.")

    for i in dado:
        if not isinstance(i, (int, float)) or math.isnan(i) or math.isinf(i):
            raise ValueError("Os elementos não se tratam de números, logo não há como efetuar sua média.")
    
    
    soma = sum(dado)

    return float(soma/(len(dado))) #deixado float explícito aqui - não era necessário, mas fica mais claro
    
def coeficiente_determinacao(valores_y:list, valores_y_ajustados:list) -> float:
    """Calcula o coeficiente de determinação R² para avaliar a qualidade do ajuste.

    Args:
        valores_y (list): Valores reais de y.
        valores_y_ajustados (list): Valores ajustados de y pela regressão.

    Raises:
        ValueError: As listas de valores_y e valores_y_ajustados devem ter o mesmo tamanho.

    Returns:
        float: O coeficiente de determinação R².
    """
    if len(valores_y) != len(valores_y_ajustados):
        raise ValueError("As listas de valores_y e valores_y_ajustados devem ter o mesmo tamanho.")

    y_medio = media(valores_y)
    soma_erros_quadrados = sum((y - valores_y_ajustados[i]) ** 2 for i, y in enumerate(valores_y))
    soma_total_variacao = sum((y - y_medio) ** 2 for y in valores_y)

    if soma_total_variacao == 0:
        return 0.0

    r_quadrado = 1 - (soma_erros_quadrados / soma_total_variacao)

    return r_quadrado

def regressao_linear(valores_x:list, valores_y:list, mostrar_grafico: bool = True, coeficiente_determinacao_r: bool = True) -> tuple :
    """Calcula os coeficientes (angular,linear) da reta que melhor se ajusta aos dados.
    Args:
        valores_x (list): Coordenada x de cada ponto.
        valores_y (list): Coordenada y de cada ponto.
        mostrar_grafico (bool, optional): Indica se o gráfico de dispersão e a reta de ajuste
        devem ser exibidos automaticamente. Por padrão, é True.
        coeficiente_determinacao_r (bool, optional): Indica se o coeficiente de determinação R² deve ser calculado e exibido no terminal. Por padrão, é True.

    Raises:
        ValueError: A quantidade de abcissas deve ser igual à de ordenadas.

    Returns:
        tuple: Coeficientes da reta de regressão linear. (Coeficiente angular,Coeficiente linear)
    """
    if len(valores_x) != len(valores_y):
        raise ValueError("A quantidade de abcissas deve ser igual à de ordenadas.")

    den_beta_chapeu =  -len(valores_x)*(media(valores_x)*media(valores_x))
    num_beta_chapeu =  -len(valores_x)*media(valores_x)*media(valores_y)

    for k in range(len(valores_x)):
        den_beta_chapeu += valores_x[k]*valores_x[k]
        num_beta_chapeu += valores_x[k]*valores_y[k]
    
    beta_chapeu = num_beta_chapeu/den_beta_chapeu
    alpha_chapeu = media(valores_y) - beta_chapeu*media(valores_x)
    r_quadrado = coeficiente_determinacao(valores_y,[beta_chapeu*x + alpha_chapeu for x in valores_x])

    if mostrar_grafico == True:
        grafico_ajuste_linear(valores_x,valores_y,beta_chapeu,alpha_chapeu,r_quadrado)
    
    if coeficiente_determinacao_r == True:
        print(f"Coeficiente de Determinação R²: {r_quadrado:.2f}")
    
    return (beta_chapeu,alpha_chapeu)

def resolvedor_de_sistemas(MC:list, VI:list, tolerancia:float = 1e-11) -> list:
    """Resolve Sistemas Lineares. Medios e grandes é por Gauss-Jordan.

    Args:
        MC (list): Os coeficientes das incognitas do sistema linear.
        VI (list): Os coeficientes independentes das variáveis.
        tolerancia (float, optional): Abaixo desse valor o número é considerado zero; isso para que não haja divisões por números muito pequenos. Defaults to 1e-11.

    Raises:
        ValueError: Sistema impossível de ser resolvido, alguma linha deu apenas 0.

    Returns:
        list: Lista do valor de cada incognita, caso venha na ordem MC = [[a_x + a_y + a_z + ...], [b_x + b_y+...], ...], a resposta virá em [x,y,z,...].
    """    
    Matriz_Coeficientes = list(MC)
    Vetor_Independentes = list(VI)
    Matriz_Aumentada = [Matriz_Coeficientes[e] + [Vetor_Independentes[e]] for e in range(len(Vetor_Independentes))]

    def prod_linha(linha:list, produtado:float, div=False) -> list[float]:

        auxiliar = [r for r in linha]

        if div == True:
            for r in range(len(linha)):
                auxiliar[r] /= produtado

        else:
            for r in range(len(linha)):
                auxiliar[r] *= produtado

        return auxiliar
    
    def soma_linha_linha(linha:list, somado:list, sub:bool =False) -> list[float]:
        auxiliar = [r for r in linha]

        if sub == True:
            for r in range(len(linha)):
                auxiliar[r] -= somado[r]

        else:
            for r in range(len(linha)):
                auxiliar[r] += somado[r]
        
        return auxiliar

    for kk in range(len(Vetor_Independentes)):
        linhas_trocadas = False
        if abs(Matriz_Aumentada[kk][kk]) <= tolerancia:
            for j in  range(kk+1, len(Vetor_Independentes)):
                if abs(Matriz_Aumentada[j][kk]) > tolerancia:
                    Matriz_Aumentada[j], Matriz_Aumentada[kk] = Matriz_Aumentada[kk], Matriz_Aumentada[j]
                    linhas_trocadas = True
                    break

            if linhas_trocadas == False:
                raise ValueError ("Sistema sem solução única.")

        e = Matriz_Aumentada[kk][kk]
        transicao = list(Matriz_Aumentada[kk])
        Matriz_Aumentada[kk] = prod_linha(transicao, e, True) #Divide aquela linha pelo elemento da diagonal.

        for i in range(kk+1, len(Vetor_Independentes)): #Processo de triangulação
            if abs(Matriz_Aumentada[i][kk]) <= tolerancia:
                Matriz_Aumentada[i][kk] = 0
                continue
            variavel_de_suporte1 = Matriz_Aumentada[i][kk]
            variavel_de_suporte2 = prod_linha(Matriz_Aumentada[kk], variavel_de_suporte1)
            Matriz_Aumentada[i] = soma_linha_linha(Matriz_Aumentada[i], variavel_de_suporte2, True)

    #A partir daqui já temos uma matriz triangular superior.
    x = [0 for i in range(len(Vetor_Independentes))]

    for i in reversed(range(len(Vetor_Independentes))):
        soma = sum(Matriz_Aumentada[i][j] * x[j] for j in range(i + 1, len(Vetor_Independentes)))
        x[i] = (Matriz_Aumentada[i][-1] - soma) / Matriz_Aumentada[i][i]

    return x #retorna [x,y,z,...]

def aproximacao_polinomial(lista_de_coordenadas:list, grau_do_polinomio:int, mostrar_grafico: bool = True, coeficiente_determinacao_r: bool = True) -> list[float]:
    """Utiliza MMQ para fazer a regressão polinomial dos pontos dados. Tudo no plano. Retorna os coeficientes.

    Args:
        lista_de_coordenadas (list): Uma lista dos pontos cuja função vai aproximar.
        grau_do_polinomio (int): Qual tipo de polinômio a função retornará. 1 é linear, por exemplo.
        mostrar_grafico (bool, optional): Indica se o gráfico de dispersão e a curva ajustada
        devem ser exibidos automaticamente. Por padrão, é True.
        coeficiente_determinacao_r (bool, optional): Indica se o coeficiente de determinação R² deve ser calculado e exibido no terminal. Por padrão, é True.

    Raises:
        KeyError: Caso haja menos dados do que o número do grau do polinômio requerido, existirão infinitas "soluções". 

    Returns:
        list: Lista dos coeficientes em ordem crescente de grau.
    """    
    
    suporte = set()
    for i in lista_de_coordenadas:
        suporte.add(i)
    lista_de_coordenadas = [i for i in suporte]
    
    quantidade_de_pontos = len(lista_de_coordenadas)
    
    if quantidade_de_pontos < grau_do_polinomio+1: #Condição necessária para que um polinômio seja encontrado.
        raise KeyError("A quantidade de dados deve ser maior ou igual ao grau do polinômio desejado.")
    #(
    valores_x = [e for e,ee in lista_de_coordenadas]
    valores_y = [ee for e,ee in lista_de_coordenadas]
    # )Isola cada conjunto de dados de cada coordenada num vetor.

    matriz_valores_x = [[e**i for e in valores_x] for i in range(grau_do_polinomio+1)]

    #Feita a matriz de cada xis nos devidos graus para que o polinômio seja encontrado.
    def produto_de_linhas(linha1:list, linha2:list) -> float: #Retorna o elemento da matriz resultado, quando se trata do produto de matrizes.
        """Executa uma operação entre listas do mesmo tamanho.

        Args:
            linha1 (list): Lista de floats.
            linha2 (list): Lista de floats.

        Returns:
            int: O resultado do "produto interno" dos "vetores" fornecidos.
        """        
        contador = 0
        if len(linha1) == len(linha2):
            for i in range(len(linha1)):
                contador += linha1[i]*linha2[i]

        return contador

    matriz_produto_valores_x = [[produto_de_linhas(matriz_valores_x[i],matriz_valores_x[ii]) for i in range(len(matriz_valores_x))] for ii in range(len(matriz_valores_x[0])+1 - len(valores_x)+grau_do_polinomio)] #Menos um ou menos 2? Talvez 1 - (quantidade de dados - grau do polinomio)
    #A matriz que define o sistema de equações que deve ser resolvido. A outra é:

    vetor_valores_y_do_sistema = [produto_de_linhas(valores_y,matriz_valores_x[i]) for i in range(len(matriz_valores_x))]
    vetor_solucao = resolvedor_de_sistemas(matriz_produto_valores_x,vetor_valores_y_do_sistema)
    valores_y_ajustados = [
        sum(vetor_solucao[i]*(x**i) for i in range(len(vetor_solucao))) 
        for x in valores_x
    ]

    r_quadrado = coeficiente_determinacao(valores_y,valores_y_ajustados)

    if mostrar_grafico == True:
        grafico_ajuste_polinomial(valores_x, valores_y, vetor_solucao, r_quadrado)

    if coeficiente_determinacao_r == True:
        print(f"Coeficiente de Determinação R²: {r_quadrado:.2f}")
    
    return vetor_solucao

def txt_aproximacao_polinomial(lista_de_coordenadas:list, grau_do_polinomio:int) -> str:
    """Utiliza MMQ para fazer a regressão polinomial dos pontos dados. Tudo no plano. Retorna o polinômio.

    Args:
        lista_de_coordenadas (list): Uma lista dos pontos cuja função vai aproximar.
        grau_do_polinomio (int): Qual tipo de polinômio a função retornará. 1 é linear, por exemplo.

    Returns:
        str: O polinômio na sua forma por extenso.
    """    
    k = str()
    a = aproximacao_polinomial(lista_de_coordenadas,grau_do_polinomio, False, False) #não mostrar o gráfico e o R² duas vezes

    for i in range(len(a)):
        if a[len(a)-1-i] > 0:
            k+=f"({a[len(a)-1-i]:.3})x^{len(a)-i-1}"
        elif a[len(a)-1-i] == 0:
            continue
        else:
            k+=f" + ({a[len(a)-1-i]:.3})x^{len(a)-i-1} "

    return k

