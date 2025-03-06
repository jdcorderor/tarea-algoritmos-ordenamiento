# Desarrollado por Juan Diego Cordero y Nelson Guerrero.

from historial_descargas import HistorialDescargas
from reporte import Reporte

# Código principal.

# Instanciamos la clase HistorialDescargas.
historial = HistorialDescargas()

# Cargamos las descargas desde el archivo 'descargas.json'.
historial.cargar_descargas_desde_json('descargas.json')

# Instanciamos la clase Reporte.
reporte = Reporte(historial)

# Invocamos al método 'menu_reporte()' de la clase Reporte.
reporte.menu_reporte()