from abc import ABC, abstractmethod


class Informe(ABC):
    """Contrato: todo informe sabe exportarse."""

    def __init__(self, id_informe, titulo, fecha_generacion):
        self._id_informe = id_informe
        self._titulo = titulo
        self._fecha_generacion = fecha_generacion

    @abstractmethod
    def exportar(self):
        ...

    def __str__(self):
        return (f"{type(self).__name__} {self._id_informe}: "
                f"{self._titulo} ({self._fecha_generacion})")