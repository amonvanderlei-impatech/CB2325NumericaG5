[⬅️ Voltar para a página principal](../README.md)

# CB2325NumericaG5 — Aproximação

Este módulo implementa funções de análise numérica voltadas para ajuste de curvas e resolução de sistemas lineares.

Ele fornece ferramentas para cálculo de médias, regressões lineares e polinomiais (via método dos mínimos quadrados),
bem como funções auxiliares para avaliar a qualidade do ajuste (R²) e gerar representações textuais de polinômios.

[Clique aqui](graficos_aproximacao.md) para acessar o módulo gráfico utilizado.

| Função | Descrição  |
| ------------------------- | ------------------------- |
| [media](#cb2325numericag5aproximacaomedia)(dado)     | Retorna a média dos elementos da lista dada. |
| [coeficiente_determinacao](#cb2325numericag5aproximacaocoeficiente_determinacao)(valores_y, valores_y_ajustados)        | Calcula o coeficiente de determinação R² para avaliar a qualidade do ajuste. |
| [regressao_linear](#cb2325numericag5aproximacaoregressao_linear)(valores_x, valores_y, ...)             | Calcula os coeficientes (angular e linear) da reta que melhor se ajusta aos dados. |
| [resolvedor_de_sistemas](#cb2325numericag5aproximacaoresolvedor_de_sistemas)(MC, VI, tolerancia)                 | Resolve sistemas lineares por eliminação de Gauss-Jordan. |
| [aproximacao_polinomial](#cb2325numericag5aproximacaoaproximacao_polinomial)(lista_de_coordenadas, grau_do_polinomio, ...)    | Utiliza MMQ (Mínimos Quadrados) para fazer regressão polinomial dos pontos dados. |
| [txt_aproximacao_polinomial](#cb2325numericag5aproximacaotxt_aproximacao_polinomial)(lista_de_coordenadas, grau_do_polinomio) | Gera a expressão textual de um polinômio ajustado via MMQ. |

---

## `CB2325NumericaG5.aproximacao.media`

```CB2325NumericaG5.aproximacao.media(dado)```

Calcula a média dos elementos de uma lista de números.

#### Parâmetros:

**dado** : `list`
Lista de números (inteiros ou floats).

#### Retornos:

**media** : `float`
A média aritmética dos dados fornecidos.

#### Erros:

**ValueError** :
Se a lista estiver vazia.

### Exemplos:

```python
>>> from CB2325NumericaG5.aproximacao import media
>>> media([1, 2, 3])
2.0
```

---

## `CB2325NumericaG5.aproximacao.coeficiente_determinacao`

`CB2325NumericaG5.aproximacao.coeficiente_determinacao(valores_y, valores_y_ajustados)`

Calcula o coeficiente de determinação **R²**, que mede a qualidade do ajuste entre os valores observados e os valores ajustados.

#### Parâmetros:

**valores_y** : `list`
Lista contendo os valores observados (dados reais).

**valores_y_ajustados** : `list`
Lista contendo os valores estimados pelo modelo.

#### Retornos:

**r_quadrado** : `float`
Valor de R² (coeficiente de determinação), variando entre 0 e 1.
Quanto mais próximo de 1, melhor o ajuste do modelo aos dados.

#### Erros:

**ValueError** :
Se as listas `valores_y` e `valores_y_ajustados` tiverem tamanhos diferentes.

### Exemplos:

```python
>>> from CB2325NumericaG5.aproximacao import coeficiente_determinacao
>>> y = [1, 2, 3]
>>> y_ajustado = [1.1, 1.9, 3.0]
>>> coeficiente_determinacao(y, y_ajustado)
0.99
```

---

## `CB2325NumericaG5.aproximacao.regressao_linear`

`CB2325NumericaG5.aproximacao.regressao_linear(valores_x, valores_y, mostrar_grafico=True, coeficiente_determinacao_r=True)`

Calcula os coeficientes angular e linear da reta que melhor se ajusta aos dados, utilizando o método dos **Mínimos Quadrados**.

#### Parâmetros:

**valores_x** : `list`
Coordenadas x dos pontos (variável independente).

**valores_y** : `list`
Coordenadas y dos pontos (variável dependente).

**mostrar_grafico** : `bool`, opcional.
Indica se o gráfico de dispersão e a reta ajustada devem ser exibidos automaticamente.
Padrão: `True`.

**coeficiente_determinacao_r** : `bool`, opcional.
Indica se o coeficiente de determinação R² deve ser calculado e exibido no terminal.
Padrão: `True`.

#### Retornos:

**(beta_chapeu, alpha_chapeu)** : `tuple[float, float]`
Coeficiente angular (inclinação) e coeficiente linear (intercepto) da reta ajustada.

#### Erros:

**ValueError** :
Se o número de elementos em `valores_x` e `valores_y` não for igual.

### Exemplos:

```python
>>> from CB2325NumericaG5.aproximacao import regressao_linear
>>> x = [0, 1, 2, 3, 4]
>>> y = [1.1, 1.9, 3.0, 3.9, 5.2]
>>> a, b = regressao_linear(x, y, coeficiente_determinacao_r=False)
>>> print(f"y = {a:.2f}x + {b:.2f}")
y = 1.02x + 0.98
```

---

## `CB2325NumericaG5.aproximacao.resolvedor_de_sistemas`

`CB2325NumericaG5.aproximacao.resolvedor_de_sistemas(MC, VI, tolerancia=1e-11)`

Resolve sistemas lineares utilizando o método de **Gauss-Jordan**, adequado para sistemas de médio e grande porte.

#### Parâmetros:

**MC** : `list`
Matriz dos coeficientes das incógnitas do sistema linear.

**VI** : `list`
Vetor dos termos independentes (lado direito do sistema).

**tolerancia** : `float`, opcional.
Abaixo desse valor, o número é considerado zero — evita divisões por valores muito pequenos.
Padrão: `1e-11`.

#### Retornos:

**x** : `list`
Lista contendo as soluções do sistema linear, na mesma ordem das variáveis originais.
Por exemplo, se `MC` representa `[x, y, z]`, o retorno será `[x, y, z]`.

#### Erros:

**ValueError** :
Se o sistema não possuir solução única (por exemplo, quando uma linha resulta apenas em zeros).

### Exemplos:

```python
>>> from CB2325NumericaG5.aproximacao import resolvedor_de_sistemas
>>> MC = [[2, 1], [1, -1]]
>>> VI = [4, 0]
>>> resolvedor_de_sistemas(MC, VI)
[1.3333333333333335, 1.3333333333333333]
```

---

## `CB2325NumericaG5.aproximacao.aproximacao_polinomial`

`CB2325NumericaG5.aproximacao.aproximacao_polinomial(lista_de_coordenadas, grau_do_polinomio, mostrar_grafico=True, coeficiente_determinacao_r=True)`

Utiliza o método dos **Mínimos Quadrados (MMQ)** para realizar uma **regressão polinomial** dos pontos fornecidos no plano, retornando os coeficientes do polinômio ajustado.

#### Parâmetros:

**lista_de_coordenadas** : `list`
Lista de pontos (x, y) que serão utilizados no ajuste polinomial.

**grau_do_polinomio** : `int`
Grau do polinômio a ser ajustado.
Exemplo: `1` para linear, `2` para quadrático, etc.

**mostrar_grafico** : `bool`, opcional
Indica se o gráfico de dispersão e a curva ajustada devem ser exibidos automaticamente.
Padrão: `True`.

**coeficiente_determinacao_r** : `bool`, opcional
Indica se o coeficiente de determinação R² deve ser calculado e exibido no terminal.
Padrão: `True`.

#### Retornos:

**vetor_solucao** : `list[float]`
Lista contendo os coeficientes do polinômio ajustado, em ordem crescente de grau (do termo constante até o termo de maior grau).

#### Erros:

**KeyError** :
Se a quantidade de pontos for menor que o grau do polinômio desejado mais um (`grau + 1`), pois não há dados suficientes para determinar uma solução única.

### Exemplos:

```python
>>> from CB2325NumericaG5.aproximacao import aproximacao_polinomial
>>> pontos = [(-2, 5), (0, 1), (2, 5)]
>>> aproximacao_polinomial(pontos, 2, mostrar_grafico=False, coeficiente_determinacao_r=False)
[1.0, 0.0, 1.0]
```

---

## `CB2325NumericaG5.aproximacao.txt_aproximacao_polinomial`

`CB2325NumericaG5.aproximacao.txt_aproximacao_polinomial(lista_de_coordenadas, grau_do_polinomio)`

Utiliza o método dos **Mínimos Quadrados (MMQ)** para calcular a **regressão polinomial** dos pontos fornecidos e retorna o polinômio ajustado em forma de texto legível.

#### Parâmetros:

**lista_de_coordenadas** : `list`
Lista de pontos (x, y) utilizados para o ajuste polinomial.

**grau_do_polinomio** : `int`
Grau do polinômio desejado.
Exemplo: `1` para linear, `2` para quadrático, etc.

#### Retornos:

**polinomio** : `str`
Uma string representando o polinômio ajustado, escrita em forma algébrica, com os coeficientes formatados até três casas decimais.

### Exemplos:

```python
>>> from CB2325NumericaG5.aproximacao import txt_aproximacao_polinomial
>>> pontos = [(-2, 5), (0, 1), (2, 5)]
>>> txt_aproximacao_polinomial(pontos, 2)
'(1.0)x^2+(1.0)x^0'
```
