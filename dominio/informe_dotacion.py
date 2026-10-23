from dominio.informe import Informe


class InformeDotacion(Informe):
    """Informe de cuántas personas tiene un departamento."""

    def __init__(self, id_informe, fecha_generacion, departamento):
        super().__init__(id_informe, "Dotación", fecha_generacion)
        self._departamento = departamento

    def exportar(self):
        return (f"{self._departamento.get_nombre()}: "
                f"{self._departamento.cantidad_empleados()} empleados")