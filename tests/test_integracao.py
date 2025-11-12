import sys, os
import pytest
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CB2325NumericaG5.integracao import integral 

# Adicionar teste para infinitos
# Adicionar teste de números complexos

tolerancia = 0.001
n = 10000

#Teste Integral de Polinomios
@pytest.mark.parametrize(
    "funcao, a, b, esperado, metodo",
    [
        # (função, limite inferior, limite superior, valor esperado, método)

        (lambda x: x, 0, 1, 0.5, "trapezios"),      # x
        (lambda x: x**3 + (45)*x**2, 0, 1, 15.25, "trapezios"),       # x³ + 45x²
        (lambda x: x**12 + (-5)*x**2 -(91)*x**3, 0, 2, 252.82, "trapezios"),        # x^12 - 5x^2 - 91x^3
        (lambda x: x**12 + (-5)*x**2 -(91)*x**3, -1, 1, -3.1795, "trapezios"),        # x^12 - 5x^2 - 91x^3
        (lambda x: 2*x**(-2) + 3*x + 4, 1, 3, 21.333, "trapezios"),      # 2x^-2 + 3x + 4
        (lambda x: x/x, 2, 3, 1, "trapezios"),      # x/x
        # (lambda x: math.e**(-x), 0, math.inf, 1, "trapezios"), Mudar caso teste para um teste de infinitos     # e^(-x) 
        (lambda x: x**(1/2), 0, 2, 1.8856, "trapezios"),
        (lambda x: x**(1/2), 0, 2, 1.8856, "simpson"),
        # (lambda x: x**(1/2), -2, -1, 0, "trapezios") Mudar caso teste para um teste de complexos
    ]
)
def test_polinomios(funcao, a, b, esperado, metodo):
    """Teste da integral de polinômios simples"""
    resultado = integral(funcao, a, b, n, metodo=metodo, plot=False)
    assert resultado == pytest.approx(esperado, abs=tolerancia)


#Teste da Integral de Funções Constantes
@pytest.mark.parametrize(
    "funcao, a, b, esperado, metodo",
    [
        # (função, limite inferior, limite superior, valor esperado, método)

        (lambda x: 1, 0, 3, 3.0, "trapezios"),      # constante 1
        (lambda x: 5, -2, 2, 20.0, "trapezios"),        # constante 5
        (lambda x: math.e, 0, 1, math.e * 1, "trapezios"),      # constante e
        (lambda x: math.pi, 1, 4, math.pi * 3, "trapezios")     # constante pi
    ]
)
def test_constante(funcao, a, b, esperado, metodo):
    """Teste da integral de funções constantes"""
    resultado = integral(funcao, a, b, n, metodo=metodo, plot=False)
    assert resultado == pytest.approx(esperado, abs=tolerancia)


#Teste da Integral pontos - intervalos de tamanho zero
@pytest.mark.parametrize(
    "funcao, a, b, esperado, metodo",
    [
        # (função, limite inferior, limite superior, valor esperado, método)

        (lambda x: x/x + 1, 2, 2, 0, "trapezios"),      # intervalo de tamanho zero
        (lambda x: math.sin(x), 2, 2, 0, "simpson"),     # intervalo de tamanho zero 
    ]
)
def test_pontos(funcao, a, b, esperado, metodo):
    """Teste da integral de pontos"""
    resultado = integral(funcao, a, b, n, metodo=metodo, plot=False)
    assert resultado == pytest.approx(esperado, abs=tolerancia)


#Teste da Integral de intervalos invertidos
@pytest.mark.parametrize(
    "funcao, a, b, esperado, metodo",
    [
        # (função, limite inferior, limite superior, valor esperado, método)

        (lambda x: 2*x**3 +(-2)*x**2 +x +21 , 10, -3, -4593.3333, "trapezios"),     # 2*x^3 - 2*x^2 + x + 21
        (lambda x: x**2 +3*x +2 , 5, 0, -89.167, "simpson"),       # x^2 + 3*x + 2
        (lambda x: math.cos(x), math.pi, 0, 0, "simpson"),      # cos(x)
        # (lambda x: math.sin(x)/x, 3, -1, -2.7947, "simpson") Mudar esse caso teste para o teste de divisão por zero
    ]
)
def test_intervalos_invertidos(funcao, a, b, esperado, metodo):
    """Teste da integral de intervalos invertidos"""
    resultado = integral(funcao, a, b, n, metodo=metodo, plot=False)
    assert resultado == pytest.approx(esperado, abs=tolerancia)


#Teste da Integral de funções pares e ímpares
@pytest.mark.parametrize(
    "funcao, a, b, esperado, metodo",
    [
        # (função, limite inferior, limite superior, valor esperado, método)

        (lambda x: x, -1, 1, 0, "trapezios"),      # x
        (lambda x: x**3, -2, 2, 0, "simpson"),     # x^3
        (lambda x: x**2, -3, 3, 18.0, "trapezios"),   # x^2
        (lambda x: x**4, -1, 1, 0.4, "simpson"),    # x^4
        (lambda x: x**4, 0, 1, 0.2, "simpson")    # x^4
    ]
)
def test_pares_impares(funcao, a, b, esperado, metodo):
    """Teste da integral de funções pares e ímpares"""
    resultado = integral(funcao, a, b, n, metodo=metodo, plot=False)
    assert resultado == pytest.approx(esperado, abs=tolerancia)


#Teste do gráfico da Integral
teste_graficos = False
if teste_graficos == True:
    integral(lambda x: x**2, -3, 3, n, metodo="trapezios", plot=True)
    print("18")
    print("-----")
    integral(lambda x: x**3, -2, 2, n, metodo="simpson", plot=True)
    print("0")
    print("-----")
    integral(lambda x: x**12 + (-5)*x**2 -(91)*x**3, 0, 2, n, metodo="trapezios", plot=True)
    print("252.82")
    print("-----")
    integral(lambda x: x**12 + (-5)*x**2 -(91)*x**3, -1, 1, n, metodo="trapezios", plot=True)
    print("-3.1515")
    print("-----")
    integral(lambda x: 2*x**(-2) + 3*x + 4, 1, 3, n, metodo="trapezios", plot=True)
    print("21.333")
    print("-----")


#Teste da Integral de erros - Intervalo não numérico, não definido, n ímpar para simpson, infinito
def test_limites_nao_numericos():
    with pytest.raises(TypeError):
        integral(lambda x: x, "a", "b", n, metodo="trapezios", plot=False) # type: ignore


def test_simpson_n_impar():
    with pytest.raises(ValueError):
        integral(lambda x: x**2, 0, 1, 9, metodo="simpson", plot=False)


def test_divisao_zero():
    with pytest.raises(ZeroDivisionError):
        integral(lambda x: 23/x, 0, 1, 1, metodo="trapezios", plot=False)
