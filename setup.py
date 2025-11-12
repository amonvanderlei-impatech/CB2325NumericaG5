from setuptools import setup, find_packages

setup(
    name="CB2325NumericaG5",
    version="0.0.3",
    description=(
        "Biblioteca de cálculo numérico, contendo funcionalidades clássicas "
        "de análise numérica e recursos gráficos para visualização de resultados."
    ),
    author=", ".join([
        "Amon Vanderlei",
        "André Oliveira",
        "Carlos Santos",
        "Davi Campos",
        "Felipe Frohlich",
        "Gabriel Dias",
        "Lisandra Fagundes",
        "Lucas Corazza",
        "Lucas Oliveira",
        "Nicole Freire",
    ]),
    author_email=", ".join([
        "al.amon.vanderlei@impatech.edu.br",
        "al.andre.oliveira@impatech.edu.br",
        "al.carlos.santos@impatech.edu.br",
        "al.davi.campos@impatech.edu.br",
        "al.felipe.frohlich@impatech.edu.br",
        "al.gabriel.dias@impatech.edu.br",
        "al.lisandra.fagundes@impatech.edu.br",
        "al.lucas.corazza@impatech.edu.br",
        "al.lucas.oliveira@impatech.edu.br",
        "al.nicole.freire@impatech.edu.br",
    ]),
    license="MIT",
    packages=find_packages(include=["CB2325NumericaG5"]),
    install_requires=[
        "sympy",
        "matplotlib",
        "numpy",
    ],
    python_requires=">=3.8",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords=["Cálculo numérico", "Análise numérica"],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
