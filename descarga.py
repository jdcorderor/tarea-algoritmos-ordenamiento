# Desarrollado por Juan Diego Cordero y Nelson Guerrero.

# Clase Descarga: Representa una descarga en el sistema.
# Atributos: URL, Tamaño, Fecha de Inicio, Estado (completada, en_progreso, pendiente, cancelada).

class Descarga:
    # Constructor de la clase Descarga.
    def __init__(self, url, tamano, fecha_inicio, estado):
        self.url = url
        self.tamano = tamano
        self.fecha_inicio = fecha_inicio
        self.estado = estado