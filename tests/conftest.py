import pytest
from src.models import Pelicula
from src.catalog import ArbolCatalogo

# Fixture

@pytest.fixture
def pelicula_ejemplo():
    return Pelicula(
        id=50,
        titulo="Inception",
        director="Christopher Nolan",
        anio=2010,
        categoria="Ciencia Ficción",
        puntuacion=8.8,
        num_votos=2400000
    )

@pytest.fixture
def catalogo():
    return ArbolCatalogo()

@pytest.fixture
def catalogo_poblado(catalogo):
    # Insertamos datos en desorden
    ids = [50, 30, 70, 20, 40, 60, 80]
    for id_val in ids:
        peli = Pelicula(
            id=id_val,
            titulo=f"Peli-{id_val}",
            director="Director General",
            anio=2000,
            categoria="Drama",
            puntuacion=7.0,
            num_votos=10000
        )
        catalogo.insertar(peli)
    return catalogo
