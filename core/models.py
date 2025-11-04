# Site, Sector, Technology
# core/models.py
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Sector:
    """Representa un sector (A, B, C, D) con su azimut central."""
    name: str
    azimuth: float
    aperture_deg: float = 70.0   # se puede sobreescribir
    steps: int = 10


@dataclass
class Site:
    """Representa el sitio/POP donde están las antenas."""
    name: str
    lat: float
    lon: float
    # entorno: "ciudad" o "poblacion"
    environment: str = "poblacion"
    sectors: List[Sector] = field(default_factory=list)


@dataclass
class TechnologySelection:
    """Tecnologías seleccionadas por el usuario."""
    lte700: bool = False
    lte1900: bool = False
    lte2600: bool = False

    def selected_list(self) -> List[str]:
        techs = []
        if self.lte700:
            techs.append("LTE700")
        if self.lte1900:
            techs.append("LTE1900")
        if self.lte2600:
            techs.append("LTE2600")
        return techs
