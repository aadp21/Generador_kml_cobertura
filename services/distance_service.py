# services/distance_service.py
from typing import Dict


class DistanceService:
    """
    Devuelve las distancias de cada tecnología según el entorno.
    entorno puede ser: "ciudad" o "poblacion"
    """

    def get_distances(self, environment: str) -> Dict[str, float]:
        if environment == "ciudad":
            return {
                "LTE2600": 0.15,
                "LTE700": 0.65,
                "LTE1900": 0.30,
            }
        # default: población
        return {
            "LTE2600": 1.0,
            "LTE700": 5.0,
            "LTE1900": 3.0,
        }
