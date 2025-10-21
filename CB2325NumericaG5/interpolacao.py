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