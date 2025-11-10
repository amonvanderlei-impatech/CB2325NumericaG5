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











#integral (funcao, a, b, n, aprox=4, metodo="simpson", plot=True)
#testar intervalo não numérico
#Testar integral imprópria, função não definida no intervalo
#Testar n ímpar para simpson
#testar intervalos invertidos
#Testar n=0
#Testar integral de constante
#Testar integral de um ponto (intervalo de b a b)
#Testar sem plotar gráfico
#Testar gráfico invertido
#Testar integral de função par e impar
#Testar limite infinito.





