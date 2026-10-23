import sqlite3
from datetime import date

from dominio.excepciones import ErrorDeDominio
from dominio.proyecto import Proyecto
from infraestructura.conexion import transaccion


class ProyectoRepositorio:
    """Guarda proyectos y asigna empleados a ellos."""

    @staticmethod
    def _fila_a_proyecto(fila):
        return Proyecto(fila[0], fila[1], fila[2],
                        date.fromisoformat(fila[3]))

    def guardar(self, proyecto):
        with transaccion() as conn:
            cursor = conn.execute(
                """INSERT INTO proyecto (nombre, descripcion, fecha_inicio)
                   VALUES (?, ?, ?)""",
                (proyecto.get_nombre(), proyecto.get_descripcion(),
                 proyecto.get_fecha_inicio().isoformat()),
            )
            proyecto.set_id(cursor.lastrowid)
        return proyecto

    def obtener(self, id_proyecto):
        with transaccion() as conn:
            fila = conn.execute(
                """SELECT id, nombre, descripcion, fecha_inicio
                   FROM proyecto WHERE id = ?""",
                (id_proyecto,),
            ).fetchone()
        return self._fila_a_proyecto(fila) if fila else None

    def asignar_empleado(self, rut, id_proyecto):
        """Todo o nada: la asignación y su registro en la bitácora."""
        try:
            with transaccion() as conn:
                conn.execute(
                    """INSERT INTO empleado_proyecto (empleado_rut, proyecto_id)
                       VALUES (?, ?)""",
                    (rut, id_proyecto),
                )
                conn.execute(
                    """INSERT INTO bitacora
                       (fecha, accion, empleado_rut, proyecto_id)
                       VALUES (?, ?, ?, ?)""",
                    (date.today().isoformat(), "ASIGNAR", rut, id_proyecto),
                )
        except sqlite3.IntegrityError as error:
            raise ErrorDeDominio(
                "No se pudo asignar: el empleado o el proyecto no existe, "
                "o el empleado ya estaba asignado"
            ) from error

    def contar_asignaciones(self):
        with transaccion() as conn:
            return conn.execute(
                "SELECT COUNT(*) FROM empleado_proyecto"
            ).fetchone()[0]

    def contar_bitacora(self):
        with transaccion() as conn:
            return conn.execute("SELECT COUNT(*) FROM bitacora").fetchone()[0]