class Departamento:
    """Unidad administrativa de EcoTech y su personal."""

    def __init__(self, id_departamento, nombre):
        self._id_departamento = id_departamento
        self._nombre = nombre
        self._gerente = None
        self._empleados = []

    def get_id(self):
        return self._id_departamento

    def set_id(self, valor):
        self._id_departamento = valor

    def set_nombre(self, valor):
        if not valor.strip():
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = valor

    def asignar_gerente(self, empleado):
        self._gerente = empleado

    def agregar_empleado(self, empleado):
        if empleado not in self._empleados:
            self._empleados.append(empleado)
            empleado._departamento = self

    def eliminar_empleado(self, rut):
        for empleado in self._empleados:
            if empleado.get_rut() == rut:
                self._empleados.remove(empleado)
                empleado._departamento = None
                break

    def get_nombre(self):
        return self._nombre

    def cantidad_empleados(self):
        return len(self._empleados)

    def total_nomina(self):
        return sum(e.get_salario() for e in self._empleados)

    def __str__(self):
        return (f"Departamento {self._id_departamento}: {self._nombre} "
                f"({len(self._empleados)} empleados)")