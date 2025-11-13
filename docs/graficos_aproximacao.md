[⬅️ Voltar para a página principal](../README.md)

# CB2325NumericaG5 — Gráficos de Ajuste

Este módulo implementa funções para geração de gráficos relacionados a ajustes lineares e polinomiais realizados por métodos numéricos.

Ele fornece ferramentas para visualizar os pontos dados, a reta de regressão linear e curvas de regressão polinomial, incluindo a exibição do coeficiente de determinação R².

[Clique aqui](aproximacao.md) para acessar o módulo aproximação e ver mais exemplos de uso do módulo gráfico.

| Função                                                                                                      | Descrição                                                       |
| ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| [grafico_ajuste_linear](#cb2325numericag5graficosgrafico_ajuste_linear)(valores_x, valores_y, ...)         | Gera o gráfico de dispersão e a reta de ajuste linear.          |
| [grafico_ajuste_polinomial](#cb2325numericag5graficosgrafico_ajuste_polinomial)(valores_x, valores_y, ...) | Gera o gráfico de dispersão e a curva ajustada de um polinômio. |

---

## `CB2325NumericaG5.graficos.grafico_ajuste_linear`

`CB2325NumericaG5.graficos.grafico_ajuste_linear(valores_x, valores_y, coeficiente_angular, coeficiente_linear, r_quadrado)`

Gera o **gráfico de dispersão** dos pontos fornecidos e plota a **reta de ajuste linear** obtida por regressão.

A função também exibe no gráfico o valor do coeficiente de determinação **R²**, que representa a qualidade do ajuste.

#### Parâmetros:

**valores_x** : `list`
Lista contendo os valores da coordenada x dos pontos.

**valores_y** : `list`
Lista contendo os valores da coordenada y dos pontos.

**coeficiente_angular** : `float`
Coeficiente angular da reta ajustada.

**coeficiente_linear** : `float`
Coeficiente linear da reta ajustada.

**r_quadrado** : `float`
Valor do coeficiente de determinação R² associado ao ajuste.

#### Retornos:

**None** :
A função apenas exibe o gráfico, não há retorno de valor.

### Exemplos:

```python
>>> from CB2325NumericaG5.graficos_aproximacao import grafico_ajuste_linear
>>> x = [0, 1, 2, 3]
>>> y = [1.1, 2.0, 2.9, 4.2]
>>> grafico_ajuste_linear(x, y, coeficiente_angular=1.03, coeficiente_linear=0.95, r_quadrado=0.998)
```

---

## `CB2325NumericaG5.graficos.grafico_ajuste_polinomial`

`CB2325NumericaG5.graficos.grafico_ajuste_polinomial(valores_x, valores_y, coeficientes, r_quadrado)`

Gera o **gráfico de dispersão** dos pontos fornecidos e plota a **curva ajustada de um polinômio**, cujos coeficientes foram determinados previamente por regressão polinomial.

A curva é representada de forma suave utilizando 200 pontos igualmente espaçados no intervalo determinado pelos valores de x.

#### Parâmetros:

**valores_x** : `list`
Valores da coordenada x dos pontos.

**valores_y** : `list`
Valores da coordenada y dos pontos.

**coeficientes** : `list`
Lista contendo os coeficientes do polinômio ajustado, em ordem crescente (termo constante até o de maior grau).

**r_quadrado** : `float`
Coeficiente de determinação R² associado ao ajuste polinomial.

#### Retornos:

**None** :
A função apenas exibe o gráfico, não há retorno de valor.

### Exemplos:

```python
>>> from CB2325NumericaG5.graficos_aproximacao import grafico_ajuste_polinomial
>>> x = [-2, 0, 2]
>>> y = [5, 1, 5]
>>> coef = [1.0, 0.0, 1.0]  # y = x² + 1
>>> grafico_ajuste_polinomial(x, y, coef, r_quadrado=1.0)
```
