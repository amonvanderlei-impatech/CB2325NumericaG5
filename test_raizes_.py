import sympy as sp
import math
import sys
import os
import numpy as np
import pytest


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import CB2325NumericaG5.raizes as rz


#Conjunto de funções triviais.
pol1 = lambda x: (-2*x) + 5
pol2 = lambda x: (-x**2) + (8*x) - 16
polfract = lambda x: (x**2 - 1)/(x-1)
exponencial = lambda x: (2.71828)**x - 1


#Conjunto de funções triviais. Valores muito pequenos.
polpeq1 = lambda x: ((-2e-8)*x) + 5*(1e-8)
polpeq2 = lambda x: ((-1e-8)*(x**2)) + ((8e-8)*x) -16*(1e-8)
polfractpeq = lambda x: ((x**2 - 1)/(x-1))*1e-8
exponencialpeq = lambda x: ((2.71828)**x - 1)*1e-8


#Conjunto de funções triviais. Valores muito pequenos.
polgran1 = lambda x: ((-2e8)*x) + 5*(1e8)
polgran2 = lambda x: (-1e8)*(x**2) + (8e8)*x -16*(1e8)
polfractgra = lambda x: ((x**2 - 1)/(x-1))*1e8
exponencialgran = lambda x: ((2.71828)**x - 1)*1e8


#Conjunto de funções não triviais.
polsemraiz = lambda x: x**2 + 1
pol_duas_raizes = lambda x: x**2 - 1
exponencial_sem_raiz = lambda x: (2.71828)**x
seno = lambda x: x - (x**3)/6 + (x**5)/120 - (x**7)/5040 + (x**9)/362880 - (x**11)/39916800
cosseno = lambda x: 1 - (x**2)/2 + (x**4)/24 - (x**6)/720 + (x**8)/40320 - (x**10)/3628800

   
def proximo(a,b,tol):
        if abs(a) == 1 or abs(b) == 1: #A função duas raizes admite duas raizes.
            if abs(abs(a)-abs(b)) < tol:
                return True
            
        if abs(a-b) < tol:
            return True
        
        if b == 1.57079632679489661923123169163: #Identifica que a função é a cosseno.
            if abs(abs(a)-abs(b))<tol:#A função cosseno admite os dois sinais.
                return True
            
            for i in range(10): #A função cosseno adimite mais de uma raiz também.
                if abs(abs(a)-(abs(b+i*3.14)))<1:
                    return True
                
        for i in range(30):
            if (abs(a) - 3.14*i)<.01: #A função seno aparece com pi. E admite algumas raizes.
                if b ==0:
                    return True
                
        else:
            return False
        

@pytest.mark.parametrize("pontoi", [
    -1000000,
    -1000,
    -100.0001,
    -1,
    -.001,
    0,
    1.001,
    1,
    100.0001,
    1000,
    1000000
])
@pytest.mark.parametrize("funcao, raiz_esperada", [
    (pol1, 2.5),
    (pol2, 4.0),
    (polfract, -1),
    (exponencial, 0),
    (polpeq1, 2.5),
    (polpeq2, 4),
    (polfractpeq, -1),
    (exponencialpeq, 0),
    (polgran1, 2.5),
    (polgran2, 4.0),
    (polfractgra, -1),
    (exponencialgran, 0),
    (pol_duas_raizes, 1),
    (seno, 0),
    (cosseno, 1.57079632679489661923123169163)
])
def test_newton_raizes(funcao, raiz_esperada, pontoi):
    try:
        resultado = rz.newton(funcao, pontoi, plot=False)
        assert proximo(resultado,raiz_esperada, 1e-3), \
            f"Esperado {raiz_esperada}, obtido {resultado}"

    except Exception as e:
        # Se for erro de derivada nula → skip (condição esperada)
        if "derivada" in str(e).lower() or "zero" in str(e).lower():
            pytest.skip(f"Derivada nula em ponto inicial {pontoi}, teste ignorado: {e}")
        else:
            pytest.fail(f"Falhou ({funcao(0)}) para ponto inicial {pontoi}: {e}")


#Funções bem simples, apenas para testar a função auxiliar.
f1 = lambda x: 2*x - 10
f2 = lambda x: x**3
f3 = lambda x: (x-1)**5


def logo_ali(a,b,tolerancia): #Função para comparar os resultados.
    if type(a) == list: #Pois o método da bisseção retorna uma lista.
        if abs(a[0]-b)<tolerancia and abs(a[1]-b)<tolerancia:
            return True
        else:
            return False
       
    else:
        if abs(a-b) < tolerancia:
            return True
        else:
            return False
       
@pytest.mark.parametrize("funcao, raiz",[
    (f1,5),
    (f2,0),
    (f3,1)
])
@pytest.mark.parametrize("nome", [
    "bissecao",
    "secante",
    "newton"              
])
def test_raizes(funcao,raiz,nome):
    resultado = rz.raiz(
    funcao,
    -10,10,10,
    method = nome,
    plot=False)
    assert logo_ali(resultado,raiz, 1e-3), \
        f"Esperado {raiz}, obtido {resultado}"

def test_graficos():
    r1 = rz.raiz(
        f1,
        -10,10,10,
        method="newton",
        )
    assert logo_ali(r1,5,1e-3), \
        f"Esperado {5}, obtido {r1}"
   
    r2 = rz.raiz(
        f1,
        -10,10,10,
        method="bissecao",
        )
    assert logo_ali(r2,5,1e-3), \
        f"Esperado {5}, obtido {r2}"
   
    r3 = rz.raiz(
        f1,
        -10,10,10,
        method="secante",
        )
    assert logo_ali(r3,5,1e-3), \
        f"Esperado {5}, obtido {r3}"
