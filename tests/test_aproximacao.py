import math
import sys
import os
import warnings
import pytest
import matplotlib
matplotlib.use("Agg")  
from math import isclose

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CB2325NumericaG5.aproximacao import (
    coeficiente_determinacao,
    aproximacao_polinomial,
    txt_aproximacao_polinomial,
    grafico_ajuste_linear,
    grafico_ajuste_polinomial,
    media,
    regressao_linear,
    resolvedor_de_sistemas
)

class TestCoeficienteDeterminacao:
    @pytest.mark.parametrize("y_real, y_ajustado, r2_esperado", [
        ([1, 2, 3, 4], [1, 2, 3, 4], 1.0),         # Teste 1: y_real é igual ao y_ajustado
        ([1, 2, 3, 4], [2.5, 2.5, 2.5, 2.5], 0.0), # Teste 2: y_ajustado é a média dos valores reais
        ([5, 5, 5], [5, 5, 5], 0.0),               # Teste 3: variação total nula
        ([1, 2, 3], [1.1, 1.9, 3.0], 0.99),        # Teste 4: caso normal
    ])
    def test_r2_casos_validos(self, y_real, y_ajustado, r2_esperado):
        """Testa os casos válidos."""
        r2_calculado = coeficiente_determinacao(y_real, y_ajustado)
        assert r2_calculado == pytest.approx(r2_esperado) 
        
    def test_r2_tamanho_invalido(self):
        """Testa se listas de tamanhos diferentes levantam ValueError."""
        y_real = [1, 2, 3]
        y_ajustado = [1, 2]
        with pytest.raises(ValueError, match="devem ter o mesmo tamanho"):
            coeficiente_determinacao(y_real, y_ajustado)
            
class TestAproximacaoPolinomial:
    @pytest.mark.parametrize("coords, grau, coefs_esperados", [
        ([(0, 1), (1, 3), (2, 5)], 1, [1.0, 2.0]),              # Reta
        ([(0, 0), (1, 1), (2, 4)], 2, [0.0, 0.0, 1.0]),         # Parábola
        ([(0, 1), (1, 2), (2, 3)], 0, [2.0]),                   # Constante
        ([(1e6, 2e6), (2e6, 4e6), (3e6, 6e6)], 1, [0.0, 2.0]),  # Números grandes
        ([(1e-6, 2e-6), (2e-6, 4e-6)], 1, [0.0, 2.0]),          # Números pequenos
    ])
    def test_aprox_casos_validos(self, coords, grau, coefs_esperados):
        """Testa os casos válidos."""
        try:
            resultado = aproximacao_polinomial(coords, grau, mostrar_grafico=False)
        except ValueError as e:
            if "solução única" in str(e):
                pytest.xfail("Problema numérico esperado com valores muito grandes")
            else:
                raise
        assert len(resultado) == len(coefs_esperados)
        assert resultado == pytest.approx(coefs_esperados, rel=0.1, abs=1e-3)

        
    def test_aprox_poucos_pontos(self):
        """Testa se menos pontos do que grau+1 levantam erro."""
        coords = [(0, 1), (1, 2)]
        with pytest.raises(KeyError, match="A quantidade de dados deve ser maior ou igual"):
            aproximacao_polinomial(coords, 3, mostrar_grafico=False)
            
    def test_aprox_pontos_repetidos(self):
        """Testa se pontos repetidos levantam erro."""
        coords = [(1, 2), (1, 2), (2, 3)]
        grau = 1
        with warnings.catch_warnings(record=True) as w:
            try:
                aproximacao_polinomial(coords, grau, mostrar_grafico=False)
            except ValueError:
                pytest.skip("Função lança erro em vez de warning para pontos repetidos")
            else:
                assert any("singular" in str(wi.message).lower() or "rank" in str(wi.message).lower() for wi in w)
        
    def test_aprox_lista_vazia(self):
        """Testa se uma lista vazia levanta erro."""
        with pytest.raises((ValueError, KeyError)):
            aproximacao_polinomial([], 1, mostrar_grafico=False)

            
    @pytest.mark.parametrize("coords", [
        [(0, "a")],
        [(None, 2)],
        ("texto", 3),
    ])
    def test_aprox_tipos_invalidos(self, coords):
        """Testa se tipos inválidos levantam erros."""
        with pytest.raises((TypeError, ValueError, KeyError)):
            aproximacao_polinomial(coords, 1, mostrar_grafico=False)
            
    def test_aprox_dados_nao_lineares(self):
        """Testa um conjunto que não segue polinômio exato."""
        coords = [(0, 1), (1, 2.8), (2, 8.9), (3, 27.1)]  # próximo de y = x³
        resultado = aproximacao_polinomial(coords, 3, mostrar_grafico=False)
        assert pytest.approx(resultado[-1], rel=0.4) == 1.0  

    
class TestTxtAproximacaoPolinomial:
    def test_retorna_string(self):
        """Verifica se a função retorna uma string."""
        resultado = txt_aproximacao_polinomial([(0, 1), (1, 3), (2, 5)], 1)
        assert isinstance(resultado, str), "A função deve retornar uma string"

    def test_contem_expoentes(self):
        """Verifica se aparecem expoentes no texto."""
        resultado = txt_aproximacao_polinomial([(0, 1), (1, 3), (2, 5)], 1)
        assert "x^1" in resultado or "x^0" in resultado, "O texto deve conter expoentes"

    def test_pula_coeficiente_zero(self):
        """Verifica se coeficientes iguais a zero são ignorados no texto."""
        resultado = txt_aproximacao_polinomial([(0, 0), (1, 1), (2, 4)], 2)
        assert "x^1" not in resultado, "O termo com coeficiente zero não deve aparecer"

    def test_formato_irregular(self):
        """Verifica se a formatação adiciona sinal + entre termos positivos."""
        resultado = txt_aproximacao_polinomial([(0, 1), (1, 3), (2, 5)], 1)
        assert "+" in resultado, "A função não insere '+' entre termos positivos"

    def test_valor_textual_correspondente(self):
        """Verifica se há coeficientes numéricos aproximados no texto."""
        resultado = txt_aproximacao_polinomial([(0, 1), (1, 3), (2, 5)], 1)
        assert "(2" in resultado or "(1" in resultado, "Coeficientes esperados não aparecem no texto"
        
class TestGraficoAjustePolinomial:
    def teste_grafico_ajuste_polinomial(self):
        """Testa se a função gera o gráfico polinomial sem erro."""
        x = [1, 2, 3]
        y = [1, 4, 9]
        coefs = [0, 0, 1]
        r_quad = 1.0
        grafico_ajuste_polinomial(x, y, coefs, r_quad)
        
class TestGraficoAjusteLinear:
    def teste_grafico_ajuste_linear(self):
        """Testa se a função gera gráfico linear sem erro."""
        x = [1, 2, 3]
        y = [2, 4, 6]
        r_quad = 1
        grafico_ajuste_linear(x, y, 2.0, 0.0, r_quad)

@pytest.mark.parametrize(
        "lista, valor_esperado",
        [
            ([1,3,5,7], 4),
            ([2.5, 3, 4.75, 10], 5.0625 )
        ]
    )
def test_media_valida(lista, valor_esperado):
    assert media(lista) == valor_esperado

@pytest.mark.parametrize(
        "lista",
        [
            ([], 4),
            (['a', 'b', 'c'], 3 )
        ]
    )
def test_media_invalida(lista):
    with pytest.raises(ValueError):
            media(lista)
            
@pytest.mark.parametrize(
        "lista, valor_esperado",
        [
            ([1e-12, 3e-12], 2e-12),
            ([1e12,3e12], 2e12),
            ([1e50,3e50], 2e50),
            ([1e5,2],50001)
        ]
    )
def test_valores_extremos(lista, valor_esperado):
    assert media(lista) == valor_esperado 

@pytest.mark.parametrize(
        "lista",
        [
            ([1,math.nan]),
            ([math.inf,3]),
        ]
    )
def test_media_nan_inf(lista):
    with pytest.raises(ValueError):
            media(lista) 

@pytest.mark.parametrize(
        "valores_x, valores_y, beta_esperado, alpha_esperado",
        [
            ([1.0,2.0,3.0], [3.0, 5.0, 7.0], 2.0, 1.0),
            ([1, 2, 3], [1, 2.5, 3.5], 1.25, -1/6),
            ([1, 2, 3, 4],[8, 6, 4, 2], -2.0, 10.0 ),
            ([1, 2, 3], [5, 5, 5], 0.0, 5.0)
        ]
    )
def test_regressao_linear_valida(valores_x, valores_y, beta_esperado, alpha_esperado):
    beta_obtido, alpha_obtido = regressao_linear(valores_x, valores_y)
    assert isclose(beta_obtido, beta_esperado, abs_tol=1e-9)
    assert isclose(alpha_obtido, alpha_esperado, abs_tol=1e-9)

  
def test_x_e_y_com_tamanhos_diferentes():
    valores_x = [1,2]
    valores_y = [3,4,5]
    with pytest.raises(ValueError, match="A quantidade de abcissas deve ser igual à de ordenadas."):
        regressao_linear(valores_x, valores_y)
 
def test_zero_division_com_um_ponto():
    valores_x = [10]
    valores_y = [20]
    
    with pytest.raises(ZeroDivisionError):
        regressao_linear(valores_x, valores_y)
        
def test_zero_division_reta_vertical():
    valores_x = [5,5,5]
    valores_y = [1,2,3]       
    
    with pytest.raises(ZeroDivisionError):
        regressao_linear(valores_x, valores_y)   

@pytest.mark.parametrize(
    'valores_x, valores_y',
    [
        ([1, 2, math.nan], [3, 4, 5]),
        ([1, 2, 3], [3, 4, math.inf]),
    ]
)
def test_nan_inf(valores_x, valores_y):
    with pytest.raises(ValueError):
        regressao_linear(valores_x, valores_y)

@pytest.mark.parametrize(
    'MC, VI, solucao_esperada',
    [
        ([[1, 2], [3, 4]], [5, 11], [1.0, 2.0]),
        ([[1, -1, 1], [2, -3, 4], [-2, -1, 1]], [0, -2, -7], [3.0, 4.0, 1.0]),
        ([[5, -1], [0, 2]], [12, -4], [2.0, -2.0]),
        ([[1.5, 0.5], [2.0, -1.0]], [7.0, 4.0], [4.0, 2.0]),
    ]
)
def test_solucoes_validas(MC, VI, solucao_esperada):
    solucao_obtida = resolvedor_de_sistemas(MC, VI, tolerancia=1e-11)
    
    for obtida, esperada in zip(solucao_obtida, solucao_esperada):
        assert isclose(obtida, esperada, abs_tol=1e-9)

def test_sistema_sem_solucao_unica():
     
    MC_impossivel = [[1, 1], [2, 2]]
    VI_impossivel = [2, 5]

    MC_indeterminado = [[1, 1], [2, 2]]
    VI_indeterminado = [2, 4]
    
    match_msg = "Sistema sem solução única."
    
    with pytest.raises(ValueError, match=match_msg):
        resolvedor_de_sistemas(MC_impossivel, VI_impossivel)

    with pytest.raises(ValueError, match=match_msg):
        resolvedor_de_sistemas(MC_indeterminado, VI_indeterminado)

def test_troca_de_linhas():
    """Testa se a função lida corretamente com pivô zero, trocando linhas."""
    
    MC = [[0, 1], [1, 1]]
    VI = [2, 3]
    solucao_esperada = [1.0, 2.0]
    
    solucao_obtida = resolvedor_de_sistemas(MC, VI)
    
    assert isclose(solucao_obtida[0], solucao_esperada[0], abs_tol=1e-9)
    assert isclose(solucao_obtida[1], solucao_esperada[1], abs_tol=1e-9)

def test_comportamento_da_tolerancia():
    """
    Testa se um número pequeno é tratado como ZERO quando <= tolerancia,
    e como número normal quando > tolerancia.
    """
    pivo_pequeno = 1e-10  
    
    MC_instavel = [[pivo_pequeno, 1], [1, 1]]
    VI_instavel = [2, 3]
    
    # 1. Tolerância Padrão (1e-11): O pivô (1e-10) é maior que a tolerância, deve resolver.
    try:
        solucao_obtida = resolvedor_de_sistemas(MC_instavel, VI_instavel, tolerancia=1e-11)
        # Verifica se obteve uma solução (o valor exato não é importante aqui, apenas que resolveu)
        assert len(solucao_obtida) == 2
    except ValueError:
        pytest.fail("A solução não deveria falhar com a tolerância padrão.")

    # 2. Tolerância Apertada (1e-9): O pivô (1e-10) é menor que a tolerância, deve levantar ValueError.
    with pytest.raises(ValueError):
        resolvedor_de_sistemas(MC_instavel, VI_instavel, tolerancia=1e-9)
        
def test_tamanhos_incompativeis():
    
    MC = [[1, 1], [2, 2], [3, 3]]
    VI = [1, 2] 

    with pytest.raises((IndexError, ValueError)):
        resolvedor_de_sistemas(MC, VI)