# CB2325NumericaG5

<p align="center">  
<img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/amonvanderlei-impatech/CB2325NumericaG5" />  
<img alt="Github License" src="https://img.shields.io/github/license/amonvanderlei-impatech/CB2325NumericaG5" />
<img alt="GitHub Repo Size" src="https://img.shields.io/github/repo-size/amonvanderlei-impatech/CB2325NumericaG5" />  
<img alt="GitHub Issues" src="https://img.shields.io/github/issues/amonvanderlei-impatech/CB2325NumericaG5" />  
<img alt="GitHub Pull Requests" src="https://img.shields.io/github/issues-pr/amonvanderlei-impatech/CB2325NumericaG5" />  
<img alt="GitHub Release" src="https://img.shields.io/github/v/release/amonvanderlei-impatech/CB2325NumericaG5">
<img alt="PyPI - Version" src="https://img.shields.io/pypi/v/CB2325NumericaG5">
</p>


## Descrição do Projeto

O **CB2325NumericaG5** é um módulo de **Cálculo Numérico** desenvolvido com o objetivo de fornecer ferramentas completas e didáticas para operações fundamentais da disciplina.

Todos os métodos foram implementados manualmente, sem depender de rotinas prontas de alto nível (como `numpy.linalg.solve`), favorecendo o estudo dos algoritmos.

## Estrutura do Módulo

O projeto é dividido nos seguintes submódulos:

* **[erros](docs/erros.md)**: Métodos para calcular erros numéricos.
* **[raizes](docs/raizes.md)**: Métodos para calcular raízes de funções.
* **[interpolacao](docs/interpolacao.md)**: Métodos para interpolação polinomial.
* **[aproximacao](docs/aproximacao.md)**: Métodos de aproximação de funções.
* **[integracao](docs/integracao.md)**: Métodos para realizar integração numérica.

## Instalação

### Opção 1 — Instalar via `pip` (PyPI)

Requer **Python 3.8+**:

```bash
pip install CB2325NumericaG5
```

### Opção 2 — Usar localmente

Se você baixou o repositório e deseja rodar um arquivo `exemplo.py` **dentro da pasta `/sandbox`**, basta adicionar o diretório raiz ao `sys.path` para permitir importações locais.

Exemplo:

```python
import sys, os

# Adiciona a pasta raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CB2325NumericaG5.erros import erro_absoluto

valor_real = 3.141592
valor_aprox = 3.14

ea = erro_absoluto(valor_real, valor_aprox)
print(ea, er)
```

> Esse é o formato **exato** recomendado quando o módulo está sendo usado localmente no `/sandbox`.

## Dependências

O pacote requer as seguintes bibliotecas:

| Pacote | Uso |
| :--- | :--- |
| `numpy` | Operações numéricas e geração de amostras. |
| `sympy` | Manipulação e cálculo simbólico. |
| `matplotlib` | Geração de gráficos e visualização de dados. |

## Autoria

O desenvolvimento deste módulo foi realizado por:

  - [Amon Vanderlei](https://github.com/amonvanderlei-impatech)
  - [André Oliveira](https://github.com/AndreFurriel)
  - [Carlos Santos](https://github.com/Cadueduedu)
  - [Davi Campos](https://github.com/davipestana-impatech)
  - [Felipe Frohlich](https://github.com/papaidoceu2)
  - [Gabriel Dias](https://github.com/GabrielKrauss2025)
  - [Lisandra Fagundes](https://github.com/lisandra21)
  - [Lucas Corazza](https://github.com/LucasCorazza2025)
  - [Lucas Oliveira](https://github.com/allucasoliveira-lab)
  - [Nicole Freire](https://github.com/al-nicole-freire)

-----

## Licença

Este projeto está sob a [Licença MIT](LICENSE).
