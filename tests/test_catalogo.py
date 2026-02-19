import os
import pytest
from src.models import Pelicula

def test_insertar_raiz(catalogo, pelicula_ejemplo):
    # Verificamos que el primer insert sea la raiz
    catalogo.insertar(pelicula_ejemplo)
    assert catalogo.root is not None
    assert catalogo.root.data.id == 50
    assert catalogo._size == 1

def test_insertar_duplicado_recalcula_puntuacion(catalogo, pelicula_ejemplo):
    catalogo.insertar(pelicula_ejemplo)
    # Insertar la misma pelicula con nueva puntuacion y votos
    duplicado = Pelicula(
        id=50,
        titulo="Inception",
        director="Christopher Nolan",
        anio=2010,
        categoria="Ciencia Ficción",
        puntuacion=10.0,
        num_votos=2400000
    )
    catalogo.insertar(duplicado)

    buscada = catalogo.buscar(50)
    assert buscada.num_votos == 4800000
    assert catalogo._size == 1

def test_buscar_existente(catalogo_poblado):
    peli = catalogo_poblado.buscar(70)
    assert peli is not None
    assert peli.titulo == "Peli-70"

def test_buscar_no_existente(catalogo_poblado):
    peli = catalogo_poblado.buscar(999)
    assert peli is None

def test_recorrido_in_order_ordenado(catalogo_poblado):
    ids = [p.id for p in catalogo_poblado.recorrer_inorder()]
    assert ids == [20, 30, 40, 50, 60, 70, 80]

def test_persistencia_json(catalogo_poblado, tmp_path):
    archivo_test = tmp_path / "test_db.json"

    catalogo_poblado.guardar_en_json(str(archivo_test))
    assert os.path.exists(archivo_test)

    from src.catalog import ArbolCatalogo
    nuevo_catalogo = ArbolCatalogo()
    nuevo_catalogo.cargar_desde_json(str(archivo_test))

    assert nuevo_catalogo._size == 7
    assert nuevo_catalogo.buscar(50).titulo == "Peli-50"

def test_eliminar_nodo_hoja(catalogo_poblado):
    # Nodo 20 es hoja porque es hijo izquierdo del 30, sin hijos propios
    exito = catalogo_poblado.eliminar(20)
    assert exito is True
    assert catalogo_poblado.buscar(20) is None

def test_eliminar_nodo_dos_hijos(catalogo_poblado):
    # El 30 tiene dos hijos: 20 y 40
    catalogo_poblado.eliminar(30)
    assert catalogo_poblado.buscar(30) is None
    # Verificar que sus hijos no se perdieron
    assert catalogo_poblado.buscar(20) is not None
    assert catalogo_poblado.buscar(40) is not None
