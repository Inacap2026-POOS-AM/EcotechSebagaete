from dominio.informe import Informe


class InformeNomina(Informe):
    """Informe de sueldos de un departamento."""

    def __init__(self, id_informe, fecha_generacion, departamento):
        super().__init__(id_informe, "Nómina", fecha_generacion)
        self._departamento = departamento

    def exportar(self):
        total = self._departamento.total_nomina()
        return (f"Nómina de {self._departamento.get_nombre()}: "
                f"${total:,.0f}")