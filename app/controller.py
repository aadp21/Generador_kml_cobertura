# AppController
# app/controller.py
from typing import Dict, Any, Optional, List

from core.models import Site, Sector, TechnologySelection
from services.distance_service import DistanceService
from services.elevation_service import ElevationService
from services.geo_service import GeoService
from services.kml_service import KmlService


class AppController:
    def __init__(self):
        self.distance_service = DistanceService()
        self.elevation_service = ElevationService()
        self.geo_service = GeoService()
        self.kml_service = KmlService(self.geo_service)

    def generate_kml_from_form(
        self,
        form_data: Dict[str, Any],
        output_path: str,
    ) -> Dict[str, Any]:
        """
        form_data debe traer:
          - name
          - lat
          - lon
          - environment ("ciudad" / "poblacion")
          - sectors: lista de dicts {name, azimuth}
          - technologies: dict con lte700, lte1900, lte2600
        """
        # 1. Validar
        name = form_data.get("name", "").strip()
        if not name:
            return {"ok": False, "error": "Debe ingresar un nombre para el sitio."}

        try:
            lat = float(form_data.get("lat"))
            lon = float(form_data.get("lon"))
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                raise ValueError()
        except Exception:
            return {"ok": False, "error": "Coordenadas en formato decimal inválido o fuera de rango."}

        environment = form_data.get("environment", "poblacion")

        # 2. Sectores
        raw_sectors: List[Dict[str, Any]] = form_data.get("sectors", [])
        sectors: List[Sector] = []
        for s in raw_sectors:
            az = s.get("azimuth")
            if az is None or str(az).strip() == "":
                # sector vacío → se omite
                continue
            try:
                az_f = float(az)
            except ValueError:
                # lo omitimos, igual que hacías con messagebox de advertencia
                continue
            sectors.append(Sector(name=s["name"], azimuth=az_f))

        if not sectors:
            return {"ok": False, "error": "Debe ingresar al menos un azimut."}

        # 3. Tecnologías
        tech_sel_dict = form_data.get("technologies", {})
        tech_sel = TechnologySelection(
            lte700=bool(tech_sel_dict.get("lte700")),
            lte1900=bool(tech_sel_dict.get("lte1900")),
            lte2600=bool(tech_sel_dict.get("lte2600")),
        )
        tech_list = tech_sel.selected_list()
        if not tech_list:
            # se podría permitir, pero tu versión pedía al menos 1
            return {"ok": False, "error": "Debe seleccionar al menos una tecnología."}

        # 4. Crear site
        site = Site(
            name=name,
            lat=lat,
            lon=lon,
            environment=environment,
            sectors=sectors
        )

        # 5. Distancias por entorno
        distances_by_tech = self.distance_service.get_distances(environment)

        # 6. Generar KML
        self.kml_service.generate_kml(
            site=site,
            technologies=tech_list,
            distances_by_tech=distances_by_tech,
            output_path=output_path,
        )

        # 7. Obtener elevación
        elevation = self.elevation_service.get_elevation(lat, lon)

        return {
            "ok": True,
            "elevation": elevation,
            "path": output_path,
        }
