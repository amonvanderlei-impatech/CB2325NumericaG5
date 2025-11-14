[⬅️ Voltar para a página principal](../README.md)

# CB2325NumericaG5 — Raízes

Este módulo implementa métodos numéricos clássicos para **encontrar raízes de funções reais** em ℝ.
Oferece três algoritmos:

* **Bisseção**
* **Newton–Raphson**
* **Secante**

E também uma função auxiliar que seleciona automaticamente o método desejado.

O módulo pode exibir gráficos das iterações, permitindo visualizar convergência, tangentes e secantes.

| Função                                                    | Descrição                                                      |
| --------------------------------------------------------- | -------------------------------------------------------------- |
| [bissecao](#cb2325numericag5raizesbissecao)(f, a, b, ...) | Encontra uma raiz usando o método da bisseção.                 |
| [newton](#cb2325numericag5raizesnewton)(f, x0, ...)       | Usa derivadas simbólicas (SymPy) e o método de Newton–Raphson. |
| [secante](#cb2325numericag5raizessecante)(f, a, b, ...)   | Aplica o método da secante para encontrar raízes.              |
| [raiz](#cb2325numericag5raizesraiz)(f, a, b, x0, ...)     | Encaminha automaticamente para um dos métodos disponíveis.     |

---

## `CB2325NumericaG5.raizes.bissecao`

`CB2325NumericaG5.raizes.bissecao(f, a, b, tol=1e-6, max_iter=100, plot=True)`

Implementa o método da **bisseção**, utilizado para encontrar uma raiz de uma função contínua no intervalo [a, b], assumindo que há **mudança de sinal**: $f(a) \cdot f(b) < 0$.

A cada iteração o intervalo é reduzido pela metade, convergindo para a raiz.

#### Parâmetros:

**f** : `Callable[[float], float]`
Função contínua que recebe e retorna números reais.

**a** : `float`
Extremo esquerdo do intervalo inicial.

**b** : `float`
Extremo direito do intervalo inicial.

**tol** : `float`, opcional.
Tolerância para o critério de parada em (|f(c)|).
Padrão: `1e-6`.

**max_iter** : `int`, opcional.
Número máximo de iterações.
Padrão: `100`.

**plot** : `bool`, opcional.
Se `True`, exibe o gráfico das iterações.
Padrão: `True`.

#### Retornos:

**c** : `float`
Uma aproximação da raiz no intervalo [a, b].

#### Erros:

**ValueError** :

* Se `a` ou `b` forem inválidos (NaN, infinito ou não finitos).
* Se `f(a)` ou `f(b)` forem inválidos.
* Se não houver mudança de sinal no intervalo.
* Se algum valor no meio das iterações resultar em NaN/infinito.

**RuntimeError** :
Se o método não convergir após `max_iter` iterações.

### Exemplos:

```python
>>> from CB2325NumericaG5.raizes import bissecao
>>> f = lambda x: x**2 - 4
>>> bissecao(f, 0, 5, plot=False)
1.9999998807907104
```

---

## `CB2325NumericaG5.raizes.newton`

`CB2325NumericaG5.raizes.newton(f, x0, tol=1e-6, max_iter=100, plot=True)`

Implementa o método de **Newton–Raphson**, utilizando o SymPy para calcular a derivada automaticamente.

O método utiliza a fórmula iterativa: $x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}$

#### Parâmetros:

**f** : `Callable[[sympy.Symbol|float], sympy.Expr|float]`
Função que aceita símbolos do SymPy ou números reais.

**x0** : `float`
Chute inicial.

**tol** : `float`, opcional.
Tolerância para parada em $|f(x_k)|$.
Padrão: `1e-6`.

**max_iter** : `int`, opcional.
Número máximo de iterações.
Padrão: `100`.

**plot** : `bool`, opcional.
Se `True`, exibe as tangentes iterativas.
Padrão: `True`.

#### Retornos:

**xk** : `float`
Aproximação da raiz encontrada.

#### Erros:

**ZeroDivisionError** :
Se a derivada se tornar 0 em alguma iteração.

**ValueError** :
Se, após as iterações, $|f(x_k)|$ ainda for maior que a tolerância.

### Exemplos:

```python
>>> from CB2325NumericaG5.raizes import newton
>>> import sympy as sp
>>> f = lambda x: x**3 - 2*x - 5
>>> newton(f, x0=2, plot=False)
2.094551481698199
```

---

## `CB2325NumericaG5.raizes.secante`

`CB2325NumericaG5.raizes.secante(f, a, b, tol=1e-6, max_iter=100, plot=True)`

Implementa o método da **secante**, que aproxima derivadas por diferenças finitas usando dois valores iniciais.

Formulação iterativa: $x_{k+1} = x_k - f(x_k)\frac{x_k-x_{k-1}}{f(x_k)-f(x_{k-1})}$

#### Parâmetros:

**f** : `Callable[[float], float]`
Função alvo.

**a** : `float`
Primeiro chute inicial.

**b** : `float`
Segundo chute inicial.

**tol** : `float`, opcional.
Tolerância para parada.
Padrão: `1e-6`.

**max_iter** : `int`, opcional.
Número máximo de iterações.
Padrão: `100`.

**plot** : `bool`, opcional.
Se `True`, exibe o gráfico com as secantes sucessivas.
Padrão: `True`.

#### Retornos:

**c** : `float`
Aproximação da raiz encontrada.

#### Erros:

**ZeroDivisionError** :
Se ocorrer divisão por zero ao calcular a secante.

**ValueError** :
Se `a`, `b`, `f(a)` ou `f(b)` forem inválidos ou resultarem em infinito/NaN.

**RuntimeError** :
Se não convergir.

### Exemplos:

```python
>>> from CB2325NumericaG5.raizes import secante
>>> f = lambda x: x**2 - 3
>>> secante(f, 1, 2, plot=False)
1.7320506804317222
```

---

## `CB2325NumericaG5.raizes.raiz`

`CB2325NumericaG5.raizes.raiz(f, a=None, b=None, x0=None, tol=1e-6, method="bissecao", max_iter=100, aprox=4, plot=True)`

Função auxiliar que permite escolher automaticamente um dos métodos:

* `"bissecao"`
* `"secante"`
* `"newton"`

Encaminha a execução para a função correspondente.

#### Parâmetros:

**f** : `Callable`
Função cuja raiz será buscada.

**a** : `float | None`, opcional.
Intervalo esquerdo ou chute inicial (quando aplicável).

**b** : `float | None`, opcional.
Intervalo direito ou segundo chute inicial (quando aplicável).

**x0** : `float | None`, opcional.
Chute inicial para Newton.

**tol** : `float`, opcional.
Tolerância desejada.
Padrão: `1e-6`.

**method** : `str`, opcional.
Método a utilizar. Pode ser `"bissecao"`, `"secante"` ou `"newton"`.
Padrão: `"bissecao"`.

**max_iter** : `int`, opcional.
Máximo de iterações.
Padrão: `100`.

**aprox** : `int`, opcional.
Número de casas decimais para arredondamento.
Padrão: `4`.

**plot** : `bool`, opcional.
Se `True`, exibe gráficos gerados pelo método escolhido.
Padrão: `True`.

#### Retornos:

**float** :
Aproximação da raiz calculada pelo método selecionado.

#### Erros:

**ValueError** :
Se `method` não for um dos valores válidos.

### Exemplos:

```python
>>> from CB2325NumericaG5.raizes import raiz
>>> f = lambda x: x**3 - 9*x + 1
>>> raiz(f, a=-5, b=5, method="bissecao", plot=False)
-2.8793852416
```
