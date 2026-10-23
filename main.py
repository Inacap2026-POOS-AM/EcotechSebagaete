from datetime import date

from dominio.departamento import Departamento
from dominio.empleado import Empleado
from dominio.proyecto import Proyecto
from dominio.registro_tiempo import RegistroTiempo

depto = Departamento("D-01", "Desarrollo Sostenible")
empleado = Empleado("E-01", "Sebastián Gaete", "+56911111111",
                    "sebastian@ecotech.cl", date(2024, 3, 1),
                    1000000.0, "hash_de_ejemplo")
proyecto = Proyecto("P-50", "Panel Solar", "Monitoreo de paneles",
                    date(2026, 3, 1))
registro = RegistroTiempo("R-01", date(2026, 10, 22), 4.5,
                          "Diseño de clases")

for objeto in (depto, empleado, proyecto, registro):
    print("Objeto creado:", type(objeto).__name__)

depto.agregar_empleado(empleado)
proyecto.asignar_empleado(empleado)
empleado.registrar_horas(date(2026, 10, 22), 4.5, "Diseño de clases")

print("Empleados en el departamento:", len(depto._empleados))
print("Empleados en el proyecto:", len(proyecto._empleados))
print("Registros del empleado:", len(empleado._registros))