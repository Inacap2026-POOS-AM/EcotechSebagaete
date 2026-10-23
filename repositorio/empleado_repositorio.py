import sqlite3
from datetime import date

from dominio.empleado import Empleado
from dominio.excepciones import ErrorDeDominio, RutDuplicado
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

    def _existe_rut(self, rut):
        """Incluye empleados archivados: su RUT sigue ocupado."""
        with transaccion() as conn:
            fila = conn.execute(
                "SELECT 1 FROM empleado WHERE rut = ?", (rut,)
            ).fetchone()
        return fila is not None

    def guardar(self, empleado, departamento_id=None):
        try:
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
        except sqlite3.IntegrityError as error:
            if self._existe_rut(empleado.get_rut()):
                raise RutDuplicado(
                    f"Ya existe un empleado con RUT {empleado.get_rut()}"
                ) from error
            if "empleado.email" in str(error):
                raise ErrorDeDominio(
                    "Ya existe un empleado con ese email"
                ) from error
            raise ErrorDeDominio(
                "Datos rechazados: departamento inexistente o sueldo inválido"
            ) from error
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
                (f"%{nombre_contiene}%",),  # arma el dato, no el SQL
            ).fetchall()
        return [self._fila_a_empleado(f) for f in filas]

    def actualizar(self, empleado):
        try:
            with transaccion() as conn:
                cursor = conn.execute(
                    """UPDATE empleado
                       SET nombre = ?, telefono = ?, email = ?,
                           sueldo_base = ?
                       WHERE rut = ? AND activo = 1""",
                    (empleado.get_nombre(), empleado.get_telefono(),
                     empleado.get_email(), empleado.get_salario(),
                     empleado.get_rut()),
                )
        except sqlite3.IntegrityError as error:
            raise ErrorDeDominio(
                "No se pudo actualizar: el email ya está en uso "
                "o los datos no son válidos"
            ) from error
        return cursor.rowcount

    def eliminar(self, rut):
        """Borrado lógico: archiva al empleado."""
        with transaccion() as conn:
            cursor = conn.execute(
                "UPDATE empleado SET activo = 0 WHERE rut = ? AND activo = 1",
                (rut,),
            )
        return cursor.rowcount > 0