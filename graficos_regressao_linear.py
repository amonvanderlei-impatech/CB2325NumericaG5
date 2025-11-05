import matplotlib.pyplot as plt
import numpy as np

def grafico_ajuste_linear(valores_x:list, valores_y:list, coeficiente_angular:float, coeficiente_linear:float, r_quadrado:float) -> None:
    """Gera o gráfico de dispersão dos pontos e a reta de ajuste linear.
    Args:
        valores_x (list): Coordenada x de cada ponto.
        valores_y (list): Coordenada y de cada ponto.
        coeficiente_angular (float): Coeficiente angular da reta de ajuste linear.
        coeficiente_linear (float): Coeficiente linear da reta de ajuste linear.
        r_quadrado (float): Coeficiente de determinação R².
    """
    plt.scatter(valores_x, valores_y, color='blue', label='Pontos de dados')
    
    x_min = min(valores_x)
    x_max = max(valores_x)
    y_min = coeficiente_angular * x_min + coeficiente_linear
    y_max = coeficiente_angular * x_max + coeficiente_linear

    plt.plot([x_min, x_max], [y_min, y_max], color='red', label=f'Reta de Ajuste Linear (R² = {r_quadrado:.2f})')

    plt.xlabel('Valores X')
    plt.ylabel('Valores Y')
    plt.title('Ajuste Linear')
    plt.legend()
    plt.grid(True)
    plt.show()
    return None


#versão utilizando numpy - a reta de ajuste fica mais suave
def grafico_ajuste_polinomial(valores_x:list, valores_y:list, coeficientes:list, r_quadrado:float) -> None:
    """Gera o gráfico de dispersão dos pontos e a curva de ajuste polinomial.
    Args:
        valores_x (list): Coordenada x de cada ponto.
        valores_y (list): Coordenada y de cada ponto.
        coeficientes (list): Coeficientes do polinômio de ajuste.
        r_quadrado (float): Coeficiente de determinação R².
    """
    plt.scatter(valores_x, valores_y, color='blue', label='Pontos de dados')

    #cria 200 pontos igualmente espaçados entre o min e o max de x para uma curva mais suave
    intervalo_x = np.linspace(min(valores_x), max(valores_x), 200) 

    valores_y_ajustados = []
    #calcula e adiciona os valores de y ajustados usando a expressão do polinomio 
    for x in intervalo_x:
        y=0
        for i in range(len(coeficientes)):
            y += coeficientes[i] * (x ** i)
        valores_y_ajustados.append(y)

    plt.plot(intervalo_x, valores_y_ajustados, color='red', label=f'Curva de Ajuste Polinomial (R² = {r_quadrado:.2f})')

    plt.xlabel('Valores X')
    plt.ylabel('Valores Y')
    plt.title('Ajuste Polinomial')
    plt.legend()
    plt.grid(True)
    plt.show()
