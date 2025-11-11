import math
import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CB2325NumericaG5.raizes import bissecao, secante

class Testbissecao:
    @pytest.mark.parametrize(
        "f, a, b, esperado",
        [
            (lambda x: x - x ** 3 / 6 + x ** 5 / 120, -math.pi, math.pi, 0.0),
            (lambda x: 1 - x ** 2 / 2 + x ** 4 / 24 - x**6 / 720, 0.0, math.pi, math.pi / 2),
            (lambda x: x ** 2 - 1, 0.0, 2.0, 1.0),
            (lambda x: - 2*x + 1, 0.0, 1, 0.5),
            (lambda x: math.sin(x) - x**2, 1, 0.6, 0.876),
            (lambda x: abs(x) - 1, 0, 2, 1)

        ],
    )

    def test_raizes_validas(self, f, a, b, esperado):
        """Testa se as raízes são calculadas corretamente."""
        raiz_bissecao = bissecao(f, a, b, plot=False)

        assert raiz_bissecao == pytest.approx(esperado, rel=1e-3)


    @pytest.mark.parametrize(
        "f, a, b",
        [
            (lambda x: x**2 + 1, -1, 1),
            (lambda x: math.cos(x), 0, 2*math.pi),
            (lambda x: x ** 2 - 1, 0, 0),
            (lambda x: abs(x), -1, 1),

        ],
    )

    def teste_parametros_invalidas(self, f, a, b):
        """ Testa casos onde os valores de f(a) * f(b) > 0 (inclusive para pontos repetidos)"""
        with pytest.raises(ValueError):
            bissecao(f, a, b, plot=False)


    @pytest.mark.parametrize(
        "f, a, b",
        [
            ('função', 0, 1),
            (lambda x: x**2 - 1, '0', 1.5),
            (lambda x: x ** 2 - 1, 0, '1.5'),
            (lambda x: x**2 - 1, 0, (1, 2, 3)),
            (lambda x: x ** 2 - 1, (1, 2, 3), 2),
            (lambda x: x ** 2 - 1, 0, [1, 2, 3]),
            (lambda x: x ** 2 - 1, [1, 2, 3], 2),

        ],
    )

    def test_invalid_tipo(self, f, a, b):
        """Testa se entradas com tipos errados geram TypeError."""
        with pytest.raises(TypeError):
            bissecao(f, a, b, plot=False)


    @pytest.mark.parametrize(
        "f, a, b",
        [
            (lambda x: x, -1, 1e300),
            (lambda x: x, -1e300, 1e300),

        ],
    )

    def test_float_extremos(self, f, a, b):
        """Testa bicessao com valores muito grandes."""
        assert bissecao(f, a, b, plot=False) == pytest.approx(0, abs=1e-6)


    @pytest.mark.parametrize(
        "f, a, b",
        [
            (lambda x: x, -1e-300, 1),
            (lambda x: x, -1e-300, 1e-300),

        ],
    )

    def test_valores_proximos(self, f, a, b):
        """Testa bicessao com valores muito pequenos."""
        assert bissecao(f, a, b, plot=False) == pytest.approx(0, abs=1e-6)


    @pytest.mark.parametrize(
        "f, a, b",
        [
            (lambda x: x, math.nan, 1),
            (lambda x: x, -math.inf, math.inf),

        ],
    )

    def test_nan_e_inf(self, f, a, b):
        """Testa NaN e infinitos."""
        with pytest.raises(ValueError):
            bissecao(f, a, b, plot=False)


    @pytest.mark.parametrize(
        "f, a, b, aceitaveis",
        [
            (lambda x: math.sin(x), -4, 4, [-math.pi, math.pi, 0]),

        ],
    )

    def test_multiplas_raizes(self, f, a, b, aceitaveis):
        """Testa a bissecao com mais de 1 raiz no intervalo"""
        r = bissecao(f, a, b, plot=False) == pytest.approx(1, abs=1e-6)
        assert any(abs(r - raiz) <= 1e-6 for raiz in aceitaveis), f"raiz {r} não está nas aceitáveis {aceitaveis}"


    @pytest.mark.parametrize(
        "f, a, b",
        [
            (lambda x: math.tan(x), -math.pi/2, math.pi/2),
        ],
    )

    def test_descontinuidades(self, f, a, b):
        """Testa funções não contínuas"""
        with pytest.raises(ValueError):
            bissecao(f, a, b, plot=False)

        # Observação: Não é verificado se isinf(math.tan(+-pi/2))


    @pytest.mark.parametrize(
        "f, a, b",
        [
            (lambda x: abs(x) - x**2 + (abs(x)**1.5) - math.sin(x)/2 + 2, -3, 4),
        ],
    )

    def test_plot(self, f, a, b):
        """Testa se o gráfico roda sem retornar erros."""
        bissecao(f, a, b, plot=True)


class Testsecante:
    @pytest.mark.parametrize(
        "f, a, b, esperado",
        [
            (lambda x: x - x ** 3 / 6 + x ** 5 / 120, -math.pi, math.pi, 0.0),
            (lambda x: 1 - x ** 2 / 2 + x ** 4 / 24 - x**6 / 720, 0.0, math.pi, math.pi / 2),
            (lambda x: x ** 2 - 1, 0.0, 2.0, 1.0),
            (lambda x: - 2*x + 1, 0.0, 1, 0.5),
            (lambda x: math.sin(x) - x**2, 1, 0.6, 0.876),
            (lambda x: abs(x) - 1, 0, 2, 1)

        ],
    )

    def test_raizes_validas(self, f, a, b, esperado):
        """Testa se as raízes são calculadas corretamente."""
        raiz_secante = secante(f, a, b, plot=False)

        assert raiz_secante == pytest.approx(esperado, rel=1e-3)


    @pytest.mark.parametrize(
        "f, a, b",
        [
            (lambda x: x**2 - 1, -2, 2),
            (lambda x: math.cos(x), 0, 2*math.pi),
            (lambda x: abs(x), -1, 1),

        ],
    )

    def teste_parametros_invalidas(self, f, a, b):
        """ Testa casos onde os valores de f(a) = f(b)"""
        with pytest.raises(ZeroDivisionError):
            secante(f, a, b, plot=False)


    @pytest.mark.parametrize(
        "f, a, b",
        [
            ('função', 0, 1),
            (lambda x: x**2 - 1, '0', 1.5),
            (lambda x: x ** 2 - 1, 0, '1.5'),
            (lambda x: x**2 - 1, 0, (1, 2, 3)),
            (lambda x: x ** 2 - 1, (1, 2, 3), 2),
            (lambda x: x ** 2 - 1, 0, [1, 2, 3]),
            (lambda x: x ** 2 - 1, [1, 2, 3], 2),

        ],
    )

    def test_invalid_tipo(self, f, a, b):
        """Testa se entradas com tipos errados geram TypeError."""
        with pytest.raises(TypeError):
            secante(f, a, b, plot=False)


    @pytest.mark.parametrize(
        "f, a, b",
        [
            (lambda x: x, -1, 1e300),
            (lambda x: x, -1e300, 1e300),

        ],
    )

    def test_float_extremos(self, f, a, b):
        """Testa secante com valores muito grandes."""
        assert bissecao(f, a, b, plot=False) == pytest.approx(0, abs=1e-6)


    @pytest.mark.parametrize(
        "f, a, b",
        [
            (lambda x: x, -1e-300, 1e-300),

        ],
    )

    def test_valores_proximos(self, f, a, b):
        """Testa secante com valores muito pequenos."""
        with pytest.raises(ZeroDivisionError):
            secante(f, a, b, plot=False)

    @pytest.mark.parametrize(
        "f, a, b",
        [
            (lambda x: x, math.nan, 1),
            (lambda x: x, -math.inf, math.inf),

        ],
    )

    def test_nan_e_inf(self, f, a, b):
        """Testa NaN e infinitos."""
        with pytest.raises(ValueError):
            secante(f, a, b, plot=False)


    @pytest.mark.parametrize(
        "f, a, b, aceitaveis",
        [
            (lambda x: math.sin(x), -4, 4, [-math.pi, math.pi, 0]),

        ],
    )

    def test_multiplas_raizes(self, f, a, b, aceitaveis):
        """Testa a secante com mais de 1 raiz no intervalo"""
        r = secante(f, a, b, plot=False) == pytest.approx(1, abs=1e-6)
        assert any(abs(r - raiz) <= 1e-6 for raiz in aceitaveis), f"raiz {r} não está nas aceitáveis {aceitaveis}"


    @pytest.mark.parametrize(
        "f, a, b",
        [
            (lambda x: math.tan(x), -math.pi/2, math.pi/2),
        ],
    )

    def test_descontinuidades(self, f, a, b):
        """Testa funções não contínuas"""
        with pytest.raises(ValueError):
            secante(f, a, b, plot=False)

        # Observação: Não é verificado se isinf(math.tan(+-pi/2))

    @pytest.mark.parametrize(
        "f, a, b",
        [
            (lambda x: x**2 + 1, -0.5, 2),
            (lambda x: abs(x) + 1, -0.5, 2),
        ],
    )

    def test_raizes_complexas(self, f, a, b):
        """Testa o comportamento quando as raízes são complexas."""
        with pytest.raises(RuntimeError):
            secante(f, a, b, plot=False)

    @pytest.mark.parametrize(
        "f, a, b",
        [
            (lambda x: abs(x) - x**2, -0.5, 1.5),
        ],
    )

    def test_plot(self, f, a, b):
        """Testa se o gráfico roda sem retornar erros."""
        secante(f, a, b, plot=True)


import CB2325NumericaG5.raizes as rz

# Conjunto de funções triviais.
pol1 = lambda x: (-2 * x) + 5
pol2 = lambda x: (-x ** 2) + (8 * x) - 16
polfract = lambda x: (x ** 2 - 1) / (x - 1)
exponencial = lambda x: (2.71828) ** x - 1

# Conjunto de funções triviais. Valores muito pequenos.
polpeq1 = lambda x: ((-2e-8) * x) + 5 * (1e-8)
polpeq2 = lambda x: ((-1e-8) * (x ** 2)) + ((8e-8) * x) - 16 * (1e-8)
polfractpeq = lambda x: ((x ** 2 - 1) / (x - 1)) * 1e-8
exponencialpeq = lambda x: ((2.71828) ** x - 1) * 1e-8

# Conjunto de funções triviais. Valores muito pequenos.
polgran1 = lambda x: ((-2e8) * x) + 5 * (1e8)
polgran2 = lambda x: (-1e8) * (x ** 2) + (8e8) * x - 16 * (1e8)
polfractgra = lambda x: ((x ** 2 - 1) / (x - 1)) * 1e8
exponencialgran = lambda x: ((2.71828) ** x - 1) * 1e8

# Conjunto de funções não triviais.
polsemraiz = lambda x: x ** 2 + 1
pol_duas_raizes = lambda x: x ** 2 - 1
exponencial_sem_raiz = lambda x: (2.71828) ** x
seno = lambda x: x - (x ** 3) / 6 + (x ** 5) / 120 - (x ** 7) / 5040 + (x ** 9) / 362880 - (x ** 11) / 39916800
cosseno = lambda x: 1 - (x ** 2) / 2 + (x ** 4) / 24 - (x ** 6) / 720 + (x ** 8) / 40320 - (x ** 10) / 3628800


def proximo(a, b, tol):
    if abs(a) == 1 or abs(b) == 1:  # A função duas raizes admite duas raizes.
        if abs(abs(a) - abs(b)) < tol:
            return True

    if abs(a - b) < tol:
        return True

    if b == 1.57079632679489661923123169163:  # Identifica que a função é a cosseno.
        if abs(abs(a) - abs(b)) < tol:  # A função cosseno admite os dois sinais.
            return True

        for i in range(10):  # A função cosseno adimite mais de uma raiz também.
            if abs(abs(a) - (abs(b + i * 3.14))) < 1:
                return True

    for i in range(30):
        if (abs(a) - 3.14 * i) < .01:  # A função seno aparece com pi. E admite algumas raizes.
            if b == 0:
                return True

    else:
        return False


@pytest.mark.parametrize("pontoi", [
    -1000000,
    -1000,
    -100.0001,
    -1,
    -.001,
    0,
    1.001,
    1,
    100.0001,
    1000,
    1000000
])
@pytest.mark.parametrize("funcao, raiz_esperada", [
    (pol1, 2.5),
    (pol2, 4.0),
    (polfract, -1),
    (exponencial, 0),
    (polpeq1, 2.5),
    (polpeq2, 4),
    (polfractpeq, -1),
    (exponencialpeq, 0),
    (polgran1, 2.5),
    (polgran2, 4.0),
    (polfractgra, -1),
    (exponencialgran, 0),
    (pol_duas_raizes, 1),
    (seno, 0),
    (cosseno, 1.57079632679489661923123169163)
])
def test_newton_raizes(funcao, raiz_esperada, pontoi):
    try:
        resultado = rz.newton(funcao, pontoi, plot=False)
        assert proximo(resultado, raiz_esperada, 1e-3), \
            f"Esperado {raiz_esperada}, obtido {resultado}"

    except Exception as e:
        # Se for erro de derivada nula → skip (condição esperada)
        if "derivada" in str(e).lower() or "zero" in str(e).lower():
            pytest.skip(f"Derivada nula em ponto inicial {pontoi}, teste ignorado: {e}")
        else:
            pytest.fail(f"Falhou ({funcao(0)}) para ponto inicial {pontoi}: {e}")


# Funções bem simples, apenas para testar a função auxiliar.
f1 = lambda x: 2 * x - 10
f2 = lambda x: x ** 3
f3 = lambda x: (x - 1) ** 5


def logo_ali(a, b, tolerancia):  # Função para comparar os resultados.
    if type(a) == list:  # Pois o método da bisseção retorna uma lista.
        if abs(a[0] - b) < tolerancia and abs(a[1] - b) < tolerancia:
            return True
        else:
            return False

    else:
        if abs(a - b) < tolerancia:
            return True
        else:
            return False


@pytest.mark.parametrize("funcao, raiz", [
    (f1, 5),
    (f2, 0),
    (f3, 1)
])
@pytest.mark.parametrize("nome", [
    "bissecao",
    "secante",
    "newton"
])
def test_raizes(funcao, raiz, nome):
    resultado = rz.raiz(
        funcao,
        -10, 10, 10,
        method=nome,
        plot=False)
    assert logo_ali(resultado, raiz, 1e-3), \
        f"Esperado {raiz}, obtido {resultado}"


def test_graficos():
    r1 = rz.raiz(
        f1,
        -10, 10, 10,
        method="newton",
    )
    assert logo_ali(r1, 5, 1e-3), \
        f"Esperado {5}, obtido {r1}"

    r2 = rz.raiz(
        f1,
        -10, 10, 10,
        method="bissecao",
    )
    assert logo_ali(r2, 5, 1e-3), \
        f"Esperado {5}, obtido {r2}"

    r3 = rz.raiz(
        f1,
        -10, 10, 10,
        method="secante",
    )
    assert logo_ali(r3, 5, 1e-3), \
        f"Esperado {5}, obtido {r3}"
