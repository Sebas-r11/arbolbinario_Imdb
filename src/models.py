from dataclasses import dataclass
from datetime import datetime

@dataclass
class Pelicula:
    id: int
    titulo: str
    director: str
    anio: int
    categoria: str
    puntuacion: float  # 0.0 a 10.0
    num_votos: int

    # Serializamos: Pasar el objeto a diccionario

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "director": self.director,
            "anio": self.anio,
            "categoria": self.categoria,
            "puntuacion": self.puntuacion,
            "num_votos": self.num_votos
        }

    # Des-serializar

    @staticmethod
    def from_dict(data: dict):
        return Pelicula(**data)  # Desempaquetado de datos
