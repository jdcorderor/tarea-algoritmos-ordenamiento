# Desarrollado por Juan Diego Cordero y Nelson Guerrero.

from historial_descargas import HistorialDescargas
from datetime import datetime

# Clase Reporte: Encargada de generar los reportes solicitados por el usuario.
# Atributos: Historial de descargas (objeto de la clase HistorialDescargas).

class Reporte:
    # Constructor de la clase Reporte.
    def __init__(self, historial_descargas: HistorialDescargas):
        self.historial_descargas = historial_descargas

    # Método para mostrar el menú de reportes. Solicita al usuario una opción y ejecuta el reporte correspondiente.
    def menu_reporte(self, band = True):
        while band:
            print("\n\nMenú de Reportes:")
            print("1. Mostrar descargas completadas de forma descendente por tamaño.")
            print("2. Mostrar descargas pendientes de forma ascendente por fecha de inicio.")
            print("3. Mostrar descargas ejecutadas a partir de una fecha, de forma ascendente por tamaño, y cuyas URL pertenezcan a un dominio indicado por el usuario.")
            print("4. Mostrar descargas de forma descendente por la longitud de su URL, que cumplan con un estado indicado por el usuario.")
            print("5. Mostrar todas las descargas.")
            print("6. Añadir nueva descarga.")
            print("7. Salir.")
            try:
                opcion = int(input("\nEstimado usuario, ingrese una opción: "))
            except ValueError:
                print("\n--- Opción no válida. Intente de nuevo.")
                continue
            if opcion == 1:
                reporte = self.quicksort(self.historial_descargas.historial_completadas, 0, len(self.historial_descargas.historial_completadas) - 1)
                self.mostrar_reporte(reporte, "Descargas completadas de forma descendente por tamaño")
            elif opcion == 2:
                reporte = self.mergesort(self.historial_descargas.cola_descargas + self.historial_descargas.historial_canceladas)
                self.mostrar_reporte(reporte, "Descargas no completadas de forma ascendente por fecha de inicio")
            elif opcion == 3:
                try:
                    fecha = datetime.strptime(input("Fecha de fin (YYYY-MM-DD HH:MM:SS): "), "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    print("\n--- Formato de fecha inválido.")
                    continue
                dominio = input("Dominio: ")
                if '.com' not in dominio and '.org' not in dominio and '.net' not in dominio and '.edu' not in dominio and '.gov' not in dominio:
                    print("\n--- Dominio no válido.")
                    continue
                reporte = self.heapsort(self.historial_descargas.cola_descargas + self.historial_descargas.historial_completadas + self.historial_descargas.historial_canceladas, fecha, dominio)
                self.mostrar_reporte(reporte, f"Descargas ejecutadas a partir de la fecha: {fecha}, de forma ascendente por tamaño, y cuyas URL pertenezcan al dominio: {dominio}")
            elif opcion == 4:
                estado = input("Estado: ")
                if self.validacion_estado(estado):
                    reporte = self.shellsort(self.historial_descargas.cola_descargas + self.historial_descargas.historial_completadas + self.historial_descargas.historial_canceladas, len(self.historial_descargas.cola_descargas + self.historial_descargas.historial_completadas + self.historial_descargas.historial_canceladas), estado)
                    self.mostrar_reporte(reporte, f"Descargas organizadas de forma descendente por la longitud de su URL, que cumplan con el estado: {estado}")
            elif opcion == 5:
                self.historial_descargas.mostrar_descargas()
            elif opcion == 6:
                self.historial_descargas.añadir_descarga()
            elif opcion == 7:
                band = False
            else:
                print("\n--- Opción no válida. Intente de nuevo.")

    # Método de ordenamiento QuickSort.
    def quicksort(self, arreglo, apuntador, indexpivote):
        if len(arreglo) == 1:
            return arreglo
        if apuntador < indexpivote:
            p = self.particion(arreglo, apuntador, indexpivote)
            self.quicksort(arreglo, apuntador, p - 1)
            self.quicksort(arreglo, p + 1, indexpivote)
        return arreglo
    
    # Método de partición para el QuickSort.
    def particion(self, arr, i, ip):
        pivote = arr[ip]
        for k in range(i, ip):
            if arr[k].tamano >= pivote.tamano:
                arr[k], arr[i] = arr[i], arr[k]
                i += 1
        arr[ip], arr[i] = arr[i], arr[ip]
        return ip
    
    # Método de ordenamiento MergeSort.
    def mergesort(self, arreglo):
        if len(arreglo) <= 1:
            return arreglo
        else:
            mediana = len(arreglo) // 2
            arreglo_izquierda = arreglo[:mediana]
            arreglo_derecha = arreglo[mediana:]
            arreglo_izquierda = self.mergesort(arreglo_izquierda)
            arreglo_derecha = self.mergesort(arreglo_derecha)
        return self.merge(arreglo_izquierda, arreglo_derecha)

    # Método de fusión para el MergeSort.
    def merge(self, izquierda, derecha):
        resultado = []
        i, j = 0, 0
        while i < len(izquierda) and j < len(derecha):
            if izquierda[i].fecha_inicio < derecha[j].fecha_inicio:
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1
        resultado.extend(izquierda[i:])
        resultado.extend(derecha[j:])   
        return resultado

    # Método de ordenamiento HeapSort.
    def heapsort(self, arreglo, fecha, dominio):
        tamano = len(arreglo)
        for i in range(tamano // 2 - 1, -1, -1):
            self.heapify(arreglo, tamano, i)
        for i in range(tamano - 1, 0, -1):
            arreglo[i], arreglo[0] = arreglo[0], arreglo[i]
            self.heapify(arreglo, i, 0)
        return [descarga for descarga in arreglo if dominio in descarga.url and self.convertir_datetime(descarga.fecha_inicio) > fecha]

    # Método de heapify para el HeapSort.
    def heapify(self, arr, n, i):
        mayor = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and arr[i].tamano < arr[l].tamano:
            mayor = l
        if r < n and arr[mayor].tamano < arr[r].tamano:
            mayor = r
        if mayor != i:
            arr[i], arr[mayor] = arr[mayor], arr[i]
            self.heapify(arr, n, mayor)

    # Método para convertir una fecha en formato string a datetime.
    def convertir_datetime(self, fecha):
        return datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")

    # Método de ordenamiento ShellSort.
    def shellsort(self, arreglo, n, estado):
        intervalo = n//2
        while intervalo > 0:
            for i in range(intervalo, n):
                temp = arreglo[i]
                j = i
                while j >= intervalo and len(arreglo[j - intervalo].url) < len(temp.url):
                    arreglo[j] = arreglo[j - intervalo]
                    j -= intervalo
                arreglo[j] = temp
            intervalo //= 2
        return [descarga for descarga in arreglo if descarga.estado == estado]
    
    # Metodo para mostrar el reporte.
    def mostrar_reporte(self, arreglo, membrete):
        if not arreglo:
            print("\n--- No hay descargas que cumplan con los criterios solicitados.")
        else:
            print(f"\n\n{membrete}:\n")
            for descarga in arreglo:
                print(f"{descarga.url} - {descarga.tamano} - {descarga.fecha_inicio} - {descarga.estado}\n")

    # Método de validación del estado de la descarga.
    def validacion_estado(self, estado):
        if estado not in ['completada', 'pendiente', 'cancelada', 'en_progreso']:
            print("\n--- Estado no válido. Intente de nuevo.\n(completada, pendiente, en_progreso, cancelada)")
            return False
        return True