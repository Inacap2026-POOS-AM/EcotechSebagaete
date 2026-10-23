class EmpleadoRepositorio:
    """Guarda y recupera empleados de la base de datos."""

    def guardar(self, emp):
        """Recibe un Empleado y lo inserta como fila en la tabla empleado."""
        sql = """INSERT INTO empleado
                 (rut, nombre, fecha_ingreso, sueldo_base)
                 VALUES (?, ?, ?, ?)"""
        pass

    def buscar_por_rut(self, rut):
        """Busca una fila por RUT y devuelve un Empleado (o None)."""
        sql = "SELECT rut, nombre, fecha_ingreso, sueldo_base " \
              "FROM empleado WHERE rut = ?"
        pass