from dominio.departamento import Departamento
from infraestructura.conexion import transaccion


class DepartamentoRepositorio:
    """CRUD de departamentos. Recibe y devuelve objetos del dominio."""

    @staticmethod
    def _fila_a_departamento(fila):
        return Departamento(fila[0], fila[1])

    def guardar(self, departamento):
        with transaccion() as conn:
            cursor = conn.execute(
                "INSERT INTO departamento (nombre) VALUES (?)",
                (departamento.get_nombre(),),
            )
            departamento.set_id(cursor.lastrowid)
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
                (f"%{nombre_contiene}%",),  # solo arma el dato, no el SQL
            ).fetchall()
        return [self._fila_a_departamento(f) for f in filas]

    def actualizar(self, departamento):
        with transaccion() as conn:
            cursor = conn.execute(
                "UPDATE departamento SET nombre = ? WHERE id = ?",
                (departamento.get_nombre(), departamento.get_id()),
            )
        return cursor.rowcount

    def eliminar(self, id_departamento):
        """Borrado físico. La base lo rechaza si aún tiene empleados."""
        with transaccion() as conn:
            cursor = conn.execute(
                "DELETE FROM departamento WHERE id = ?",
                (id_departamento,),
            )
        return cursor.rowcount > 0