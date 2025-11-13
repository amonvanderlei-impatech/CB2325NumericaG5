import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CB2325NumericaG5.erros import erro_absoluto, erro_relativo, soma_de_kahan

valor_real = 3.141592
valor_aprox = 3.14

ea = erro_absoluto(valor_real, valor_aprox)
er = erro_relativo(valor_real, valor_aprox)

lista_valores = [2.5,-1.1,0.000000001,10000000]
soma_kahan = soma_de_kahan(lista_valores)

print(ea, er)
print(soma_kahan)