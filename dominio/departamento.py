class Departamento:
    """Unidad administrativa de EcoTech y su personal."""

    def __init__(self, id_departamento, nombre):
        self._id_departamento = id_departamento
        self._nombre = nombre
        self._gerente = None    # 0..1 -> puede ser None
        self._empleados = []    # 0..* -> lista

    def asignar_gerente(self, empleado):
        self._gerente = empleado

    def agregar_empleado(self, empleado):
        if empleado not in self._empleados:
            self._empleados.append(empleado)
            empleado._departamento = self

    def eliminar_empleado(self, id_empleado):
        for empleado in self._empleados:
            if empleado._id_empleado == id_empleado:
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