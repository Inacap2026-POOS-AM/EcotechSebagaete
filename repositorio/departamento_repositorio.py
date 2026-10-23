import sqlite3

from dominio.departamento import Departamento
from dominio.excepciones import ErrorDeDominio
from infraestructura.conexion import transaccion


class DepartamentoRepositorio:
    """CRUD de departamentos. Recibe y devuelve objetos del dominio."""

    @staticmethod
    def _fila_a_departamento(fila):
        return Departamento(fila[0], fila[1])

    def guardar(self, departamento):
        try:
            with transaccion() as conn:
                cursor = conn.execute(
                    "INSERT INTO departamento (nombre) VALUES (?)",
                    (departamento.get_nombre(),),
                )
                departamento.set_id(cursor.lastrowid)
        except sqlite3.IntegrityError as error:
            raise ErrorDeDominio(
                "Ya existe un departamento con ese nombre"
            ) from error
        return departamento

    def obtener(self, id_departamento):
        with transaccion() as conn:
            fila = conn.execute(
                "SELECT id, nombre FROM departamento WHERE id = ?",
                (id_departamento,),
            ).fetchone()
        return self._fila_a_departamento(fila) if fila else None

    def listar(self, nombre_contiene=""):
        with transaccion() as conn:
            filas = conn.execute(
                """SELECT id, nombre FROM departamento
                   WHERE nombre LIKE ? ORDER BY nombre""",
                (f"%{nombre_contiene}%",),  # arma el dato, no el SQL
            ).fetchall()
        return [self._fila_a_departamento(f) for f in filas]

    def actualizar(self, departamento):
        try:
            with transaccion() as conn:
                cursor = conn.execute(
                    "UPDATE departamento SET nombre = ? WHERE id = ?",
                    (departamento.get_nombre(), departamento.get_id()),
                )
        except sqlite3.IntegrityError as error:
            raise ErrorDeDominio(
                "Ya existe un departamento con ese nombre"
            ) from error
        return cursor.rowcount

    def eliminar(self, id_departamento):
        """Borrado físico. Se rechaza si aún tiene empleados."""
        try:
            with transaccion() as conn:
                cursor = conn.execute(
                    "DELETE FROM departamento WHERE id = ?",
                    (id_departamento,),
                )
        except sqlite3.IntegrityError as error:
            raise ErrorDeDominio(
                "No se puede eliminar: el departamento aún tiene empleados"
            ) from error
        return cursor.rowcount > 0