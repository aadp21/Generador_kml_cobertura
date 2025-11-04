# services/kml_service.py
from typing import List, Dict
import simplekml

from core.models import Site, Sector
from core.constants import TECH_COLORS, TECH_FOLDER_NAMES, SECTOR_COLORS
from services.geo_service import GeoService


class KmlService:
    def __init__(self, geo_service: GeoService):
        self.geo = geo_service

    def generate_kml(
        self,
        site: Site,
        technologies: List[str],
        distances_by_tech: Dict[str, float],
        output_path: str,
    ):
        kml = simplekml.Kml()

        # Crear carpetas por tecnología
        folders = {}
        for tech in technologies:
            folder_name = TECH_FOLDER_NAMES.get(tech, tech)
            folders[tech] = kml.newfolder(name=folder_name)

        # Para cada sector del sitio
        for sector in site.sectors:
            # Línea del sector (como en tu código original, 2 km fijos solo para la línea)
            lat2, lon2 = self.geo.destination_point(site.lat, site.lon, sector.azimuth, 2.0)
            line = kml.newlinestring(
                name=f"Sector {sector.name} - {site.name}",
                coords=[(site.lon, site.lat), (lon2, lat2)]
            )
            line.style.linestyle.width = 4
            line.style.linestyle.color = SECTOR_COLORS.get(sector.name, "ff000000")

            # Ahora los polígonos por tecnología
            for tech in technologies:
                alcance_km = distances_by_tech.get(tech)
                if alcance_km is None:
                    continue

                puntos = self.geo.build_sector_polygon(
                    site.lat,
                    site.lon,
                    sector,
                    alcance_km
                )

                poligono = folders[tech].newpolygon(
                    name=f"{tech} - Sector {sector.name} ({site.environment.capitalize()})"
                )
                poligono.outerboundaryis = puntos
                poligono.style.polystyle.color = TECH_COLORS.get(tech, "7f00ff00")
                poligono.style.linestyle.width = 1
                poligono.style.linestyle.color = "ff000000"

        # Punto principal con descripción
        descripcion = "Coberturas incluidas:\n"
        for tech in technologies:
            descripcion += f"- {tech}\n"

        kml.newpoint(
            name=site.name,
            coords=[(site.lon, site.lat)],
            description=descripcion
        )

        kml.save(output_path)
