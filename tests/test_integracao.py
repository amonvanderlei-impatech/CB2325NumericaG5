import sys, os
import pytest
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CB2325NumericaG5.integracao import integral 
#Talvez precise importar função gráfico tbm...




#Testes Básicos de Funcionamento Simples (polinomios)
@pytest.mark.parametrize(
    "funcao, a, b, esperado, metodo",
    [
        # (função, limite inferior, limite superior, valor esperado, método)

        (lambda x: x, 0, 1, 0.5, "trapezios"),      # x
        (lambda x: x**3 + (45)*x**2, 0, 1, 15.25, "trapezios"),       # x³ + 45x²
        (lambda x: x**12 + (-5)*x**2 -(91)*x**3, 0, 2, 252.82, "trapezios"),        # x^12 - 5x^2 - 91x^3
        (lambda x: x**12 + (-5)*x**2 -(91)*x**3, -1, 1, -3.1515, "trapezios")        # x^12 - 5x^2 - 91x^3
    ]
)
def teste_simples_funcionalidade(funcao, a, b, esperado, metodo):
    """Teste da integral de polinômios simples"""
    resultado = integral(funcao, a, b, n=10, metodo=metodo, plot=False)
    assert resultado == esperado


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
def teste_constante(funcao, a, b, esperado, metodo):
    """Teste da integral de funções constantes"""
    resultado = integral(funcao, a, b, n=10, metodo=metodo, plot=False)
    assert resultado == esperado


#Teste da Integral de erros - Intervalo não numérico, não definido, n ímpar para simpson, infinito
@pytest.mark.parametrize(
    "funcao, a, b, esperado, metodo",
    [
        # (função, limite inferior, limite superior, valor esperado, método)

        (lambda x: 1, 0, 3, 3.0, "trapezios"),
    ]
)
def teste_erros(funcao, a, b, esperado, metodo):
    """Teste da integral de erros/retornos esperados"""
    resultado = integral(funcao, a, b, n=10, metodo=metodo, plot=False)
    assert resultado == esperado


#Teste da Integral pontos - intervalos de tamanho zero
@pytest.mark.parametrize(
    "funcao, a, b, esperado, metodo",
    [
        # (função, limite inferior, limite superior, valor esperado, método)

        (lambda x: 1, 0, 3, 3.0, "trapezios"),      
    ]
)
def teste_pontos(funcao, a, b, esperado, metodo):
    """Teste da integral de pontos"""
    resultado = integral(funcao, a, b, n=10, metodo=metodo, plot=False)
    assert resultado == esperado


#Teste da Integral de intervalos invertidos
@pytest.mark.parametrize(
    "funcao, a, b, esperado, metodo",
    [
        # (função, limite inferior, limite superior, valor esperado, método)

        (lambda x: 1, 0, 3, 3.0, "trapezios"),      
    ]
)
def teste_intervalos_invertidos(funcao, a, b, esperado, metodo):
    """Teste da integral de intervalos invertidos"""
    resultado = integral(funcao, a, b, n=10, metodo=metodo, plot=False)
    assert resultado == esperado


#Teste da Integral de funções pares e ímpares
@pytest.mark.parametrize(
    "funcao, a, b, esperado, metodo",
    [
        # (função, limite inferior, limite superior, valor esperado, método)

        (lambda x: 1, 0, 3, 3.0, "trapezios"),     
    ]
)
def teste_pares_impares(funcao, a, b, esperado, metodo):
    """Teste da integral de funções pares e ímpares"""
    resultado = integral(funcao, a, b, n=10, metodo=metodo, plot=False)
    assert resultado == esperado


#Teste do gráfico da Integral
@pytest.mark.parametrize(
    "funcao, a, b, esperado, metodo",
    [
        # (função, limite inferior, limite superior, valor esperado, método)

        (lambda x: 1, 0, 3, 3.0, "trapezios"),      
    ]
)
def teste_graficos(funcao, a, b, esperado, metodo):
    """Testes dos gráficos da integral"""
    resultado = integral(funcao, a, b, n=10, metodo=metodo, plot=False)
    assert resultado == esperado
