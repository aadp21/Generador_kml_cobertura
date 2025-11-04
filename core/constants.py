# colores, aperturas, nombres
# core/constants.py

# Apertura por defecto del sector (70° como en tu código original)
DEFAULT_SECTOR_APERTURE_DEG = 70
DEFAULT_SECTOR_STEPS = 10

# Colores de los sectores (línea) en el KML
SECTOR_COLORS = {
    "A": "ffff0000",  # Azul en tu comentario, pero en KML es ARGB (esto era el original)
    "B": "ff0000ff",
    "C": "ff00ff00",
    "D": "ff00ffff",
}

# Colores de las tecnologías (polígonos) en el KML
TECH_COLORS = {
    "LTE700": "3300ff00",   # Verde
    "LTE1900": "660075ff",  # Naranja / violeta
    "LTE2600": "ff0000ff",  # Azul
}

# Nombres de carpetas que se crean en el KML
TECH_FOLDER_NAMES = {
    "LTE700": "Cobertura LTE700",
    "LTE1900": "Cobertura LTE1900",
    "LTE2600": "Cobertura LTE2600",
}
