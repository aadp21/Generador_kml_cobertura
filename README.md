# 🗺️ Generador de Cobertura KML

Aplicación en **Python + Tkinter** para generar archivos `.kml` con coberturas sectorizadas por tecnología móvil (LTE700, LTE1900, LTE2600, y futuras bandas como NR3500).

Permite ingresar un sitio (POP) con sus coordenadas, definir azimuts por sector, seleccionar las tecnologías activas y generar un archivo KML compatible con Google Earth.

---

## 🧱 Estructura del Proyecto
kml_cobertura/
├─ app/
│ └─ controller.py # Lógica central: valida inputs y orquesta los servicios
├─ config/
│ └─ settings.py # URLs y configuraciones globales
├─ core/
│ ├─ constants.py # Constantes globales (colores, aperturas)
│ └─ models.py # Clases base (Site, Sector, TechnologySelection)
├─ services/
│ ├─ distance_service.py # Distancias según entorno (Ciudad / Población)
│ ├─ elevation_service.py # Obtiene elevación vía API
│ ├─ geo_service.py # Cálculos geográficos (azimut, destino)
│ └─ kml_service.py # Genera archivo KML con SimpleKML
├─ ui/
│ └─ main_window.py # Interfaz gráfica (Tkinter)
├─ main.py # Punto de entrada principal
├─ requirements.txt # Dependencias del entorno virtual
├─ update_requirements.py # Script para actualizar requirements.txt
└─ .gitignore # Archivos y carpetas que no se deben subir a GitHub
