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

        (lambda x: x, 0, 1, 0.5, "trapezios"),       # linear
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

        (lambda x: 1, 0, 3, 3.0, "trapezios"),       # constante
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

        (lambda x: 1, 0, 3, 3.0, "trapezios"),       # constante
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

        (lambda x: 1, 0, 3, 3.0, "trapezios"),       # constante
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

        (lambda x: 1, 0, 3, 3.0, "trapezios"),       # constante
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

        (lambda x: 1, 0, 3, 3.0, "trapezios"),       # constante
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

        (lambda x: 1, 0, 3, 3.0, "trapezios"),       # constante
    ]
)
def teste_graficos(funcao, a, b, esperado, metodo):
    """Testes dos gráficos da integral"""
    resultado = integral(funcao, a, b, n=10, metodo=metodo, plot=False)
    assert resultado == esperado
