"""
Script para actualizar automáticamente el archivo requirements.txt
con las versiones actuales del entorno virtual (.venv).
"""

import subprocess
import os

def generar_requirements():
    ruta = os.path.join(os.getcwd(), "requirements.txt")
    print(f"🔄 Generando archivo: {ruta}")

    try:
        with open(ruta, "w", encoding="utf-8") as f:
            subprocess.run(["pip", "freeze"], stdout=f, check=True)
        print("✅ requirements.txt actualizado correctamente.")
    except Exception as e:
        print(f"❌ Error al generar requirements.txt: {e}")

if __name__ == "__main__":
    generar_requirements()
