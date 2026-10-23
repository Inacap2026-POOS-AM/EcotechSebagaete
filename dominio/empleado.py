import hashlib

from dominio.persona import Persona
from dominio.registro_tiempo import RegistroTiempo


class Empleado(Persona):
    """Empleado de EcoTech. Registra horas en proyectos."""

    def __init__(self, id_empleado, nombre, telefono, email,
                 fecha_inicio_contrato, salario, contrasena_hash):
        super().__init__(nombre, telefono, email)
        self._id_empleado = id_empleado
        self._fecha_inicio_contrato = fecha_inicio_contrato
        self.set_salario(salario)
        self._contrasena_hash = contrasena_hash
        self._departamento = None   # 0..1 -> puede ser None
        self._proyectos = []        # 0..* -> lista
        self._registros = []        # 0..* -> lista

    def set_salario(self, nuevo_salario):
        if nuevo_salario <= 0:
            raise ValueError("El salario debe ser positivo")
        self._salario = nuevo_salario

    def get_salario(self):
        return self._salario

    def autenticar(self, contrasena):
        hash_ingresado = hashlib.sha256(contrasena.encode()).hexdigest()
        return hash_ingresado == self._contrasena_hash

    def registrar_horas(self, proyecto, fecha, horas, descripcion):
        registro = RegistroTiempo(f"R-{len(self._registros) + 1}",
                                  fecha, horas, descripcion)
        self._registros.append(registro)
        proyecto._registros.append(registro)

    def total_horas(self):
        return sum(r.get_cantidad_horas() for r in self._registros)

    def __str__(self):
        return f"Empleado {self._id_empleado}: {super().__str__()}"