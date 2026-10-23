from datetime import date

from dominio.empleado import Empleado
from infraestructura.conexion import transaccion


class EmpleadoRepositorio:
    """CRUD de empleados. Recibe y devuelve objetos del dominio."""

    @staticmethod
    def _fila_a_empleado(fila):
        return Empleado(
            rut=fila[0], nombre=fila[1], telefono=fila[2], email=fila[3],
            fecha_inicio_contrato=date.fromisoformat(fila[4]),
            salario=fila[5], contrasena_hash=fila[6],
        )

    def guardar(self, empleado, departamento_id=None):
        with transaccion() as conn:
            conn.execute(
                """INSERT INTO empleado
                   (rut, nombre, telefono, email, fecha_ingreso,
                    sueldo_base, contrasena_hash, departamento_id)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (empleado.get_rut(), empleado.get_nombre(),
                 empleado.get_telefono(), empleado.get_email(),
                 empleado.get_fecha_inicio_contrato().isoformat(),
                 empleado.get_salario(), empleado.get_contrasena_hash(),
                 departamento_id),
            )
        return empleado

    def obtener(self, rut):
        with transaccion() as conn:
            fila = conn.execute(
                """SELECT rut, nombre, telefono, email, fecha_ingreso,
                          sueldo_base, contrasena_hash
                   FROM empleado WHERE rut = ? AND activo = 1""",
                (rut,),
            ).fetchone()
        return self._fila_a_empleado(fila) if fila else None

    def listar(self, nombre_contiene=""):
        with transaccion() as conn:
            filas = conn.execute(
                """SELECT rut, nombre, telefono, email, fecha_ingreso,
                          sueldo_base, contrasena_hash
                   FROM empleado
                   WHERE activo = 1 AND nombre LIKE ?
                   ORDER BY nombre""",
                (f"%{nombre_contiene}%",),  # solo arma el dato, no el SQL
            ).fetchall()
        return [self._fila_a_empleado(f) for f in filas]

    def actualizar(self, empleado):
        with transaccion() as conn:
            cursor = conn.execute(
                """UPDATE empleado
                   SET nombre = ?, telefono = ?, email = ?, sueldo_base = ?
                   WHERE rut = ? AND activo = 1""",
                (empleado.get_nombre(), empleado.get_telefono(),
                 empleado.get_email(), empleado.get_salario(),
                 empleado.get_rut()),
            )
        return cursor.rowcount

    def eliminar(self, rut):
        """Borrado lógico: archiva al empleado."""
        with transaccion() as conn:
            cursor = conn.execute(
                "UPDATE empleado SET activo = 0 WHERE rut = ? AND activo = 1",
                (rut,),
            )
        return cursor.rowcount > 0