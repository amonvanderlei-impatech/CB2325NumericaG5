import sys, os
import pytest
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CB2325NumericaG5.integracao import integral 


tolerancia = 0.001
n = 10000


@pytest.mark.parametrize(
    "funcao, a, b, esperado, metodo",
    [
        (lambda x: x, 0, 1, 0.5, "trapezios"),
        (lambda x: x**3 + (45)*x**2, 0, 1, 15.25, "trapezios"),
        (lambda x: x**12 + (-5)*x**2 -(91)*x**3, 0, 2, 252.82, "trapezios"),
        (lambda x: x**12 + (-5)*x**2 -(91)*x**3, -1, 1, -3.1795, "trapezios"),
        (lambda x: 2*x**(-2) + 3*x + 4, 1, 3, 21.333, "trapezios"),
        (lambda x: x/x, 2, 3, 1, "trapezios"),
        (lambda x: x**(1/2), 0, 2, 1.8856, "trapezios"),
        (lambda x: x**(1/2), 0, 2, 1.8856, "simpson"),
    ]
)
def test_polinomios(funcao, a, b, esperado, metodo):
    """Teste da integral de polinômios simples"""
    resultado = integral(funcao, a, b, n, metodo=metodo, plot=False)
    assert resultado == pytest.approx(esperado, abs=tolerancia)


@pytest.mark.parametrize(
    "funcao, a, b, esperado, metodo",
    [
        (lambda x: 1, 0, 3, 3.0, "trapezios"),
        (lambda x: 5, -2, 2, 20.0, "trapezios"),
        (lambda x: math.e, 0, 1, math.e * 1, "trapezios"),
        (lambda x: math.pi, 1, 4, math.pi * 3, "trapezios")
    ]
)
def test_constante(funcao, a, b, esperado, metodo):
    """Teste da integral de funções constantes"""
    resultado = integral(funcao, a, b, n, metodo=metodo, plot=False)
    assert resultado == pytest.approx(esperado, abs=tolerancia)


@pytest.mark.parametrize(
    "funcao, a, b, esperado, metodo",
    [
        (lambda x: x/x + 1, 2, 2, 0, "trapezios"),
        (lambda x: math.sin(x), 2, 2, 0, "simpson"),
    ]
)
def test_pontos(funcao, a, b, esperado, metodo):
    """Teste da integral de pontos"""
    resultado = integral(funcao, a, b, n, metodo=metodo, plot=False)
    assert resultado == pytest.approx(esperado, abs=tolerancia)


@pytest.mark.parametrize(
    "funcao, a, b, esperado, metodo",
    [
        (lambda x: 2*x**3 +(-2)*x**2 +x +21 , 10, -3, -4593.3333, "trapezios"),
        (lambda x: x**2 +3*x +2 , 5, 0, -89.167, "simpson"),
        (lambda x: math.cos(x), math.pi, 0, 0, "simpson"),
    ]
)
def test_intervalos_invertidos(funcao, a, b, esperado, metodo):
    """Teste da integral de intervalos invertidos"""
    resultado = integral(funcao, a, b, n, metodo=metodo, plot=False)
    assert resultado == pytest.approx(esperado, abs=tolerancia)


@pytest.mark.parametrize(
    "funcao, a, b, esperado, metodo",
    [
        (lambda x: x, -1, 1, 0, "trapezios"),
        (lambda x: x**3, -2, 2, 0, "simpson"),
        (lambda x: x**2, -3, 3, 18.0, "trapezios"),
        (lambda x: x**4, -1, 1, 0.4, "simpson"),
        (lambda x: x**4, 0, 1, 0.2, "simpson")
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


def test_limites_nao_numericos():
    """Teste da integral de intervalos não numéricos"""
    with pytest.raises(TypeError):
        integral(lambda x: x, "a", "b", n, metodo="trapezios", plot=False) # type: ignore


def test_simpson_n_impar():
    """Teste de integral de n ímpar para simpson"""
    with pytest.raises(ValueError):
        integral(lambda x: x**2, 0, 1, 9, metodo="simpson", plot=False)


@pytest.mark.parametrize(
    "funcao, a, b, metodo", 
    [
        (lambda x: 23/x, 0, 1, "trapezios"),
        (lambda x: math.sin(x)/(x+1), 3, -1, "simpson"),
    ]
    )
def test_divisao_zero_no_limite(funcao, a, b, metodo):
    """Teste de integral de divisão por zero"""
    with pytest.raises(ValueError):
        integral(funcao, a, b, n, metodo = metodo, plot = False)

@pytest.mark.parametrize(
    "funcao, a, b, metodo", 
    [
        (lambda x: 23/x, -1, 1, "trapezios"),
        (lambda x: math.sin(x)/x, 3, -1, "simpson"),
    ]
    )
def test_divisao_zero_no_interior(funcao, a, b, metodo):
    """Teste de integral de divisão por zero"""
    with pytest.raises(ZeroDivisionError):
        integral(funcao, a, b, n, metodo = metodo, plot = False)


@pytest.mark.parametrize(
    "funcao, a, b, metodo", 
    [
        (lambda x: math.e**(-x), 0, math.inf, "trapezios"),
        (lambda x: math.e**(-x), 0, math.nan, "trapezios"),
        (lambda x: math.e**(-x), math.inf, 1, "simpson"),
        (lambda x: math.e**(-x), math.nan, 1, "simpson")
    ]
    )
def test_inf_nan(funcao, a, b, metodo):
    """Teste da integral de intervalos infinitos e NaN"""
    with pytest.raises(ValueError):
        integral(funcao, a, b, n, metodo = metodo, plot = False)


def test_complexos():
    """Teste da integral de números complexos"""
    with pytest.raises(ValueError):
        integral(lambda x: x**(1/2), -2, -1, n, plot = False)
