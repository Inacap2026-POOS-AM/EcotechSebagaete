import hashlib
from datetime import date

from dominio.departamento import Departamento
from dominio.empleado import Empleado
from dominio.informe import Informe
from dominio.informe_dotacion import InformeDotacion
from dominio.informe_nomina import InformeNomina
from dominio.informe_proyecto import InformeProyecto
from dominio.persona import Persona
from dominio.proyecto import Proyecto

clave = hashlib.sha256("clave123".encode()).hexdigest()

depto = Departamento("D-01", "Desarrollo Sostenible")
empleado = Empleado("E-01", "Sebastián Gaete", "+56911111111",
                    "sebastian@ecotech.cl", date(2024, 3, 1),
                    1000000.0, clave)
proyecto = Proyecto("P-50", "Panel Solar", "Monitoreo de paneles",
                    date(2026, 3, 1))

depto.agregar_empleado(empleado)
proyecto.asignar_empleado(empleado)
empleado.registrar_horas(proyecto, date(2026, 10, 22), 4.5,
                         "Diseño de clases")

print("--- __str__ ---")
print(empleado)
print(depto)
print(proyecto)
print("Autenticación correcta:", empleado.autenticar("clave123"))

print("--- Validaciones ---")
try:
    empleado.set_salario(-5)
except ValueError as error:
    print("Salario inválido:", error)
try:
    empleado.registrar_horas(proyecto, date(2026, 10, 22), 30, "x")
except ValueError as error:
    print("Horas inválidas:", error)
try:
    Persona("Ana", "+5690000000", "correo-sin-arroba")
except ValueError as error:
    print("Email inválido:", error)

print("--- Clase abstracta ---")
try:
    Informe("I-00", "Prueba", date(2026, 10, 22))
except TypeError as error:
    print("No se puede instanciar:", error)

print("--- Polimorfismo ---")
hoy = date(2026, 10, 22)
informes = [
    InformeNomina("I-01", hoy, depto),
    InformeNomina("I-02", hoy, depto),
    InformeProyecto("I-03", hoy, proyecto),
    InformeDotacion("I-04", hoy, depto),
]
for informe in informes:
    print(informe)
    print("  ->", informe.exportar())