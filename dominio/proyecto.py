class Proyecto:
    """Actividades de desarrollo y los empleados asignados."""

    def __init__(self, id_proyecto, nombre, descripcion, fecha_inicio):
        self._id_proyecto = id_proyecto
        self._nombre = nombre
        self._descripcion = descripcion
        self._fecha_inicio = fecha_inicio
        self._empleados = []    # 0..* -> lista

    def asignar_empleado(self, empleado):
        if empleado not in self._empleados:
            self._empleados.append(empleado)
            empleado._proyectos.append(self)

    def desasignar_empleado(self, empleado):
        if empleado in self._empleados:
            self._empleados.remove(empleado)
            empleado._proyectos.remove(self)

    def get_detalles(self):
        pass