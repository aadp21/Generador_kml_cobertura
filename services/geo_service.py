# services/geo_service.py

import math
from typing import List, Tuple
from core.models import Sector
from core.constants import DEFAULT_SECTOR_STEPS


class GeoService:
    EARTH_RADIUS_KM = 6371.0

    def destination_point(self, lat: float, lon: float, azimuth_deg: float, distance_km: float) -> Tuple[float, float]:
        """Calcula el punto destino dado un punto, azimut y distancia (como tu calcular_destino)."""
        azimuth_rad = math.radians(azimuth_deg)
        lat1 = math.radians(lat)
        lon1 = math.radians(lon)

        lat2 = math.asin(math.sin(lat1) * math.cos(distance_km / self.EARTH_RADIUS_KM) +
                         math.cos(lat1) * math.sin(distance_km / self.EARTH_RADIUS_KM) * math.cos(azimuth_rad))
        lon2 = lon1 + math.atan2(
            math.sin(azimuth_rad) * math.sin(distance_km / self.EARTH_RADIUS_KM) * math.cos(lat1),
            math.cos(distance_km / self.EARTH_RADIUS_KM) - math.sin(lat1) * math.sin(lat2)
        )
        return math.degrees(lat2), math.degrees(lon2)

    def build_sector_polygon(
        self,
        lat: float,
        lon: float,
        sector: Sector,
        distance_km: float,
    ) -> List[Tuple[float, float]]:
        """
        Genera la lista de puntos (lon, lat) que forman el polígono del sector.
        Cierra el polígono volviendo al punto central.
        """
        puntos: List[Tuple[float, float]] = []
        inicio = sector.azimuth - sector.aperture_deg / 2
        fin = sector.azimuth + sector.aperture_deg / 2
        steps = sector.steps or DEFAULT_SECTOR_STEPS

        for i in range(steps + 1):
            angulo = inicio + i * (fin - inicio) / steps
            lat2, lon2 = self.destination_point(lat, lon, angulo, distance_km)
            puntos.append((lon2, lat2))

        # Cerrar polígono al punto de origen
        puntos.append((lon, lat))
        return puntos
