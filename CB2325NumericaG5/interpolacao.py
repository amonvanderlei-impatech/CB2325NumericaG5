from sympy import symbols, simplify, lambdify, Number, latex, Symbol
from numpy import linspace
from matplotlib.pyplot import show, subplots
from typing import Union
import numbers


class Interpolacao:
    """
        Classe abstrata que verifica a entrada do domínio, imagem e imagem_derivada.

        Args:
            dominio (list): Lista de pontos do domínio
            imagem (list): Lista de pontos da imagem
            imagem_derivada (list): Lista de pontos da imagem da derivada. Padroniza em None

        Raises:
            TypeError: se o 'dominio' e a 'imagem' não forem listas
            ValueError: se o tamanho do 'dominio' for diferente do tamanho da 'imagem'
            TypeError: se o 'dominio', a 'imagem' e a 'imagem_derivada' não forem listas
            ValueError: se o tamanho do 'dominio', da 'imagem' ou da 'imagem_derivada' forem diferentes
            ValueError: se o 'dominio' possuir valores repetidos ou quantidade insuficiente de pontos
            NotImplementedError: se a __repr__ ou o __call__ não forem implementados
        """

    def __init__(self, dominio:list, imagem:list, imagem_derivada:list = None):
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
                raise TypeError('`dominio` deve ser uma lista de números')

        # Garantimos que a imagem é uma lista de números
        for i in imagem:
            if not isinstance(i, numbers.Real):
                raise TypeError('`imagem` deve ser uma lista de números')

        # Cria as variáveis internas
        self.x = symbols('x')
        self.dominio = dominio
        self.imagem = imagem

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
                    raise TypeError('`imagem_derivada` deve ser uma lista de números')

            # Cria uma variável interna
            self.imagem_derivada = imagem_derivada

    def __repr__(self):
        raise NotImplementedError

    def __call__(self, t):
        raise NotImplementedError


class PoliInterp(Interpolacao):
    """
        Interpola os pontos dados utilizando o metodo de Lagrange e armazena o polinômio simplificado
    Args:
        dominio (list): Lista de pontos do domínio
        imagem (list): Lista de pontos da imagem

    Raises:
        ValueError: se o ponto não for do tipo int, float ou Symbol
        ValueError: se o ponto estiver fora do intervalo de interpolação, evitando extrapolação

    Returns:
        str: representação do polinômio interpolador
        str: representação do polinômio interpolador em LaTeX
        int: valor do polinômio num ponto específico, se o valor for inteiro
        float: valor do polinômio num ponto específico, se o valor for um número de ponto flutuante
    """

    def __init__(self, dominio, imagem):
        super().__init__(dominio, imagem)

        # Metodo de Lagrange
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


class InterpLinear(Interpolacao):
    """
        Cria retas que interpolam pontos dois a dois e armazena elas num dicionário interno dividindo cada reta por intervalo.

        Args:
            dominio (list): Lista de pontos do domínio
            imagem (list): Lista de pontos da imagem

        Raises:
            ValueError: se o ponto não for do tipo int ou float
            ValueError: se o ponto estiver fora do intervalo de interpolação, evitando extrapolação

        Returns:
            dict: representação das retas interpoladoras por partes
            int: valor da reta num ponto específico, se o valor for inteiro
            float: valor da reta num ponto específico, se o valor for um número de ponto flutuante

    """

    def __init__(self, dominio, imagem):
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


class PoliHermite(Interpolacao):
    """
        Interpola utilizando o metodo de Hermite e armazena o polinomio simplificado

        Args:
            dominio (list): Lista de pontos do domínio
            imagem (list): Lista de pontos da imagem
            imagem_derivada (list): Lista de pontos da imagem da derivada

        Raises:
            ValueError: se o ponto não for do tipo int, float ou Symbol
            ValueError: se o ponto estiver fora do intervalo de interpolação, evitando extrapolação

        Returns:
            str: representação do polinômio interpolador
            str: primeiro coeficiente de Hermite
            str: segundo coeficiente de Hermite
            str: polinômio de Hermite
            str: representação do polinômio interpolador em LaTeX
            int: valor do polinômio num ponto específico, se o valor for inteiro
            float: valor do polinômio num ponto específico, se o valor for um número de ponto flutuante
        """

    def __init__(self, dominio, imagem, imagem_derivada):
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

    def _hx_j(self, j):
        soma = (1-2*(self.x - self.dominio[j])*(self.coef_lagrange[j][1].subs(self.x, self.dominio[j])))*(self.coef_lagrange[j][0])**2
        return simplify(soma)

    def _hy_j(self, j):
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


def grafico(polinomio, precisao = 100):
    """Esboça o gráfico das subclasses da classe Interpolacao

    Argumentos:
        polinomio (PoliInterp, InterpLinear, PoliHermite): Polinomio a ser esboçado
        precisao (int): número de pontos do polinomio a serem calculados. Padroniza em 100.
    """
    
    x_simb, t = symbols('x t')
    
    x_expr = t
    x_lamb = lambdify(t, x_expr, "numpy")
    
    f, ax = subplots()
    ax.set_aspect("equal")
    
    if type(polinomio) == InterpLinear:
        precisao = precisao//len(polinomio.dominio)
        
        xmin, xmax = polinomio.pares_ord[0][0], polinomio.pares_ord[len(polinomio.pares_ord) - 1][0]
        ymin, ymax = polinomio.imagem[0], polinomio.imagem[0]
        
        for y in polinomio.imagem:
            if y < ymin:
                ymin = y
            if y > ymax:
                ymax = y
                
        mini, maxi = min(xmin, ymin), max(xmax, ymax)
        
        ax.set_xlim(mini-1, maxi+1)
        ax.set_ylim(mini-1, maxi+1)
        
        for i in range(1,len(polinomio.pares_ord)):
            y_expr = polinomio.pares_ord[i-1][1] + (
                x_simb - polinomio.pares_ord[i-1][0]) * (
                    polinomio.pares_ord[i][1] - polinomio.pares_ord[i-1][1]) / (
                        polinomio.pares_ord[i][0] - polinomio.pares_ord[i-1][0])
            y_lamb = lambdify(x_simb, y_expr, "numpy")
            
            f_vals = linspace(polinomio.pares_ord[i-1][0], polinomio.pares_ord[i][0], precisao)
            x_func = x_lamb(f_vals)
            y_func = y_lamb(f_vals)
            
            ax.plot(x_func, y_func)
             
    else:
        y_expr = polinomio.pol
        y_lamb = lambdify(x_simb, y_expr, "numpy")
        
        xmin, xmax, ymin, ymax = polinomio.dominio[0], polinomio.dominio[0], polinomio.imagem[0], polinomio.imagem[0]
        for x in polinomio.dominio:
            if x < xmin:
                xmin = x
            if x > xmax:
                xmax = x
        for y in polinomio.imagem:
            if y < ymin:
                ymin = y
            if y > ymax:
                ymax = y
        
        mini, maxi = min(xmin, ymin), max(xmax, ymax)
        
        ax.set_xlim(mini-1, maxi+1)
        ax.set_ylim(mini-1, maxi+1)
        
        f_vals = linspace(xmin, xmax, precisao)
        x_func = x_lamb(f_vals)
        y_func = y_lamb(f_vals)
        
        ax.plot(x_func, y_func)
    
    for i in range(len(polinomio.dominio)):
            x_ponto, y_ponto = polinomio.dominio[i], polinomio.imagem[i]
            ax.plot(x_ponto, y_ponto, "o")
        
    show()

metodo1 = InterpLinear([-2, -1, 0, 1, 2],[0, -1, 2, -3, 4])
metodo2 = PoliInterp([-2, -1, 0, 1, 2],[0, -1, 2, -3, 4])
grafico(metodo1)
grafico(metodo2)