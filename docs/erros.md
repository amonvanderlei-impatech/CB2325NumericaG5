[⬅️ Voltar para a página principal](../README.md)

# CB2325NumericaG5 — Erros Numéricos

Este módulo implementa funções voltadas para análise de erros numéricos, permitindo a avaliação da precisão de aproximações e a realização de somas de alta estabilidade numérica utilizando o algoritmo de Kahan.

Ele fornece ferramentas para cálculo de erro absoluto, erro relativo e soma compensada de números em ponto flutuante.

| Função                                                                              | Descrição                                                               |
| ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| [erro_absoluto](#cb2325numericag5erroserro_absoluto)(valor_real, valor_aprox, ...) | Calcula o erro absoluto entre dois valores numéricos.                   |
| [erro_relativo](#cb2325numericag5erroserro_relativo)(valor_real, valor_aprox, ...) | Calcula o erro relativo entre dois valores numéricos.                   |
| [soma_de_kahan](#cb2325numericag5errossoma_de_kahan)(lista_de_valores)             | Realiza uma soma estável numericamente utilizando o algoritmo de Kahan. |

---

## `CB2325NumericaG5.erros.erro_absoluto`

`CB2325NumericaG5.erros.erro_absoluto(valor_real, valor_aprox, casas_decimais=6)`

Calcula o **erro absoluto** entre um valor real e um valor aproximado, arredondado a um número configurável de casas decimais.

O erro absoluto é definido como:

$E_a = |\text{valor\_real} - \text{valor\_aprox}|$

#### Parâmetros:

**valor_real** : `float`
Valor exato ou referência do número.

**valor_aprox** : `float`
Valor aproximado a ser comparado.

**casas_decimais** : `int`, opcional.
Número de casas decimais desejadas no resultado.
Padrão: `6`.

#### Retornos:

**erro_absoluto** : `float`
Erro absoluto entre os valores fornecidos, arredondado.

#### Erros:

**TypeError** :
Se `valor_real` ou `valor_aprox` não forem números reais.

**ValueError** :
Se `casas_decimais` não for um inteiro não negativo.

### Exemplos:

```python
>>> from CB2325NumericaG5.erros import erro_absoluto
>>> erro_absoluto(3.141592, 3.14)
0.001592
```

---

## `CB2325NumericaG5.erros.erro_relativo`

`CB2325NumericaG5.erros.erro_relativo(valor_real, valor_aprox, casas_decimais=6)`

Calcula o **erro relativo** entre um valor real e um valor aproximado, arredondado ao número desejado de casas decimais.

O erro relativo é definido como:

$E_r = \left|\frac{\text{valor\_real} - \text{valor\_aprox}}{\text{valor\_real}}\right|$

#### Parâmetros:

**valor_real** : `float`
Valor exato ou referência. Deve ser diferente de zero.

**valor_aprox** : `float`
Valor obtido por medição ou aproximação.

**casas_decimais** : `int`, opcional.
Número de casas decimais desejadas no resultado.
Padrão: `6`.

#### Retornos:

**erro_relativo** : `float`
Erro relativo calculado, arredondado conforme especificado.

#### Erros:

**ValueError** :
Se `valor_real` for zero (divisão por zero).

**TypeError** :
Se `valor_real` ou `valor_aprox` não forem números reais.

**ValueError** :
Se `casas_decimais` não for um inteiro não negativo.

### Exemplos:

```python
>>> from CB2325NumericaG5.erros import erro_relativo
>>> erro_relativo(3.141592, 3.14)
0.000507
```

---

## `CB2325NumericaG5.erros.soma_de_kahan`

`CB2325NumericaG5.erros.soma_de_kahan(lista_de_valores)`

Realiza a soma de uma lista de valores utilizando o **algoritmo de Kahan**, que reduz significativamente o erro de arredondamento em somas de números de ponto flutuante.

Este método é especialmente útil quando a lista contém números de magnitudes muito diferentes (muito grandes e muito pequenos).

#### Parâmetros:

**lista_de_valores** : `float[]`
Lista contendo os valores que serão somados.

#### Retornos:

**soma_compensada** : `float`
Soma final dos valores fornecidos, com compensação de erros de arredondamento.

#### Erros:

**TypeError** :
Se `lista_de_valores` não for uma lista.

*(Valores não numéricos na lista são ignorados automaticamente.)*

### Exemplos:

```python
>>> from CB2325NumericaG5.erros import soma_de_kahan
>>> soma_de_kahan([2.5,-1.1,0.000000001,10000000])
10000001.4
```
