[⬅️ Voltar para a página principal](../README.md)

# CB2325NumericaG5 — Integração Numérica

Este módulo implementa funções para **cálculo numérico de integrais definidas** e suas respectivas **representações gráficas** utilizando métodos clássicos de integração.

Ele fornece ferramentas para validar funções, gerar parábolas usadas na regra de Simpson e calcular integrais por:

* Regra dos Trapézios
* Regra de Simpson (1/3)

| Função                                                                            | Descrição                                                           |
| --------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| [_validar_valor_funcao](#cb2325numericag5integracao_validar_valor_funcao)(valor) | Valida valores retornados pela função integrada.                    |
| [_plot_parabola](#cb2325numericag5integracao_plot_parabola)(x0, x1, ...)         | Gera a representação gráfica da parábola usada na regra de Simpson. |
| [integral](#cb2325numericag5integracaointegral)(funcao, a, b, n, ...)            | Calcula a integral definida pelos métodos dos trapézios ou Simpson. |

---

## `CB2325NumericaG5.integracao._validar_valor_funcao`

`CB2325NumericaG5.integracao._validar_valor_funcao(valor)`

Valida se o valor retornado pela função integrada é **real**, **finito** e **não complexo**, garantindo a consistência matemática da integração.

#### Parâmetros:

**valor** : `float | np.ndarray | complex`
Valor retornado pela função que está sendo integrada.

#### Retornos:

**float**
O valor convertido para `float`, caso seja válido.

#### Erros:

**ValueError** :
Se o valor retornado for infinito, NaN ou complexo.

### Exemplos:

```python
>>> from CB2325NumericaG5.integracao import _validar_valor_funcao
>>> _validar_valor_funcao(3.5)
3.5
```

---

## `CB2325NumericaG5.integracao._plot_parabola`

`CB2325NumericaG5.integracao._plot_parabola(x0, x1, x2, y0, y1, y2)`

Gera a **representação gráfica de uma parábola** que passa pelos três pontos fornecidos
$((x_0, y_0)), ((x_1, y_1)), ((x_2, y_2))$ — utilizada na regra de Simpson.

A área sob a curva é preenchida para auxiliar na visualização.

#### Parâmetros:

**x0, x1, x2** : `float`
Coordenadas x dos três pontos usados na interpolação parabólica.

**y0, y1, y2** : `float`
Coordenadas y dos pontos correspondentes.

#### Retornos:

**None**

### Exemplos:

```python
>>> from CB2325NumericaG5.integracao import _plot_parabola
>>> _plot_parabola(0, 1, 2, 1, 2, 1)
```

---

## `CB2325NumericaG5.integracao.integral`

`CB2325NumericaG5.integracao.integral(funcao, a, b, n, aprox=4, metodo="simpson", plot=True)`

Calcula numericamente a **integral definida** de uma função real no intervalo [a, b], utilizando o **método dos trapézios** ou a **regra de Simpson (1/3)**.

Opcionalmente, gera o **gráfico da área sob a curva**, ilustrando o processo de integração.

Se (a > b), o resultado segue a convenção matemática e será **negativo**.

#### Parâmetros:

**funcao** : `Callable[[Union[float, np.ndarray]], Union[float, np.ndarray]]`
Função a ser integrada.

**a** : `float`
Limite inferior da integração.

**b** : `float`
Limite superior da integração.

**n** : `int`
Número de subdivisões do intervalo.
Para `"simpson"`, deve ser **par**.

**aprox** : `int`, opcional.
Número de casas decimais para arredondamento.
Padrão: `4`.

**metodo** : `str`, opcional.
Método de integração numérica: `"trapezios"` ou `"simpson"`.
Padrão: `"simpson"`.

**plot** : `bool`, opcional.
Se `True`, exibe a representação gráfica da integração.
Padrão: `True`.

#### Retornos:

**float**
Valor aproximado da integral definida de `funcao` no intervalo ([a, b]),
arredondado conforme `aprox`.

#### Erros:

**TypeError** :
Se `funcao` não for chamável.
Se `a` ou `b` não forem números reais.

**ValueError** :
Se `n` ≤ 0.
Se `aprox` < 0.
Se `metodo` não for `"trapezios"` ou `"simpson"`.
Se `metodo="simpson"` e `n` for ímpar.
Se a função retornar valores inválidos (complexos, inf, NaN).

### Exemplos:

```python
>>> from CB2325NumericaG5.integracao import integral
>>> resultado = integral(lambda x: x**2, 0, 2, n=10, metodo="simpson", plot=True)
>>> print(resultado)
2.6667
```
