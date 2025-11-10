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
        if b == 1.57079632679489661923123169163: #A função cosseno admite os dois sinais.
            if abs(abs(a)-abs(b))<tol:
                return True
            for i in range(10):
                if abs(abs(a)-(abs(b+i*3.14)))<1:
                    return True
        for i in range(30):
            if (abs(a) - 3.14*i)<.01: #A função seno aparece com pi.
                if b ==0:
                    return True
        else:
            return False
