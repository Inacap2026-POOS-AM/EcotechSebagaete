class Proyecto:
    """Actividades de desarrollo y los empleados asignados."""

    def __init__(self, id_proyecto, nombre, descripcion, fecha_inicio):
        self._id_proyecto = id_proyecto
        self._nombre = nombre
        self._descripcion = descripcion
        self._fecha_inicio = fecha_inicio
        self._empleados = []
        self._registros = []

    def get_id(self):
        return self._id_proyecto

    def set_id(self, valor):
        self._id_proyecto = valor

    def get_nombre(self):
        return self._nombre

    def get_descripcion(self):
        return self._descripcion

    def get_fecha_inicio(self):
        return self._fecha_inicio

    def asignar_empleado(self, empleado):
        if empleado not in self._empleados:
            self._empleados.append(empleado)
            empleado._proyectos.append(self)

    def desasignar_empleado(self, empleado):
        if empleado in self._empleados:
            self._empleados.remove(empleado)
            empleado._proyectos.remove(self)

    def get_detalles(self):
        return f"{self._nombre}: {self._descripcion}"

    def total_horas(self):
        return sum(r.get_cantidad_horas() for r in self._registros)

    def __str__(self):
        return (f"Proyecto {self._id_proyecto}: {self._nombre} "
                f"(inicio {self._fecha_inicio})")