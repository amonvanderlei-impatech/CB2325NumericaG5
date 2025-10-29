from sympy import symbols, simplify, Number, latex, Symbol
from typing import Union


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
        if imagem_derivada is None:
            # Garantimos que o domínio e a imagem são listas de pontos
            if not isinstance(dominio, list) or not isinstance(imagem, list):
                raise TypeError('Argumentos inválidos')

            # Garantimos que o domínio e a imagem possuem a mesma quantidade de pontos
            if len(dominio) != len(imagem):
                raise ValueError('Dados inválidos')

        else:
            # Garantimos que o domínio, a imagem e a imagem_derivada são listas de pontos
            if not isinstance(dominio, list) or not isinstance(imagem, list) or not isinstance(imagem_derivada, list):
                raise TypeError('Argumentos inválidos')

            # Garantimos que o domínio, a imagem e a imagem_derivada possuem a mesma quantidade de pontos
            if len(dominio) != len(imagem) or len(dominio) != len(imagem_derivada) or len(imagem) != len(
                    imagem_derivada):
                raise ValueError('Dados inválidos')

            self.imagem_derivada = imagem_derivada

        # Garantimos que o domínio não possui pontos repetidos
        if len(set(dominio)) != len(dominio) or len(dominio) < 2:
            raise ValueError('Domínio inválido')

        self.x = symbols('x')
        self.dominio = dominio
        self.imagem = imagem


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
        # A representação é uma str do polinômio
        return f'{self.pol}'

    def __call__(self, t:Union[int, float, Symbol]):
        if not isinstance(t, Union[int, float, Symbol]):
            raise ValueError('O ponto deve ser um número ou uma variável')

        # Retorna a representação do polinômio no ponto x em LaTeX
        if isinstance(t, Symbol):
            return latex(self.pol)

        # Previne extrapolação
        if t < min(self.dominio) or t > max(self.dominio):
            raise ValueError('Valores fora do intervalo do domínio não são bem aproximados')

        temp = self.pol.subs(self.x, t)
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
                    (self.pares_ord[i + 1][1] - self.pares_ord[i][1]) / (
                    self.pares_ord[i + 1][0] - self.pares_ord[i][0]))

            # Adiciona a reta simplificada no dicionário: (xi, xi+1): reta
            self.pol[(self.pares_ord[i][0], self.pares_ord[i + 1][0])] = simplify(reta)

    def __repr__(self):
        # Retorna um dicionário
        return f'{self.pol}'

    def _eval(self, pos:tuple, t:Union[int, float]):
        temp = self.pol[pos].subs(self.x, t)
        if isinstance(temp, Number):
            if temp.is_integer:
                return int(temp)
            return float(temp)
        return None

    def __call__(self, t:Union[int, float]):
        if not isinstance(t, Union[int, float]):
            raise ValueError('O ponto deve ser do tipo int ou float')

        temp = [i[0] for i in self.pares_ord]

        # Extrapolação
        if t>temp[-1] or t<temp[0]:
            raise ValueError('Valores fora do intervalo do domínio não são bem aproximados')

        for i in range(len(temp) - 1):
            if temp[i] <= t <= temp[i + 1]:
                return self._eval((temp[i], temp[i + 1]), t)
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
        # Retorna a representação do polinômio
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

    def __call__(self, t:Union[int, float, Symbol]):
        if not isinstance(t, Union[int, float, Symbol]):
            raise ValueError('O ponto deve ser um número ou uma variável')

        # Retorna a representação do polinômio no ponto x em latex
        if isinstance(t, Symbol):
            return latex(self.pol)

        # Evita extrapolação
        if min(self.dominio) <= t <= max(self.dominio):
            temp = self.pol.subs(self.x, t)
            if isinstance(temp, Number):
                if temp.is_integer:
                    return int(temp)
                return float(temp)
            return None
        else:
            raise ValueError('Valores fora do intervalo do domínio não são bem aproximados')
