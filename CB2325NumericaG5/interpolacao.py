"""
Módulo para cálculo de polinômios interpoladores.

Este módulo fornece classes para construir e avaliar polinômios interpoladores a partir de
listas de pontos no plano. Inclui implementações para:
- interpolação de Lagrange (PoliInterp),
- interpolação linear por partes (InterpLinear),
- interpolação de Hermite usando valores e derivadas (PoliHermite).

As classes validam entradas, constroem expressões simbólicas (SymPy) e expõem um método
`grafico(precisao: int = 100) -> None` para esboçar o polinômio ou os segmentos.
"""


from sympy import symbols, simplify, lambdify, Number, latex, Symbol
from numpy import linspace
from matplotlib.pyplot import show, subplots
from typing import Union
import numbers
import math


class Interpolacao:
    """
    Classe base para verificar e armazenar os dados de entrada comuns às interpolações.

    Args:
        dominio (list): Lista de pontos do domínio (valores numéricos, distintos).
        imagem (list): Lista de valores da função nos pontos do domínio (numéricos).
        imagem_derivada (list | None): Lista com os valores da derivada nos pontos do domínio,
            ou None quando não aplicável. Valor padrão: None.

    Raises:
        TypeError: Se `dominio`, `imagem` (ou `imagem_derivada`, quando fornecida) não for do tipo list,
            ou se algum elemento das listas não for um número real (verifica math.inf e math.nan).
        ValueError: Se `dominio` e `imagem` tiverem comprimentos diferentes, se `imagem_derivada`
            tiver comprimento diferente, se `dominio` contiver valores repetidos ou
            se `dominio` tiver menos de 2 pontos.

    Attributes:
        x (sympy.Symbol): Símbolo interno usado para construir expressões simbólicas.
        dominio (list): Domínio validado (lista de números reais).
        imagem (list): Valores da função no domínio (lista de números reais).
        imagem_derivada (list | None): Valores das derivadas no domínio (lista de números reais) ou None.
    """


    def __init__(self, dominio:list, imagem:list, imagem_derivada:Union[list, None] = None):
        # Garantimos que o domínio e a imagem são listas de pontos
        if not isinstance(dominio, list) or not isinstance(imagem, list):
            raise TypeError('`dominio` e `imagem` devem ser do tipo list')

        # Garantimos que o domínio e a imagem possuem a mesma quantidade de pontos
        if len(dominio) != len(imagem):
            raise ValueError('`dominio` e `imagem` devem ter a mesma quantidade de pontos')

        # Garantimos que o domínio não possui pontos repetidos
        if len(set(dominio)) != len(dominio):
            raise ValueError('`dominio` não pode ter valores repetidos')

        # Garantimos que o domínio possui mais de 2 pontos
        if len(dominio) < 2:
            raise ValueError('`dominio` deve possuir mais de 2 pontos')

        # Garantimos que o domínio é uma lista de números
        for i in dominio:
            if not isinstance(i, numbers.Real):
                raise TypeError('`dominio` deve ser uma lista de números reais')
            if math.isinf(i):
                raise ValueError('`dominio` contém infinito')
            if math.isnan(i):
                raise ValueError('`dominio` contém NaN')

        # Garantimos que a imagem é uma lista de números
        for i in imagem:
            if not isinstance(i, numbers.Real):
                raise TypeError('`imagem` deve ser uma lista de números reais')
            if math.isinf(i):
                raise ValueError('`imagem` contém infinito')
            if math.isnan(i):
                raise ValueError('`imagem` contém NaN')

        # Cria as variáveis internas
        self.x = symbols('x')
        self.dominio = dominio[:]
        self.imagem = imagem[:]

        if imagem_derivada is not None:
            # Garantimos que a imagem_derivada é uma lista de pontos
            if not isinstance(imagem_derivada, list):
                raise TypeError('`imagem_derivada` deve ser do tipo list')

            # Garantimos que o domínio e a imagem_derivada possuem a mesma quantidade de pontos
            if len(dominio) != len(imagem_derivada):
                raise ValueError('`dominio` e `imagem` devem ter a mesma quantidade de pontos')

            # Garantimos que a imagem_derivada é uma lista de números
            for i in imagem_derivada:
                if not isinstance(i, numbers.Real):
                    raise TypeError('`imagem_derivada` deve ser uma lista de números reais')
                if math.isinf(i):
                    raise ValueError('`imagem_derivada` contém infinito')
                if math.isnan(i):
                    raise ValueError('`imagem_derivada` contém NaN')

            # Cria uma variável interna
            self.imagem_derivada = imagem_derivada[:]

    def __repr__(self):
        raise NotImplementedError

    def __call__(self, p:Union[int, float, Symbol]):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError
    
    def grafico(self, precisao:int = 100) -> None:
        """
        Esboça o gráfico da classe Interpolacao
        
        Args:
            precisao (int, opcional): número de pontos do polinomio a serem calculados. Padroniza em 100.

        Raises:
            TypeError: se precisão não for do tipo int
        """
        
        #Garante que precisao seja do tipo int
        if not isinstance(precisao, int):
            raise TypeError("precisao deve ser do tipo int")

        #Preparação
        x_simb = symbols('x')
        _, ax = subplots()
        ax.set_aspect("equal")
        
        #Determinação dos limites do gráfico
        xmin, xmax, ymin, ymax = min(self.dominio), max(self.dominio), min(self.imagem), max(self.imagem)
        mini, maxi = min(xmin, ymin), max(xmax, ymax)
        ax.set_xlim(mini-1, maxi+1)
        ax.set_ylim(mini-1, maxi+1)

        #Conversão do polinomio
        y_vals = linspace(xmin, xmax, precisao)
        y_lamb = lambdify(x_simb, self.pol, "numpy")
        y_func = y_lamb(y_vals)
        if isinstance(y_func, (int, float)):
                y_func = [y_func]*precisao
        
        #Esboço da curva e dos pontos
        ax.plot(y_vals, y_func)
        for i in range(len(self.dominio)):
                x_ponto, y_ponto = self.dominio[i], self.imagem[i]
                ax.plot(x_ponto, y_ponto, "o")
        
        #Exibição
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True)
        show()


class PoliInterp(Interpolacao):
    """
    Polinômio interpolador baseado no método de Lagrange.

    Constrói o polinômio interpolador de Lagrange simplificado a partir de
    listas `dominio` e `imagem` fornecidas na construção da instância.

    Args:
        dominio (list): Lista de pontos do domínio (valores numéricos distintos).
        imagem (list): Lista de valores da função nos pontos do domínio (numéricos).

    Raises:
        ValueError: Se o ponto passado para `__call__` não for um número real nem um
            `sympy.Symbol`, ou se o ponto numérico estiver fora do intervalo [min(dominio), max(dominio)]
            (extrapolação não permitida).

    Attributes:
        pol (sympy.Expr): Polinômio interpolador simplificado (expressão simbólica).
        x (sympy.Symbol): Símbolo interno herdado de Interpolacao.

    Usage:
        p = PoliInterp(dominio, imagem)
        str(p)         # representação do polinômio
        p(sym)         # retorna LaTeX do polinômio se sym for sympy.Symbol
        p(valor_real)  # retorna int/float se o valor for numérico dentro do domínio
    """

    def __init__(self, dominio:list, imagem:list):
        super().__init__(dominio, imagem)

        # método de Lagrange
        soma = 0
        for i in range(len(self.dominio)):
            prod = 1
            for e in range(len(self.dominio)):
                if e != i:
                    prod *= (self.x - self.dominio[e]) / (self.dominio[i] - self.dominio[e])
            soma += self.imagem[i] * prod

        self.pol = simplify(soma)  # Polinômio interpolador simplificado

    def __repr__(self):
        return f'{self.pol}'

    def __call__(self, p:Union[int, float, Symbol]):
        if not isinstance(p, numbers.Real) and not isinstance(p, Symbol):
            raise ValueError('O ponto deve ser um número real ou uma variável')

        # Retorna a representação do polinômio no ponto p (variável) em LaTeX
        if isinstance(p, Symbol):
            return latex(self.pol.subs(self.x, p))

        # Previne extrapolação
        if p < min(self.dominio) or p > max(self.dominio):
            raise ValueError('Valores fora do intervalo do domínio não são bem aproximados')

        temp = self.pol.subs(self.x, p)
        if isinstance(temp, Number):
            if temp.is_integer:
                return int(temp)
            return float(temp)
        return None

    def __eq__(self, other):
        if isinstance(other, PoliInterp) or isinstance(other, PoliHermite):
            return self.pol == other.pol
        return False


class InterpLinear(Interpolacao):
    """
    Interpolação linear por segmentos (retas entre pares consecutivos de pontos).

    Calcula e armazena retas que ligam cada par consecutivo de pontos do domínio,
    representadas como expressões simbólicas simplificadas em um dicionário.

    Args:
        dominio (list): Lista de pontos do domínio (valores numéricos, distintos).
        imagem (list): Lista de valores da função nos pontos do domínio (numéricos).

    Raises:
        ValueError: Se o ponto passado para `__call__` não for um número real,
            ou se o ponto estiver fora do intervalo do domínio (extrapolação não permitida).

    Attributes:
        pares_ord (list[tuple]): Lista de pares ordenados (xi, yi) ordenados por xi.
        pol (dict): Dicionário mapeando o intervalo (xi, xi+1) para a expressão simbólica da reta entre esses pontos.

    Usage:
        l = InterpLinear(dominio, imagem)
        l(valor_real)  # retorna int/float se o valor estiver no domínio
    """

    def __init__(self, dominio:list, imagem:list):
        super().__init__(dominio, imagem)

        self.pares_ord = []
        for i, e in zip(dominio, imagem):
            self.pares_ord.append((i, e))
        self.pares_ord = sorted(self.pares_ord)

        # Criamos um dicionário para dividir as retas que ligam os pontos 2 a 2
        self.pol = {}

        # Calcula cada reta
        for i in range(len(self.pares_ord) - 1):
            reta = self.pares_ord[i][1] + (self.x - self.pares_ord[i][0]) * (
                (self.pares_ord[i + 1][1] - self.pares_ord[i][1]) / (self.pares_ord[i + 1][0] - self.pares_ord[i][0]))

            # Adiciona a reta simplificada no dicionário: (xi, xi+1): reta
            self.pol[(self.pares_ord[i][0], self.pares_ord[i + 1][0])] = simplify(reta)

    def __repr__(self):
        return f'{self.pol}'

    def _eval(self, pos:tuple, t:Union[int, float]):
        temp = self.pol[pos].subs(self.x, t)
        if isinstance(temp, Number):
            if temp.is_integer:
                return int(temp)
            return float(temp)
        return None

    def __call__(self, p:Union[int, float]):
        if not isinstance(p, numbers.Real):
            raise ValueError('O ponto deve ser um número real')

        temp = [i[0] for i in self.pares_ord]

        # Extrapolação
        if p>temp[-1] or p<temp[0]:
            raise ValueError('Valores fora do intervalo do domínio não são bem aproximados')

        for i in range(len(temp) - 1):
            if temp[i] <= p <= temp[i + 1]:
                return self._eval((temp[i], temp[i + 1]), p)
        return None

    def __eq__(self, other):
        if isinstance(other, InterpLinear):
            return self.pol == other.pol
        return False
    
    def grafico(self, precisao:int = 100) -> None:
        """
        Esboça o gráfico da classe InterpLinear
        
        Argumentos:
            precisao (int): número de pontos do polinomio a serem calculados. Padroniza em 100.
            
        Raises:
            TypeError: se precisão não for do tipo int
        """
        
        #Garante que precisao seja do tipo int
        if not isinstance(precisao, int):
            raise TypeError("precisao deve ser do tipo int")
        
        #Preparação
        x_simb = symbols('x')
        _, ax = subplots()
        ax.set_aspect("equal")
        precisao = precisao//(len(self.dominio) - 1)
        
        #Determinação dos limites do gráfico
        xmin, xmax, ymin, ymax = self.pares_ord[0][0], self.pares_ord[len(self.pares_ord) - 1][0], min(self.imagem), max(self.imagem)
        mini, maxi = min(xmin, ymin), max(xmax, ymax)
        ax.set_xlim(mini-1, maxi+1)
        ax.set_ylim(mini-1, maxi+1)
        
        #Conversão do polinomio e esboço das retas
        for i in range(1,len(self.pares_ord)):
            y_expr = self.pares_ord[i-1][1] + (
                x_simb - self.pares_ord[i-1][0]) * (
                    self.pares_ord[i][1] - self.pares_ord[i-1][1]) / (
                        self.pares_ord[i][0] - self.pares_ord[i-1][0])
            y_vals = linspace(self.pares_ord[i-1][0], self.pares_ord[i][0], precisao)
            y_lamb = lambdify(x_simb, y_expr, "numpy")
            y_func = y_lamb(y_vals)
            if isinstance(y_func, (int, float)):
                y_func = [y_func]*precisao
            ax.plot(y_vals, y_func)
        
        #Esboço dos pontos
        for i in range(len(self.dominio)):
                x_ponto, y_ponto = self.dominio[i], self.imagem[i]
                ax.plot(x_ponto, y_ponto, "o")
        
        #Exibição
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True)
        show()


class PoliHermite(Interpolacao):
    """
    Interpolador polinomial pelo método de Hermite (uso de valores e derivadas).

    Constrói o polinômio de Hermite a partir de `dominio`, `imagem` e `imagem_derivada`,
    usando funções auxiliares que computam os polinômios base de Hermite Hx_j e Hy_j.

    Args:
        dominio (list): Lista de pontos do domínio (valores numéricos, distintos).
        imagem (list): Lista de valores da função nos pontos do domínio (numéricos).
        imagem_derivada (list): Lista de valores das derivadas nos pontos do domínio (numéricos).

    Raises:
        ValueError: Se o ponto passado para `__call__` não for um número real nem um `sympy.Symbol`,
            ou se o ponto numérico estiver fora do intervalo [min(dominio), max(dominio)] (extrapolação não permitida).

    Attributes:
        coef_lagrange (dict): Dicionário em que cada entrada j contém (L_j(x), L_j'(x)) simplificados.
        pol (sympy.Expr): Polinômio de Hermite resultante e simplificado.

    Usage:
        h = PoliHermite(dominio, imagem, imagem_derivada)
        str(h)           # representação do polinômio
        h(sym)           # retorna LaTeX do polinômio se sym for sympy.Symbol
        h(valor_real)    # retorna int/float se o valor estiver no domínio
    """

    def __init__(self, dominio:list, imagem:list, imagem_derivada:list):
        super().__init__(dominio, imagem, imagem_derivada)

        # Dicionário com os coeficientes de Lagrange
        self.coef_lagrange = {}
        for j in range(len(imagem)):
            prod = 1
            for i in range(len(dominio)):
                if j != i:
                    prod *= (self.x - dominio[i]) / (dominio[j] - dominio[i])
            self.coef_lagrange[j] = (simplify(prod), simplify(prod.diff(self.x)))

        # Encontra o polinômio de hermite
        self.pol = self._hermite()

    def __repr__(self):
        return f'{self.pol}'

    def _hx_j(self, j:int):
        soma = (1-2*(self.x - self.dominio[j])*(self.coef_lagrange[j][1].subs(self.x, self.dominio[j])))*(self.coef_lagrange[j][0])**2
        return simplify(soma)

    def _hy_j(self, j:int):
        soma = (self.x-self.dominio[j])*(self.coef_lagrange[j][0])**2
        return simplify(soma)

    def _hermite(self):
        pol = 0
        for j in range(len(self.dominio)):
            pol += self.imagem[j]*self._hx_j(j) + self.imagem_derivada[j]*self._hy_j(j)
        return simplify(pol)

    def __call__(self, p:Union[int, float, Symbol]):
        if not isinstance(p, numbers.Real) and not isinstance(p, Symbol):
            raise ValueError('O ponto deve ser um número ou uma variável')

        # Retorna a representação do polinômio no ponto p (variável) em LaTeX
        if isinstance(p, Symbol):
            return latex(self.pol.subs(self.x, p))

        # Evita extrapolação
        if min(self.dominio) <= p <= max(self.dominio):
            temp = self.pol.subs(self.x, p)
            if isinstance(temp, Number):
                if temp.is_integer:
                    return int(temp)
                return float(temp)
            return None

        else:
            raise ValueError('Valores fora do intervalo do domínio não são bem aproximados')

    def __eq__(self, other):
        if isinstance(other, PoliInterp) or isinstance(other, PoliHermite):
            return self.pol == other.pol
        return False
