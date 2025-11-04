# Tkinter, botones, entries
# ui/main_window.py
import tkinter as tk
from tkinter import messagebox, filedialog, IntVar

from app.controller import AppController


class MainWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Generador Cobertura por Banda")
        self.root.geometry("520x560")
        self.root.resizable(False, False)

        self.controller = AppController()

        self.FONT = ("Segoe UI", 11)

        self._build_ui()

    def _build_ui(self):
        # Nombre
        tk.Label(self.root, text="Código del POP:", font=self.FONT).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.entry_nombre = tk.Entry(self.root, font=self.FONT, width=25)
        self.entry_nombre.insert(0, "ej: CC242")
        self.entry_nombre.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        self.entry_lat = self._add_labeled_entry("Latitud (decimal):", 1)
        self.entry_lon = self._add_labeled_entry("Longitud (decimal):", 2)

        btn_elev = tk.Button(self.root, text="Consultar Elevación", font=("Segoe UI", 10),
                             command=self._on_check_elevation, bg="#cccccc")
        btn_elev.grid(row=3, column=1, pady=5)
        self.label_elevacion = tk.Label(self.root, text="", font=("Segoe UI", 10, "italic"))
        self.label_elevacion.grid(row=4, column=0, columnspan=3)

        # Azimuts
        self.entry_az_a = self._add_labeled_entry("Azimut Sector A:", 5)
        self.entry_az_b = self._add_labeled_entry("Azimut Sector B:", 6)
        self.entry_az_c = self._add_labeled_entry("Azimut Sector C:", 7)
        self.entry_az_d = self._add_labeled_entry("Azimut Sector D:", 8)

        # Tecnologías
        self.lte2600_var = tk.BooleanVar()
        self.lte700_var = tk.BooleanVar()
        self.lte1900_var = tk.BooleanVar()

        frame_tech = tk.LabelFrame(self.root, text="Tecnologías a incluir", font=self.FONT, padx=10, pady=10)
        frame_tech.grid(row=9, column=0, columnspan=3, padx=10, pady=10)

        tk.Checkbutton(frame_tech, text="LTE2600", variable=self.lte2600_var, font=self.FONT).grid(row=0, column=0, padx=10, pady=5)
        tk.Checkbutton(frame_tech, text="LTE700", variable=self.lte700_var, font=self.FONT).grid(row=0, column=1, padx=10, pady=5)
        tk.Checkbutton(frame_tech, text="LTE1900", variable=self.lte1900_var, font=self.FONT).grid(row=0, column=2, padx=10, pady=5)

        # Entorno
        self.entorno_var = IntVar()  # 0 = poblacion, 1 = ciudad
        entorno_check = tk.Checkbutton(self.root, text="Ciudad (si no está marcado es Población)", variable=self.entorno_var)
        entorno_check.grid(row=10, column=0, columnspan=5, sticky="w")

        btn = tk.Button(self.root, text="Generar archivo KML", font=("Segoe UI", 12, "bold"),
                        bg="#007acc", fg="white", command=self._on_generate_kml)
        btn.grid(row=12, column=0, columnspan=3, pady=20, ipadx=15, ipady=8)

        tk.Label(self.root, text="Realizado por: AD", font=("Segoe UI", 9, "italic"), fg="gray").grid(
            row=13, column=0, columnspan=3, pady=(0, 10)
        )

    def _add_labeled_entry(self, text, row, default_text=""):
        tk.Label(self.root, text=text, font=self.FONT).grid(row=row, column=0, sticky="w", padx=10, pady=5)
        entry = tk.Entry(self.root, font=self.FONT, width=25)
        if default_text:
            entry.insert(0, default_text)
        entry.grid(row=row, column=1, columnspan=2, padx=5, pady=5)
        return entry

    def _on_check_elevation(self):
        # usamos directamente el controller para no repetir lógica
        try:
            lat = float(self.entry_lat.get())
            lon = float(self.entry_lon.get())
        except ValueError:
            self.label_elevacion.config(text="Coordenadas inválidas")
            return

        elev = self.controller.elevation_service.get_elevation(lat, lon)
        if elev is not None:
            self.label_elevacion.config(text=f"Elevación del terreno: {elev} m")
        else:
            self.label_elevacion.config(text="No se pudo obtener la elevación")

    def _on_generate_kml(self):
        # 1. pedir ruta
        nombre_sitio = self.entry_nombre.get().strip()
        suggested_name = nombre_sitio if nombre_sitio else "sitio"
        archivo = filedialog.asksaveasfilename(
            defaultextension=".kml",
            filetypes=[("Archivos KML", "*.kml")],
            title="Guardar archivo KML",
            initialfile=f"{suggested_name}.kml"
        )
        if not archivo:
            return

        # 2. armar form_data como lo espera el controller
        form_data = {
            "name": nombre_sitio,
            "lat": self.entry_lat.get(),
            "lon": self.entry_lon.get(),
            "environment": "ciudad" if self.entorno_var.get() == 1 else "poblacion",
            "sectors": [
                {"name": "A", "azimuth": self.entry_az_a.get()},
                {"name": "B", "azimuth": self.entry_az_b.get()},
                {"name": "C", "azimuth": self.entry_az_c.get()},
                {"name": "D", "azimuth": self.entry_az_d.get()},
            ],
            "technologies": {
                "lte700": self.lte700_var.get(),
                "lte1900": self.lte1900_var.get(),
                "lte2600": self.lte2600_var.get(),
            }
        }

        result = self.controller.generate_kml_from_form(form_data, archivo)

        if not result.get("ok"):
            messagebox.showerror("Error", result.get("error", "Error desconocido"))
            return

        elev = result.get("elevation")
        if elev is not None:
            messagebox.showinfo("KML Generado", f"Archivo guardado:\n{archivo}\nElevación: {elev} metros.")
        else:
            messagebox.showinfo("KML Generado", f"Archivo guardado:\n{archivo}\nNo se pudo obtener la elevación.")
