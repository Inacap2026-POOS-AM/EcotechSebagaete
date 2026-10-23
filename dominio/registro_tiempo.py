class RegistroTiempo:
    """Registro de las horas trabajadas por un empleado."""

    def __init__(self, id_registro, fecha, cantidad_horas,
                 descripcion_tareas):
        self._id_registro = id_registro
        self._fecha = fecha
        self.set_cantidad_horas(cantidad_horas)
        self._descripcion_tareas = descripcion_tareas

    def set_cantidad_horas(self, horas):
        if not 0 < horas <= 24:
            raise ValueError("Las horas deben estar entre 0 y 24")
        self._cantidad_horas = horas

    def get_cantidad_horas(self):
        return self._cantidad_horas

    def validar_entrada(self):
        return 0 < self._cantidad_horas <= 24

    def __str__(self):
        return (f"Registro {self._id_registro}: {self._fecha} - "
                f"{self._cantidad_horas} h ({self._descripcion_tareas})")