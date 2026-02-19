from typing import Optional, Generator, List
from src.models import Pelicula
from src.node import NodoPelicula
import json
import os

class ArbolCatalogo:
    def __init__(self):
        self.root: Optional[NodoPelicula] = None
        self._size: int = 0  # Para benchmark rápido de tamaño

    def insertar(self, pelicula: Pelicula) -> None:
        if not self.root:
            self.root = NodoPelicula(pelicula)
            self._size += 1
        else:
            self._insertar_recursivo(self.root, pelicula)

    def _insertar_recursivo(self, actual: NodoPelicula, pelicula: Pelicula) -> None:
        if pelicula.id < actual.data.id:
            if actual.left is None:
                actual.left = NodoPelicula(pelicula)
                self._size += 1
            else:
                self._insertar_recursivo(actual.left, pelicula)
        elif pelicula.id > actual.data.id:
            if actual.right is None:
                actual.right = NodoPelicula(pelicula)
                self._size += 1
            else:
                self._insertar_recursivo(actual.right, pelicula)
        else:
            print(f"⚠ ID {pelicula.id} existente. Actualizando puntuación.")
            # Recalcular puntuacion promedio con el nuevo voto
            total_actual = actual.data.puntuacion * actual.data.num_votos
            total_nuevo = total_actual + pelicula.puntuacion * pelicula.num_votos
            actual.data.num_votos += pelicula.num_votos
            actual.data.puntuacion = round(total_nuevo / actual.data.num_votos, 2)

    def buscar(self, id: int) -> Optional[Pelicula]:
        return self._buscar_recursivo(self.root, id)

    def _buscar_recursivo(self, actual: Optional[NodoPelicula], id: int) -> Optional[Pelicula]:
        if actual is None or actual.data.id == id:
            return actual.data if actual else None

        if id < actual.data.id:
            return self._buscar_recursivo(actual.left, id)
        return self._buscar_recursivo(actual.right, id)

    # RETO: Uso de Generadores (yield) para eficiencia de memoria en recorridos masivos
    def recorrer_inorder(self) -> Generator[Pelicula, None, None]:
        yield from self._inorder_recursivo(self.root)

    def _inorder_recursivo(self, actual: Optional[NodoPelicula]) -> Generator[Pelicula, None, None]:
        if actual:
            yield from self._inorder_recursivo(actual.left)
            yield actual.data
            yield from self._inorder_recursivo(actual.right)

    # -- Persistencia de datos

    # Guardar el arbol en el disco usando json pre-order

    def guardar_en_json(self, ruta_archivo: str):
        print(f"Guardando archivo en {ruta_archivo}...")

        # Obtener la lista de los diccionarios
        lista_datos = [p.to_dict() for p in self.recorrer_preorder()]

        # Asegurarnos que ese directorio existe
        os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)

        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(lista_datos, f, indent=4, ensure_ascii=False)
        print("Guardado exitoso")

    def cargar_desde_json(self, ruta_archivo: str):
        # Leer el json y poblar arbol
        if not os.path.exists(ruta_archivo):
            print(f"⚠ La ruta para el archivo({ruta_archivo}) no existe.")
            return

        print(f"Cargando el catálogo desde {ruta_archivo}...")
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            lista_datos = json.load(f)

        self.root = None  # Limpiar el arbol
        self._size = 0

        for item in lista_datos:
            pelicula = Pelicula.from_dict(item)
            self.insertar(pelicula)

        print(f"Carga completada. {self._size} películas recuperadas")

    def recorrer_preorder(self) -> Generator[Pelicula, None, None]:
        yield from self._preorder_recursivo(self.root)

    def _preorder_recursivo(self, actual: Optional[NodoPelicula]) -> Generator[Pelicula, None, None]:
        if actual:
            yield actual.data  # raiz
            yield from self._preorder_recursivo(actual.left)
            yield from self._preorder_recursivo(actual.right)

    def eliminar(self, id: int) -> bool:
        self.root, eliminado = self._eliminar_recursivo(self.root, id)
        if eliminado:
            self._size -= 1
        return eliminado

    def _eliminar_recursivo(self, actual: Optional[NodoPelicula], id: int):
        if not actual:
            return actual, False

        if id < actual.data.id:
            actual.left, eliminado = self._eliminar_recursivo(actual.left, id)
        elif id > actual.data.id:
            actual.right, eliminado = self._eliminar_recursivo(actual.right, id)
        else:
            # Caso 1 y 2: Sin hijos o con un solo hijo
            if not actual.left:
                return actual.right, True
            if not actual.right:
                return actual.left, True

            # Caso 3: Dos Hijos
            temp = self._min_value_node(actual.right)
            actual.data = temp.data
            actual.right, _ = self._eliminar_recursivo(actual.right, temp.data.id)
            return actual, True

        return actual, eliminado

    def _min_value_node(self, nodo: NodoPelicula) -> NodoPelicula:
        current = nodo

        while current.left is not None:
            current = current.left

        return current

    def imprimir_arbol(self):
        if not self.root:
            print("El catálogo está vacío")
        else:
            self._imprimir_recursivo(self.root, 0, "Raíz: ")

    def _imprimir_recursivo(self, actual: Optional[NodoPelicula], nivel: int, prefijo: str):
        if actual is not None:
            print(" " * (nivel * 4) + f"{prefijo}[{actual.data.id}] {actual.data.titulo} | ⭐ {actual.data.puntuacion} | {actual.data.categoria}")
            if actual.left or actual.right:
                if actual.left:
                    self._imprimir_recursivo(actual.left, nivel + 1, "Izq-- ")
                else:
                    print(" " * ((nivel + 1) * 4) + "Izq-- Vacío")

                if actual.right:
                    self._imprimir_recursivo(actual.right, nivel + 1, "Der-- ")
                else:
                    print(" " * ((nivel + 1) * 4) + "Der-- Vacío")
