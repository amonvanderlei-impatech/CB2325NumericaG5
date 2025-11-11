import math
import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CB2325NumericaG5.erros import erro_absoluto, erro_relativo, soma_de_kahan

class TestErrosNumericos:

    # erro_absoluto()

    @pytest.mark.parametrize(
        "valor_real, valor_aprox, casas_decimais, esperado",
        [
            (10.0, 7.5, 6, 2.5),                        # Cálculo básico
            (0.0, 0.0, 6, 0.0),                         # Valores iguais
            (1, 0, 4, 1.0),                             # Diferença total
            (5.1234567, 5.1234561, 6, 0.000001),        # Teste de arredondamento e precisão
            (1, 1.000000000001, 12, 0.000000000001)     # Alta precisão
        ]
    )
    def test_erro_absoluto_valido(self, valor_real, valor_aprox, casas_decimais, esperado):
        """Testa os casos acima, e verifica se a função em si está retornando corretamente"""
        assert erro_absoluto(valor_real, valor_aprox, casas_decimais) == esperado

    @pytest.mark.parametrize("casas", [-1, 1.5, "a", None])
    # Número negativo, float, string e None
    def test_erro_absoluto_casas_invalidas(self, casas):
        """Verifica se o ValueError está sendo levantado"""
        with pytest.raises(ValueError, match="inteiro não-negativo"):
            erro_absoluto(1.0, 2.0, casas)  

    def test_erro_absoluto_tipo_errado(self):
        """Testa TypeError quando entradas que não são números são colocadas"""
        with pytest.raises(TypeError, match="devem ser números reais"):
            erro_absoluto("a", 1.0)  # type: ignore
        with pytest.raises(TypeError, match="devem ser números reais"):
            erro_absoluto(2.0, None) # type: ignore

    # erro_relativo()       

    @pytest.mark.parametrize(
        "valor_real, valor_aprox, casas_decimais, esperado",
        [
            (10.0, 7.5, 6, 0.25),               # Cálculo básico
            (-1.0, -1.0, 6, 0.0),                 # Valores iguais
            (1, 1.000000000001, 12, 0.000000000001),  # Alta precisão
            (100, 99.9, 3, 0.001),              # Teste de escala
            (100, 99.9, 1, 0.0),                # Teste de arredondamento
            (-10.0, -7.5, 6, 0.25),             # Números negativos
            (8.0, 10.0, 2, 0.25),               # Valor aproximado > valor real
        ]
    )


    def test_erro_relativo_valido(self, valor_real, valor_aprox, casas_decimais, esperado):
        """Testa os casos acima, e verifica se a função em si está retornando corretamente"""
        assert erro_relativo(valor_real, valor_aprox, casas_decimais) == esperado

    def test_erro_relativo_valor_real_zero(self):
        """Verifica se o ValueError está sendo lançado quando o valor_real é igual a 0"""
        with pytest.raises(ValueError, match="não pode ser zero"):
            erro_relativo(0, 1.0)  

    @pytest.mark.parametrize("casas", [-1, 1.5, "a", None]) 
    # Número negativo, float, string e None
    def test_erro_relativo_casas_invalidas(self, casas):
        """Verifica se o ValueError está sendo levantado"""
        with pytest.raises(ValueError, match="inteiro não-negativo"):
            erro_relativo(1.0, 2.0, casas)  

    def test_erro_relativo_tipo_errado(self):
        """Testa TypeError quando entradas que não são números são colocadas"""
        with pytest.raises(TypeError, match="devem ser números reais"):
            erro_relativo("a", 1.0)  # type: ignore
        with pytest.raises(TypeError, match="devem ser números reais"):
            erro_relativo(2.0, None) # type: ignore

    # soma_de_kahan()

    @pytest.mark.parametrize(
        "lista_de_valores , esperado",
        [
            ([1.0,2.0,3.0,4.0],10.0),                               # Cálculo básico
            ([1.0,"b",9.0,"a"],10.0),                               # Strings misturadas
            (["a",None, False],0.0),                                # Vários tipos diferentes
            ([],0.0),                                               # Lista vazia
            ([2.5,-1.1,0.000000001,10000000],10000001.400000001),   # Alta precisão
        ]
    )

    def test_soma_de_kahan_valido(self, lista_de_valores, esperado):
        """Testa os casos acima, e verifica se a função em si está retornando corretamente"""
        assert soma_de_kahan(lista_de_valores) == esperado

    @pytest.mark.parametrize("lista_de_valores", [1, -5, 2.5, 'a', None, True])
    # Inteiro, número negativo, float, string, None e booleana
    def test_soma_de_kahan_tipo_errado(self, lista_de_valores):
        """Testa o TypeError quando a entrada não é uma lista"""
        with pytest.raises(TypeError, match="deve ser uma lista"):
            soma_de_kahan(lista_de_valores)
