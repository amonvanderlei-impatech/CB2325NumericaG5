from sympy import symbols, simplify, Number




class PoliInterp:
    """Interpola os pontos dados utilizando o metodo de Lagrange e armazena o polinômio simplificado
    Args:
        dominio (list): Lista de pontos do domínio.
        imagem (list): Lista de pontos da imagem.

    Raises:
        ValueError: Se o domínio possuir pontos iguais.

    Returns:
        representação do polinômio interpolador,
        float: valor do polinômio num ponto específico."""

    def __init__(self, dominio, imagem):
        # Garantimos que o domínio e a imagem são listas de pontos
        if not isinstance(dominio, list) or not isinstance(imagem, list):
            raise ValueError('Argumentos inválidos')

        # Garantimos que o domínio e a imagem possuem a mesma quantidade de pontos
        if len(dominio) != len(imagem):
            raise ValueError('Dados inválidos')

        # Garantimos que o domínio não possui pontos repetidos
        if len(set(dominio)) != len(dominio) or len(dominio) < 2:
            raise ValueError('Domínio inválido')

        self.x = symbols('x')
        self.dominio = dominio
        self.imagem = imagem

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

    def __call__(self, t):
        # Previne extrapolação (valores fora do intervalo do domínio não são bem aproximados)
        if t < min(self.dominio) or t > max(self.dominio):
            return None

        temp = self.pol.subs(self.x, t)

        if isinstance(temp, Number):
            if temp.is_integer:
                return int(temp)
            return float(temp)

        return None








class InterpLinear:
    """Cria retas que interpolam pontos dois a dois
        e armazena elas em um dicionário interno dividindo
         cada reta por intervalo"""

    def __init__(self, dominio, imagem):
        # Garantimos que o domínio e a imagem são listas de pontos
        if not isinstance(dominio, list) or not isinstance(imagem, list):
            raise ValueError('Argumentos inválidos')

        # Garantimos que o domínio e a imagem possuem a mesma quantidade de pontos
        if len(dominio) != len(imagem):
            raise ValueError('Dados inválidos')

        # Garantimos que o domínio não possui pontos repetidos
        if len(set(dominio)) != len(dominio) or len(dominio) < 2:
            raise ValueError('Domínio inválido')

        self.x = symbols('x')

        self.pares_ord = []
        for i, e in zip(dominio, imagem):
            self.pares_ord.append((i, e))
        self.pares_ord = sorted(self.pares_ord)

        # Criamos um dicionário para dividir as retas que ligam os pontos 2 a 2
        self.pol = {}
        for i in range(len(self.pares_ord) - 1):
            reta = self.pares_ord[i][1] + (self.x - self.pares_ord[i][0]) * (
                    (self.pares_ord[i + 1][1] - self.pares_ord[i][1]) / (
                    self.pares_ord[i + 1][0] - self.pares_ord[i][0]))
            self.pol[(self.pares_ord[i][0], self.pares_ord[i + 1][0])] = simplify(reta)

    def __repr__(self):
        # Retorna um dicionário
        return f'{self.pol}'

    def eval(self, pos, t):
        temp = self.pol[pos].subs(self.x, t)
        if isinstance(temp, Number):
            if temp.is_integer:
                return int(temp)
            return float(temp)
        return None

    def __call__(self, t):
        # Lista dos x's
        temp = [i[0] for i in self.pares_ord]

        if t>temp[-1] or t<temp[0]:
            # Extrapolação
            return None

        for i in range(len(temp) - 1):
            if temp[i] <= t <= temp[i + 1]:
                return self.eval((temp[i], temp[i + 1]), t)
        return None








class PoliHermite:
    """Interpola utilizando o metodo de Hermite (interpola nos pontos dados e na primeira derivada)"""

    def __init__(self, dominio, imagem, imagem_derivada):
        if not isinstance(dominio, list) or not isinstance(imagem, list) or not isinstance(imagem_derivada, list):
            raise ValueError('Argumentos inválidos')

        if len(dominio) != len(imagem) or len(dominio) != len(imagem_derivada) or len(imagem) != len(imagem_derivada):
            raise ValueError('Dados inválidos')

        if len(set(dominio)) != len(dominio) or len(dominio) < 2:
            raise ValueError('Domínio inválido')

        self.x = symbols('x')
        self.dominio = dominio
        self.imagem = imagem
        self.imagem_derivada = imagem_derivada

        if len(set(self.dominio)) != len(self.dominio):
            raise ValueError('Dados inválidos')

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
        # Retorna a representação do polinômio simplificado
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

    def __call__(self, t):
        if min(self.dominio) <= t <= max(self.dominio):
            temp = self.pol.subs(self.x, t)
            if isinstance(temp, Number):
                if temp.is_integer:
                    return int(temp)
                return float(temp)
            return None
        else:
            raise ValueError('Extrapolação')