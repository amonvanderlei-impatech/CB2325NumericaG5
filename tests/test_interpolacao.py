from sympy import Symbol
import math
import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CB2325NumericaG5.interpolacao import InterpLinear

class TestInterpLinear:
    @pytest.mark.parametrize(
        "dominio, imagem",
        [
            ([0, 1, 2, 3, 4], [0, 1, 4, 9, 16]),
            ([0, 1, 2, 3, 10], [0, 1, 4, 9, 16])
        ]
    )
    def test_interp_linear_valida(self, dominio, imagem):
        """Testa casos válidos de interpolação."""
        interp = InterpLinear(dominio, imagem)

        assert interp(dominio[0]) == imagem[0]

        with pytest.raises(ValueError, match="fora do intervalo do domínio"):
            interp(max(dominio) + 1e5)

    @pytest.mark.parametrize(
        "dominio, imagem",
        [
            ([], [0, 1, 4, 9, 16]),
            ([0, 1, 2, 3, 10], []),
            ([], []),
            ([0, 1, 2], [1, 2])
        ]
    )
    def test_interp_linear_invalida_valor(self, dominio, imagem):
        """Testa se entradas com tamanhos inconsistentes geram ValueError."""
        with pytest.raises(ValueError):
            InterpLinear(dominio, imagem)

    @pytest.mark.parametrize(
        "dominio, imagem",
        [
            ("a", [1]),
            ([1], "a"),
            (1, 1)
        ]
    )
    def test_interp_linear_invalida_tipo(self, dominio, imagem):
        """Testa se entradas com tipos errados geram TypeError."""
        with pytest.raises(TypeError):
            InterpLinear(dominio, imagem)

    def test_nao_ordenado(self):
        """Testa se as entradas não ordenadas serão ordenadas."""
        dominio = [3, 1, 2]
        imagem = [9, 1, 4]
        interp = InterpLinear(dominio, imagem)
        
        assert list(interp.pares_ord) == [(1, 1), (2, 4), (3, 9)]
        assert interp(1.5) == 2.5

    def test_pontos_repetidos(self):
        """Testa pontos repetidos."""
        dominio = [0, 1, 1, 2]
        imagem = [0, 1, 1, 4]
        
        with pytest.raises(ValueError, match="não pode ter valores repetidos"):
            InterpLinear(dominio, imagem)

    def test_limites_dominio(self):
        """Testa para os pontos limites do domínio."""
        dominio = [0, 2, 4]
        imagem = [0, 4, 8]
        interp = InterpLinear(dominio, imagem)
        
        assert interp(0) == 0
        assert interp(4) == 8

    def test_interpolacao_linear(self):
        """Testa se a interpolação está sendo calculada corretamente."""
        dominio = [0, 2, 4]
        imagem = [0, 4, 8]
        interp = InterpLinear(dominio, imagem)
        
        assert interp(1) == 2
        assert interp(3) == 6

    def test_call_tipo_errado(self):
        """Testa se uma validação de entrada foi implementada."""
        dominio = [0, 1]
        imagem = [0, 1]
        interp = InterpLinear(dominio, imagem)
        
        with pytest.raises(ValueError, match="número real"):
            interp("a") # type: ignore

    def test_extrapolacao(self):
        """Testa extrapolação acima e abaixo do domínio."""
        dominio = [0, 1, 2]
        imagem = [0, 1, 4]
        interp = InterpLinear(dominio, imagem)
        
        with pytest.raises(ValueError):
            interp(-1)
        with pytest.raises(ValueError):
            interp(3)
        with pytest.raises(ValueError):
            interp(3.000000000001)
        with pytest.raises(ValueError):
            interp(-1e-12)

    def test_dominio_dois_pontos(self):
        """Testa em um domínio mínimo de dois pontos."""
        dominio = [0, 10]
        imagem = [0, 100]
        interp = InterpLinear(dominio, imagem)

        assert interp(5) == 50

    def test_simbolo_no_call(self):
        """Testa passar um símbolo para o interpolador."""
        dominio = [0, 1]
        imagem = [0, 1]
        interp = InterpLinear(dominio, imagem)

        with pytest.raises(ValueError):
            interp(Symbol("x")) # type: ignore

    def test_pontos_muito_proximos(self):
        """Testa se o erro é pequeno para números muito próximos"""
        dominio = [0.0, 1e-12, 2e-12]
        imagem = [0.0, 1.0, 2.0]
        interp = InterpLinear(dominio, imagem)
        result = interp(1e-12)
        
        assert abs(result - 1.0) < 1e-9 # type: ignore

    def test_dados_inalterados(self):
        """Testa se o interpolador mantém domínio e imagem."""
        dominio = [0, 1, 2]
        imagem = [0, 1, 4]
        interp = InterpLinear(dominio, imagem)

        dominio.append(3)
        imagem.append(9)
 
        assert len(interp.dominio) == 3
        assert len(interp.imagem) == 3

    def test_interpolacao_pontos_originais(self):
        """Testa se os valores da interpolação são os mesmo dos originais."""
        dominio = [0, 2, 4, 6]
        imagem = [0, 1, 4, 9]
        interp = InterpLinear(dominio, imagem)
        
        for x, y in zip(dominio, imagem):
            assert math.isclose(interp(x), y, rel_tol=1e-12) # type: ignore

    def test_float_extremos(self):
        """Testa interpolação com valores muito grandes."""
        dominio = [1e-300, 1e300]
        imagem = [1e-300, 1e300]
        interp = InterpLinear(dominio, imagem)
        
        assert interp(1e150) > 0 # type: ignore

    def test_igualdade_instancias(self):
        """Testa se duas instâncias com mesmo domínio e imagem são iguais"""
        dominio = [0, 1, 2]
        imagem = [0, 1, 4]

        interp1 = InterpLinear(dominio, imagem)
        interp2 = InterpLinear(dominio, imagem)

        assert interp1(dominio[1]) == interp2(dominio[1])

    @pytest.mark.parametrize("dominio, imagem", [
        ([0, 1, 2], [0, math.nan, 4]),
        ([0, math.inf, 2], [0, 1, 4]),
        ([0, 1, 2], [0, math.inf, 4])
    ])
    def test_nan_e_inf(self, dominio, imagem):
        """Testa NaN e infinitos."""
        with pytest.raises(ValueError):
            InterpLinear(dominio, imagem)

    def test_grafico_roda_sem_erro(self):
        """Testa se o gráfico roda sem retornar erros."""
        dominio = [0, 1, 2]
        imagem = [0, 1, 4]
        interp = InterpLinear(dominio, imagem)
        interp.grafico(precisao=10)

class TestPoliInterp:
    @pytest.mark.parametrize(
        "dominio, imagem",
        [
            ([0, 1, 2], [1, 3, 7]),   # f(x) = x² + 2x + 1
            ([0, 1, 2, 3], [1, 2, 5, 10])
        ]
    )
    def test_interp_polinomial_valida(self, dominio, imagem):
        """Testa casos válidos de interpolação polinomial."""
        interp = PoliInterp(dominio, imagem)
        assert math.isclose(interp(dominio[0]), imagem[0], rel_tol=1e-12)
        assert math.isclose(interp(dominio[-1]), imagem[-1], rel_tol=1e-12)

        # Testa extrapolação fora do domínio
        with pytest.raises(ValueError, match="fora do intervalo"):
            interp(min(dominio) - 10)

    @pytest.mark.parametrize(
        "dominio, imagem",
        [
            ([], [1, 2, 3]),
            ([0, 1, 2], []),
            ([0, 1], [1]),
            ([0], [0]),
        ]
    )
    def test_interp_polinomial_invalida_valor(self, dominio, imagem):
        """Testa se entradas inconsistentes geram ValueError."""
        with pytest.raises(ValueError):
            PoliInterp(dominio, imagem)

    @pytest.mark.parametrize(
        "dominio, imagem",
        [
            ("a", [1]),
            ([1], "a"),
            (1, 1),
        ]
    )
    def test_interp_polinomial_invalida_tipo(self, dominio, imagem):
        """Testa se entradas com tipos errados geram TypeError."""
        with pytest.raises(TypeError):
            PoliInterp(dominio, imagem)

    def test_nao_ordenado(self):
        """Testa se as entradas são ordenadas corretamente."""
        dominio = [3, 1, 2]
        imagem = [10, 2, 5]
        interp = PoliInterp(dominio, imagem)
        assert list(interp.pares_ord) == [(1, 2), (2, 5), (3, 10)]

    def test_pontos_repetidos(self):
        """Testa se o domínio não pode ter valores repetidos."""
        dominio = [0, 1, 1, 2]
        imagem = [0, 1, 2, 3]
        with pytest.raises(ValueError, match="repetidos"):
            PoliInterp(dominio, imagem)

    def test_interpolacao_polinomial(self):
        """Testa a precisão da interpolação."""
        dominio = [0, 1, 2]
        imagem = [1, 3, 7]  # f(x)=x²+2x+1
        interp = PoliInterp(dominio, imagem)
        assert math.isclose(interp(1.5), 1.5**2 + 2*1.5 + 1, rel_tol=1e-9)

    def test_call_tipo_errado(self):
        """Testa se o método __call__ rejeita tipos inválidos."""
        dominio = [0, 1]
        imagem = [0, 1]
        interp = PoliInterp(dominio, imagem)
        with pytest.raises(ValueError):
            interp("a")  # type: ignore

    def test_simbolo_no_call(self):
        """Testa passar símbolo simbólico."""
        dominio = [0, 1, 2]
        imagem = [0, 1, 4]
        interp = PoliInterp(dominio, imagem)
        with pytest.raises(ValueError):
            interp(Symbol("x"))  # type: ignore

    def test_dados_inalterados(self):
        """Testa se o objeto mantém cópia interna dos dados."""
        dominio = [0, 1, 2]
        imagem = [0, 1, 4]
        interp = PoliInterp(dominio, imagem)
        dominio.append(3)
        imagem.append(9)
        assert len(interp.dominio) == 3
        assert len(interp.imagem) == 3

    def test_pontos_muito_proximos(self):
        """Testa precisão numérica com pontos próximos."""
        dominio = [0.0, 1e-10, 2e-10]
        imagem = [0.0, 1.0, 4.0]
        interp = PoliInterp(dominio, imagem)
        r = interp(1e-10)
        assert abs(r - 1.0) < 1e-6

    def test_nan_e_inf(self):
        """Testa presença de NaN e infinitos."""
        casos = [
            ([0, math.inf, 2], [0, 1, 4]),
            ([0, 1, 2], [0, math.inf, 4]),
            ([0, 1, 2], [0, math.nan, 4])
        ]
        for dominio, imagem in casos:
            with pytest.raises(ValueError):
                PoliInterp(dominio, imagem)

    def test_igualdade_instancias(self):
        """Testa se duas instâncias com mesmos dados são equivalentes."""
        dominio = [0, 1, 2]
        imagem = [0, 1, 4]
        interp1 = PoliInterp(dominio, imagem)
        interp2 = PoliInterp(dominio, imagem)
        assert interp1(1.5) == pytest.approx(interp2(1.5))

    def test_grafico_roda_sem_erro(self):
        """Testa se o método gráfico executa sem erro."""
        dominio = [0, 1, 2]
        imagem = [0, 1, 4]
        interp = PoliInterp(dominio, imagem)
        interp.grafico(precisao=10)

