import requests
from src.models import Pelicula
from src.catalog import ArbolCatalogo

RUTA_JSON = "data/dataset.json"


def obtener_datos_api(pagina: int = 0) -> list:
    """Obtiene películas/series desde TVMaze API (gratuita, sin API key)."""
    url = f"https://api.tvmaze.com/shows?page={pagina}"
    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al conectar a la API: {e}")
        return []


def poblar_catalogo_desde_api(arbol: ArbolCatalogo, datos_json: list):
    """Mapea los datos de la API al modelo Pelicula e inserta en el árbol."""
    print(f"Procesando {len(datos_json)} títulos...")

    for item in datos_json:
        genres = item.get("genres", [])
        categoria = genres[0] if genres else "Sin categoría"

        rating = item.get("rating", {})
        puntuacion = float(rating.get("average") or 0.0)

        premiered = item.get("premiered") or "2000-01-01"
        anio = int(premiered[:4])

        network = item.get("network") or {}
        canal = network.get("name") or "Desconocido"

        pelicula = Pelicula(
            id=item["id"],
            titulo=item["name"][:50],
            director=canal[:30],          # TVMaze no tiene director; usamos el canal
            anio=anio,
            categoria=categoria[:30],
            puntuacion=puntuacion,
            num_votos=item.get("weight", 0)
        )
        arbol.insertar(pelicula)


def mostrar_menu():
    print("\n" + "=" * 52)
    print("  🎬 SISTEMA DE CALIFICACIÓN DE PELÍCULAS V2.0  ")
    print("=" * 52)
    print("1. 🌐 Cargar títulos desde API (TVMaze)")
    print("2. 📋 Ver catálogo completo (In-Order)")
    print("3. 🔍 Buscar película por ID")
    print("4. 🗑️  Eliminar película por ID")
    print("5. 💾 Guardar catálogo en disco (JSON)")
    print("6. 📂 Cargar catálogo desde disco (JSON)")
    print("7. 🌳 Mostrar estructura del árbol (Visual)")
    print("8. ❌ Salir")
    print("=" * 52)


def main():
    catalogo = ArbolCatalogo()

    # Intentar cargar catálogo previo al arrancar
    catalogo.cargar_desde_json(RUTA_JSON)

    while True:
        mostrar_menu()
        opcion = input("Seleccionar una opción (1-8): ").strip()

        if opcion == "1":
            try:
                pagina = int(input("¿Qué página cargar? (0 = primeras ~250 entradas): ").strip() or "0")
            except ValueError:
                pagina = 0
            datos = obtener_datos_api(pagina)
            if datos:
                poblar_catalogo_desde_api(catalogo, datos)
                print(f"✅ Catálogo actualizado: {catalogo._size} títulos en total.")

        elif opcion == "2":
            if catalogo._size == 0:
                print("El catálogo está vacío.")
            else:
                print(f"\n{'ID':<7} | {'AÑO':<5} | {'PUNT.':<5} | {'CATEGORÍA':<22} | {'TÍTULO'}")
                print("-" * 82)
                for peli in catalogo.recorrer_inorder():
                    print(f"{peli.id:<7} | {peli.anio:<5} | {peli.puntuacion:<5} | {peli.categoria:<22} | {peli.titulo}")

        elif opcion == "3":
            try:
                id_buscar = int(input("Ingresa el ID a buscar: ").strip())
                resultado = catalogo.buscar(id_buscar)
                if resultado:
                    print(f"\n✅ Película encontrada:")
                    print(f"    - Título:     {resultado.titulo}")
                    print(f"    - Canal/Red:  {resultado.director}")
                    print(f"    - Año:        {resultado.anio}")
                    print(f"    - Categoría:  {resultado.categoria}")
                    print(f"    - Puntuación: {resultado.puntuacion} ⭐")
                    print(f"    - Popularidad:{resultado.num_votos:,}")
                else:
                    print("❌ No se encontró ninguna película con ese ID.")
            except ValueError:
                print("Ingresa un número válido.")

        elif opcion == "4":
            try:
                id_eliminar = int(input("Ingresa el ID a eliminar: ").strip())
                if catalogo.eliminar(id_eliminar):
                    print(f"✅ Película con ID {id_eliminar} eliminada correctamente.")
                else:
                    print(f"❌ No se encontró película con ID {id_eliminar}.")
            except ValueError:
                print("Ingresa un número válido.")

        elif opcion == "5":
            catalogo.guardar_en_json(RUTA_JSON)

        elif opcion == "6":
            catalogo.cargar_desde_json(RUTA_JSON)

        elif opcion == "7":
            if catalogo._size == 0:
                print("El catálogo está vacío.")
            else:
                print("\nEstructura del árbol binario:")
                catalogo.imprimir_arbol()

        elif opcion == "8":
            print("👋 ¡Hasta pronto!")
            break

        else:
            print("⚠ Opción no válida. Elige entre 1 y 8.")


if __name__ == "__main__":
    main()
