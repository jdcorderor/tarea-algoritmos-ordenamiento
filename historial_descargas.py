# Desarrollado por Juan Diego Cordero y Nelson Guerrero.

import json
from descarga import Descarga
from datetime import datetime

# Clase HistorialDescargas: Representa el historial de descargas del sistema.
# Atributos: Cola de descargas (pendientes y en progreso) y lista de descargas completadas.

class HistorialDescargas:
    # Constructor de la clase HistorialDescargas.
    def __init__(self):
        self.cola_descargas = []
        self.historial_completadas = []
        self.historial_canceladas = []

    # Método para cargar las descargas desde un archivo JSON.
    def cargar_descargas_desde_json(self, archivo_json):
        self.cola_descargas = []
        self.historial_completadas = []
        self.historial_canceladas = []
        with open(archivo_json, 'r') as file:
            datos = json.load(file)
            for descarga_data in datos:
                descarga = Descarga(
                    url=descarga_data['url'],
                    tamano=descarga_data['tamano'],
                    fecha_inicio=descarga_data['fecha_inicio'],
                    estado=descarga_data['estado']
                )
                if descarga.estado == 'completada':
                    self.historial_completadas.append(descarga)
                elif descarga.estado == 'pendiente' or descarga.estado == 'en_progreso':
                    self.cola_descargas.append(descarga)
                elif descarga.estado == 'cancelada':
                    self.historial_canceladas.append(descarga)
        print("Descargas cargadas correctamente desde el archivo JSON.")

    # Método para guardar las descargas en un archivo JSON.
    def añadir_descarga(self):
        url = input("Ingrese la URL de la descarga: ")
        while(True):
            try:
                tamano = float(input("Ingrese el tamaño de la descarga en MB: "))
                break
            except ValueError:
                print("El tamaño de la descarga debe ser un número.")
        while(True):
            estado = input("Indique el estado que desea visualizar (0 = completado, 1 = pendiente, 2 = en_progreso, 3 = cancelada): ")
            if estado == '0' or estado == '1' or estado == '2' or estado == '3':
                break
            else:
                print("Por favor, introduzca un número válido.")
        match estado:
            case '0':
                estado = "completada"
            case '1':
                estado = "pendiente"
            case '2':
                estado = "en_progreso"
            case '3':
                estado = "cancelada"
        fecha_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nueva_descarga = {"url": url,"tamano": tamano,"fecha_inicio": fecha_inicio,"estado": estado}
        with open("descargas.json", "r") as archivo:
            datos = json.load(archivo)
        datos.append(nueva_descarga)
        with open('descargas.json', 'w') as archivo:
            json.dump(datos, archivo, indent=4)
        self.cargar_descargas_desde_json("descargas.json")
        print("Datos añadidos exitosamente al archivo JSON.\n")

    # Método para mostrar las descargas por consola.
    def mostrar_descargas(self):
        print("\nDescargas completadas:")
        for descarga in self.historial_completadas:
            print(f"{descarga.url} - {descarga.tamano} - {descarga.fecha_inicio} - {descarga.estado}")
            
        print("\nDescargas en la cola (pendientes y en progreso):")
        for descarga in self.cola_descargas:
            print(f"{descarga.url} - {descarga.tamano} - {descarga.fecha_inicio} - {descarga.estado}")

        print("\nDescargas canceladas:")
        for descarga in self.historial_canceladas:
            print(f"{descarga.url} - {descarga.tamano} - {descarga.fecha_inicio} - {descarga.estado}")