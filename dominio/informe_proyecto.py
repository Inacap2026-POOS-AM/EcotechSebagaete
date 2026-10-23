from dominio.informe import Informe


class InformeProyecto(Informe):
    """Informe de horas imputadas a un proyecto."""

    def __init__(self, id_informe, fecha_generacion, proyecto):
        super().__init__(id_informe, "Horas por proyecto", fecha_generacion)
        self._proyecto = proyecto

    def exportar(self):
        return (f"Horas en {self._proyecto.get_nombre()}: "
                f"{self._proyecto.total_horas()} h")