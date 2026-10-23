import hashlib

from dominio.excepciones import SueldoInvalido
from dominio.persona import Persona
from dominio.registro_tiempo import RegistroTiempo


class Empleado(Persona):
    """Empleado de EcoTech. Registra horas en proyectos."""

    def __init__(self, rut, nombre, telefono, email,
                 fecha_inicio_contrato, salario, contrasena_hash):
        super().__init__(nombre, telefono, email)
        self._rut = rut
        self._fecha_inicio_contrato = fecha_inicio_contrato
        self.set_salario(salario)
        self._contrasena_hash = contrasena_hash
        self._departamento = None
        self._proyectos = []
        self._registros = []

    def set_salario(self, nuevo_salario):
        if not isinstance(nuevo_salario, (int, float)) or nuevo_salario <= 0:
            raise SueldoInvalido("El salario debe ser un número positivo")
        self._salario = nuevo_salario

    def get_salario(self):
        return self._salario

    def get_rut(self):
        return self._rut

    def get_fecha_inicio_contrato(self):
        return self._fecha_inicio_contrato

    def get_contrasena_hash(self):
        return self._contrasena_hash

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
        return f"Empleado {self._rut}: {super().__str__()}"