# services/elevation_service.py
from typing import Optional
import requests
import certifi

from config.settings import OPEN_ELEVATION_URL, REQUEST_TIMEOUT


class ElevationService:
    def get_elevation(self, lat: float, lon: float) -> Optional[float]:
        params = {'locations': f"{lat},{lon}"}
        try:
            resp = requests.get(
                OPEN_ELEVATION_URL,
                params=params,
                timeout=REQUEST_TIMEOUT,
                verify=certifi.where()
            )
            resp.raise_for_status()
            data = resp.json()
            if "results" in data and isinstance(data["results"], list) and data["results"]:
                return data["results"][0].get("elevation")
            return None
        except Exception:
            # aquí podríamos loguear
            return None
