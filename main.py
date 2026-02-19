from src.models import Pelicula
from src.catalog import ArbolCatalogo

# Definir la ruta del json
RUTA_JSON = "data/dataset.json"

def run():
    catalogo = ArbolCatalogo()

    # Primer paso: Intentar cargar
    catalogo.cargar_desde_json(RUTA_JSON)

    # Si fuera la primera vez
    if catalogo._size == 0:
        print("---Primera Ejecución---")
        datos = [
            Pelicula(500, "Inception", "Christopher Nolan", 2010, "Ciencia Ficción", 8.8, 2400000),
            Pelicula(250, "El Padrino", "Francis Ford Coppola", 1972, "Drama", 9.2, 1900000),
            Pelicula(750, "Interstellar", "Christopher Nolan", 2014, "Ciencia Ficción", 8.6, 2000000),
            Pelicula(100, "Pulp Fiction", "Quentin Tarantino", 1994, "Crimen", 8.9, 2100000),
            Pelicula(500, "Inception", "Christopher Nolan", 2010, "Ciencia Ficción", 9.0, 100000),  # Duplicado para probar lógica
        ]

        for d in datos:
            catalogo.insertar(d)

        catalogo.guardar_en_json(RUTA_JSON)

    print(f"\nCatálogo actual: {catalogo._size} películas registradas.")
    print("Agregando nueva película al catálogo...")
    nueva = Pelicula(300, "El Señor de los Anillos", "Peter Jackson", 2001, "Fantasía", 8.8, 1800000)
    catalogo.insertar(nueva)

    catalogo.guardar_en_json(RUTA_JSON)

    catalogo.imprimir_arbol()
    print("Fin ejecución")

if __name__ == "__main__":
    run()
