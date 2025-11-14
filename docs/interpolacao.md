[⬅️ Voltar para a página principal](../README.md)

# CB2325NumericaG5 — Interpolação

Este módulo implementa métodos para **construção e avaliação de polinômios interpoladores**.
São fornecidas três classes principais:

* **PoliInterp** — interpolação polinomial de **Lagrange**
* **InterpLinear** — interpolação **linear por partes**
* **PoliHermite** — interpolação **de Hermite** (usando função e derivada)

Todas as classes validam os dados de entrada e produzem **expressões simbólicas (SymPy)**. Além disso, cada classe possui o método `grafico(precisao: int = 100) -> None` que exibe o polinômio ou segmentos interpoladores.

| Classe                                                    | Descrição                                                    |
| --------------------------------------------------------- | ------------------------------------------------------------ |
| [Interpolacao](#cb2325numericag5interpolacaointerpolacao) | Classe base, valida entradas e provê funcionalidades comuns. |
| [PoliInterp](#cb2325numericag5interpolacaopoliinterp)     | Interpolação polinomial de Lagrange.                         |
| [InterpLinear](#cb2325numericag5interpolacaointerplinear) | Interpolação linear por segmentos.                           |
| [PoliHermite](#cb2325numericag5interpolacaopolihermite)  | Interpolação polinomial de Hermite.                          |

---

# `CB2325NumericaG5.interpolacao.Interpolacao`

Classe base responsável por verificar e armazenar os dados necessários para qualquer interpolação.

`Interpolacao(dominio, imagem, imagem_derivada=None)`

### Parâmetros

**dominio** : `list`
Lista contendo os pontos do domínio (números reais distintos).

**imagem** : `list`
Valores da função nos pontos do domínio.

**imagem_derivada** : `list | None`, opcional.
Valores da derivada nos pontos do domínio (necessário apenas para Hermite).
Padrão: `None`.

### Validações realizadas

A classe verifica:

* `dominio`, `imagem` (e `imagem_derivada`, se fornecida) devem ser listas.
* Todos os valores devem ser **números reais**, não podem ser `nan` ou `inf`.
* `dominio` e `imagem` devem ter o **mesmo tamanho**.
* `dominio` deve ter **valores distintos**.
* `dominio` deve ter **pelo menos 2 pontos**.
* Se `imagem_derivada` for passada, deve:
  * ser uma lista
  * ter mesmo tamanho que `dominio`
  * conter apenas números reais válidos

### Atributos

**x** : `sympy.Symbol`
Símbolo usado para expressões simbólicas.

**dominio** : `list`
Domínio validado.

**imagem** : `list`
Imagem validada.

**imagem_derivada** : `list | None`
Derivadas fornecidas (se aplicável).

### Método

#### `grafico(precisao: int = 100) -> None`

Gera um gráfico do polinômio interpolador armazenado em `self.pol`.

##### Parâmetros

**precisao** : `int`
Número de pontos usados na plotagem.
Padrão: `100`.

##### Erros

* `TypeError` : caso `precisao` não seja inteiro.

---

# `CB2325NumericaG5.interpolacao.PoliInterp`

Interpolação polinomial pelo método **de Lagrange**.

`
PoliInterp(dominio, imagem)
`

Constrói automaticamente o polinômio interpolador:

$P(x) = \sum_{i=0}^{n-1} y_i , L_i(x)$

onde $L_i(x)$ são os polinômios básicos de Lagrange.

### Parâmetros

**dominio** : `list`
Pontos distintos.

**imagem** : `list`
Valores reais correspondentes.

### Atributos

**pol** : `sympy.Expr`
Polinômio interpolador simplificado.

**x** : `sympy.Symbol`
Variável simbólica.

### Métodos

#### `__repr__()`

Retorna a expressão simbólica como string.

#### `__call__(p)`

Avalia ou representa o polinômio.

##### Comportamento:

* Se `p` for `sympy.Symbol`: retorna string em **LaTeX**.
* Se `p` for número real:
  * Só avalia se **dentro do intervalo**
    [min(dominio), max(dominio)]
  * Retorna `int` ou `float` conforme apropriado.

##### Erros:

* `ValueError` : se `p` não for número real nem símbolo.
* `ValueError` : se `p` estiver fora do domínio (extrapolação proibida).

#### `__eq__(other)`

Permite comparar polinômios de Lagrange e Hermite pela igualdade simbólica.

### Exemplo

```python
>>> from CB2325NumericaG5.interpolacao import PoliInterp
>>> from sympy import Symbol
>>> x = Symbol("x")
>>> p = PoliInterp([0, 1, 2], [1, 3, 2])
>>> p(1)
3
>>> p(x)
'- \\frac{3 x^{2}}{2} + \\frac{7 x}{2} + 1'
```

---

# `CB2325NumericaG5.interpolacao.InterpLinear`

Interpolação linear por partes (segmentos de reta).

`InterpLinear(dominio, imagem)`

Ordena os pontos, constrói as retas entre pares sucessivos e organiza em um dicionário.

### Parâmetros

**dominio** : `list`
Valores reais distintos.

**imagem** : `list`
Correspondentes valores da função.

### Atributos

**pares_ord** : `tuple[]`
Lista de pares ordenados `(xi, yi)` em ordem crescente de `xi`.

**pol** : `dict`
Dicionário que mapeia cada intervalo `(xi, xi+1)` para a expressão simbólica da reta correspondente.

### Métodos

#### `__repr__()`

Retorna o dicionário de segmentos.

#### `_eval(pos, t)`

Avalia simbolicamente a reta no intervalo `pos = (xi, xi+1)`.

#### `__call__(p)`

Avalia a interpolação linear no ponto `p`.

##### Comportamento:

* Aceita apenas números reais.
* Encontra o intervalo correspondente e avalia nele.
* **Não permite extrapolação**.

##### Erros:

* `ValueError` : se `p` não for número real.
* `ValueError` : se estiver fora do domínio.

#### `__eq__(other)`

Compara dicionários de segmentos linearmente iguais.

#### `grafico(precisao=100)`

Gera um gráfico segmentado, com cada reta plotada separadamente.

##### Parâmetros:

* **precisao** : `int`
  Será dividido proporcionalmente entre os intervalos.

##### Erros:

* `TypeError` : se não for inteiro.

### Exemplo

```python
>>> from CB2325NumericaG5.interpolacao import InterpLinear
>>> l = InterpLinear([0, 1, 2], [1, 3, 2])
>>> l(1.5)
2.5
```

---

# `CB2325NumericaG5.interpolacao.PoliHermite`

Interpolação polinomial **de Hermite**, usando função e derivada em cada ponto.

`PoliHermite(dominio, imagem, imagem_derivada)`

Constrói automaticamente o polinômio:

$H(x) = \sum_{j=0}^{n-1} \left[ y_j,H_{x_j}(x) + y'*j,H*{y_j}(x) \right]$

onde os termos são gerados a partir dos polinômios de Lagrange e suas derivadas.

### Parâmetros

**dominio** : `list`
Pontos distintos.

**imagem** : `list`
Valores reais.

**imagem_derivada** : `list`
Valores reais das derivadas.

### Atributos

**coef_lagrange** : `dict`
Armazena, para cada índice `j`, o par: $(L_j(x), L'_j(x))$

**pol** : `sympy.Expr`
Polinômio interpolador simplificado.

### Métodos

#### `__repr__()`

Retorna o polinômio como string simbólica.

#### `_hx_j(j)`

Computa a base de Hermite associada ao valor $y_j$.

#### `_hy_j(j)`

Computa a base associada à derivada $y_j'$.

#### `_hermite()`

Combina todas as bases para construir o polinômio final.

#### `__call__(p)`

Avalia ou retorna o polinômio em formato LaTeX.

##### Comportamento:

* Se for símbolo, retorna LaTeX.
* Se for número, só avalia dentro do intervalo do domínio.

##### Erros:

* `ValueError` : se tipo inválido.
* `ValueError` : extrapolação não permitida.

#### `__eq__(other)`

Compara polinômios de Hermite e Lagrange por igualdade simbólica.

### Exemplo

```python
>>> from CB2325NumericaG5.interpolacao import PoliHermite
>>> from sympy import Symbol
>>> x = Symbol("x")
>>> p = PoliHermite([0, 1, 2], [1, 3, 2], [3, 2, 1])
>>> p(1)
3
>>> p(x)
'\\frac{9 x^{5}}{4} - \\frac{41 x^{4}}{4} + \\frac{59 x^{3}}{4} - \\frac{31 x^{2}}{4} + 3 x + 1'
```
