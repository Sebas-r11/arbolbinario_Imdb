import sys
import os
import time
import random
import string
from typing import List

# Ajuste para las importaciones
# importar src sin importar donde se ejecute el script

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models import Pelicula
from src.catalog import ArbolCatalogo

# Definicion de variables

CANTIDAD_DATOS = 1000000
RANGO_ID_INICIO = 100000
RANGO_ID_FIN = 999999

CATEGORIAS = ["Acción", "Drama", "Comedia", "Terror", "Ciencia Ficción", "Animación", "Fantasía"]

def generar_datos_falsos(n: int) -> List[Pelicula]:
    # Generar datos de forma masiva
    print(f"Generando {n} películas aleatorias")
    dataset = []

    start_gen = time.perf_counter()

    for _ in range(n):
        id_pelicula = random.randint(RANGO_ID_INICIO, RANGO_ID_FIN)
        titulo = ''.join(random.choices(string.ascii_uppercase, k=6))
        director = ''.join(random.choices(string.ascii_uppercase, k=8))
        categoria = random.choice(CATEGORIAS)

        pelicula = Pelicula(
            id=id_pelicula,
            titulo=f"FILM-{titulo}",
            director=f"DIR-{director}",
            anio=random.randint(1970, 2025),
            categoria=categoria,
            puntuacion=round(random.uniform(1.0, 10.0), 1),
            num_votos=random.randint(100, 5000000)
        )

        dataset.append(pelicula)

    end_gen = time.perf_counter()
    print(f"Datos generados en {end_gen - start_gen:.4f} segundos")
    return dataset

def busqueda_lineal_lista(dataset: List[Pelicula], id_objetivo: int):
    # Busqueda elemento por elemento para la lista
    for p in dataset:
        if p.id == id_objetivo:
            return p
    return None

def ejecutar_benchmark():
    print("\n" + "="*60)
    print(f"INICIANDO BENCHMARK")
    print("="*60)

    # Primer paso: Generar datos
    datos = generar_datos_falsos(CANTIDAD_DATOS)

    # Segundo paso, elegir el id a buscar
    target = datos[-1].id
    print(f"El objetivo es el id: {target}")

    # Poblar el arbol
    print("\nPoblando el arbol...")
    catalogo = ArbolCatalogo()

    start_load = time.perf_counter()

    for p in datos:
        catalogo.insertar(p)

    end_load = time.perf_counter()
    print(f"Tiempo de insercion de datos al arbol es de {end_load - start_load:.4f} segundos")
    print(f"Total de los nodos unicos es de {catalogo._size}")

    print("\n" + "-"*30)
    print("Empezamos la carrera de la lista versus el arbol")
    print("-"*30)

    # Hacer busqueda en la lista

    print("Iniciando busqueda lineal de la lista")
    start_list = time.perf_counter()
    res_list = busqueda_lineal_lista(datos, target)
    end_list = time.perf_counter()
    tiempo_lista = end_list - start_list
    print(f"El tiempo de la lista fue de {tiempo_lista:.10f} segundos")

    # Hacer la busqueda en el arbol

    print("Iniciando busqueda binaria en el arbol")
    start_tree = time.perf_counter()
    res_tree = catalogo.buscar(target)
    end_tree = time.perf_counter()
    tiempo_tree = end_tree - start_tree
    print(f"El tiempo del arbol fue de {tiempo_tree:.10f} segundos")

    # Imprimir resultados

    print("\n" + "="*60)
    print("RESULTADOS FINALES")
    print("="*60)

    if tiempo_tree > 0:
        diferencia = tiempo_lista / tiempo_tree
        print(f"El Arbol Binario fue {diferencia:,.2f} veces mas rapido que la lista")
    else:
        print("El arbol hizo la busqueda en 0 segundos")

    print("\n" + "="*60)

if __name__ == "__main__":
    ejecutar_benchmark()
