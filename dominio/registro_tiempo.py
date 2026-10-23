class RegistroTiempo:
    """Registro de las horas trabajadas por un empleado."""

    def __init__(self, id_registro, fecha, cantidad_horas,
                 descripcion_tareas):
        self._id_registro = id_registro
        self._fecha = fecha
        self._cantidad_horas = cantidad_horas
        self._descripcion_tareas = descripcion_tareas

    def validar_entrada(self):
        pass

    def get_cantidad_horas(self):
        pass

    def set_cantidad_horas(self, horas):
        pass