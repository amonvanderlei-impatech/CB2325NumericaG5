import math
import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CB2325NumericaG5.erros import erro_absoluto

class TestErrosNumericos:
    @pytest.mark.parametrize(
        "valor_real, valor_aprox, casas_decimais, esperado",
        [
            (10.0, 7.5, 6, 2.5),
            (0.0, 0.0, 6, 0.0),
            (1, 0, 4, 1.0),
            (5.1234567, 5.1234561, 6, round(abs(5.1234567 - 5.1234561), 6)),
            (1,1.000000000001,12,round(abs(1-1.000000000001), 12))
        ]
    )
    def test_erro_absoluto_valido(self, valor_real, valor_aprox, casas_decimais, esperado):
        """Testa os casos acima, e verifica se a função em si ta retornando corretamente"""
        assert erro_absoluto(valor_real, valor_aprox, casas_decimais) == esperado

    @pytest.mark.parametrize("casas", [-1, 1.5, "a", None])
    def test_erro_absoluto_casas_invalidas(self, casas):
        """Verifica se o ValueError está sendo levantado"""
        with pytest.raises(ValueError, match="inteiro não-negativo"):
            erro_absoluto(1.0, 2.0, casas)  

    def test_erro_absoluto_tipo_errado(self):
        """Testa TypeError quando entradas que não são números são colocadas"""
        with pytest.raises(TypeError, match="devem ser números reais"):
            erro_absoluto("a", 1.0) 
        with pytest.raises(TypeError, match="devem ser números reais"):
            erro_absoluto(2.0, None) 
