import sympy as sp
from typing import Callable
import numpy as np
import matplotlib.pyplot as plt
import math
import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CB2325NumericaG5.raizes_aproximacao import bissecao, secante

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

    def teste_raizes_invalidas(self, f, a, b):
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
            (lambda x: abs(x) - x**2 + (abs(x)**1.5) - math.sin(x)/2, -2.5, 3),
        ],
    )

    def test_plot(self, f, a, b):
        """Testa se o gráfico roda sem retornar erros."""
        bissecao(f, a, b, plot=True)