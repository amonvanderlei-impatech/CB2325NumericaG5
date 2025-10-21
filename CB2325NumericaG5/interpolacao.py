from sympy import symbols, simplify

class PoliInterp:

    def __init__(self, dominio, imagem):
        self.x = symbols('x')
        # Garantimos que o domínio e a imagem possuem a mesma quantidade de pontos
        self.dominio = []
        self.imagem = []
        for i, e in zip(dominio, imagem):
            self.dominio.append(i)
            self.imagem.append(e)
        soma = 0
        for i in range(len(self.dominio)):
            prod = 1
            for e in range(len(self.imagem)):
                if e != i:
                    prod *= (self.x - self.dominio[e]) / (self.dominio[i] - self.dominio[e])
            soma += self.imagem[i] * prod
        self.pol = simplify(soma)

    def __repr__(self):
        return f'{self.pol}'

    def __call__(self, t):
        temp = self.pol.subs(self.x, t)
        if int(temp)-temp == 0:
            return temp
        else:
            return f'{temp:.4f}'


class IntLinear:

    def __init__(self, dominio, imagem):
        self.x = symbols('x')
        # Garantimos que o domínio e a imagem possuem a mesma quantidade de pontos
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
        return f'{self.pol}'

    def eval(self, pos, t):
        return self.pol[pos].subs(self.x, t)

    def __call__(self, t):
        # Lista dos x's
        temp = [i[0] for i in self.pares_ord]

        for i in range(len(temp) - 1):
            if temp[i] <= t <= temp[i + 1]:
                return self.eval((temp[i], temp[i + 1]), t)

        if t > temp[-1]:
            return self.eval((temp[-2], temp[-1]), t)

        else:
            return self.eval((temp[0], temp[1]), t)




