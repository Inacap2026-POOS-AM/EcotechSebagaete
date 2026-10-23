from dominio.persona import Persona
from dominio.registro_tiempo import RegistroTiempo


class Empleado(Persona):
    """Empleado de EcoTech. Registra horas en proyectos."""

    def __init__(self, id_empleado, nombre, telefono, email,
                 fecha_inicio_contrato, salario, contrasena_hash):
        super().__init__(nombre, telefono, email)
        self._id_empleado = id_empleado
        self._fecha_inicio_contrato = fecha_inicio_contrato
        self._salario = salario
        self._contrasena_hash = contrasena_hash
        self._departamento = None   # 0..1 -> puede ser None
        self._proyectos = []        # 0..* -> lista
        self._registros = []        # 0..* -> lista

    def autenticar(self, contrasena):
        pass

    def registrar_horas(self, fecha, horas, descripcion):
        registro = RegistroTiempo(f"R-{len(self._registros) + 1}",
                                  fecha, horas, descripcion)
        self._registros.append(registro)
        return registro

    def get_salario(self):
        pass

    def set_salario(self, nuevo_salario):
        pass