from sympy import Symbol
import math
import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CB2325NumericaG5.aproximacao import (
    coeficiente_determinacao,
    aproximacao_polinomial,
    txt_aproximacao_polinomial
)

class TestCoeficienteDeterminacao:
    @pytest.mark.parametrize("y_real, y_ajustado, r2_esperado", [
        # Teste 1: y_real é igual ao y_ajustado
        ([1, 2, 3, 4], [1, 2, 3, 4], 1.0),
        # Teste 2: y_ajustado é a média dos valores reais
        ([1, 2, 3, 4], [2.5, 2.5, 2.5, 2.5], 0.0),
        
        # Teste 3: variação total nula
        ([5, 5, 5], [5, 5, 5], 0.0),
        
        # Teste 4: caso normal
        ([1, 2, 3], [1.1, 1.9, 3.0], 0.99)
    ])
    def test_r2_casos_validos(self, y_real, y_ajustado, r2_esperado):
        r2_calculado = coeficiente_determinacao(y_real, y_ajustado)
        assert r2_calculado == pytest.approx(r2_esperado) # usado pra lidar com erros de ponto flutuante
        
    def test_r2_tamanho_invalido(self):
        """Testa se listas de tamanhos diferentes levantam ValueError."""
        y_real = [1,2,3]
        y_ajustado = [1,2]
        with pytest.raises(ValueError, match="devem ter o mesmo tamanho"):
            coeficiente_determinacao(y_real, y_ajustado)