import hashlib
from datetime import date

from dominio.departamento import Departamento
from dominio.empleado import Empleado
from dominio.excepciones import ErrorDeDominio, RutDuplicado, SueldoInvalido
from dominio.proyecto import Proyecto
from inicializar_bd import base_de_demostracion
from repositorio.departamento_repositorio import DepartamentoRepositorio
from repositorio.empleado_repositorio import EmpleadoRepositorio
from repositorio.proyecto_repositorio import ProyectoRepositorio

base_de_demostracion()
deptos = DepartamentoRepositorio()
empleados = EmpleadoRepositorio()
proyectos = ProyectoRepositorio()
clave = hashlib.sha256("clave123".encode()).hexdigest()

print("=== CREAR ===")
operaciones = deptos.guardar(Departamento(None, "Operaciones"))
temporal = deptos.guardar(Departamento(None, "Temporal"))
print(operaciones)
print(temporal)
ana = Empleado("12345678-9", "Ana Rojas", "+56911111111",
               "ana@ecotech.cl", date(2024, 3, 1), 950000, clave)
empleados.guardar(ana, departamento_id=operaciones.get_id())
panel = proyectos.guardar(Proyecto(None, "Panel Solar",
                                   "Monitoreo de paneles",
                                   date(2026, 3, 1)))
print(panel)

print("=== LEER ===")
print(empleados.obtener("12345678-9"))
print(deptos.obtener(operaciones.get_id()))
print("Empleados:", len(empleados.listar()))
print("Departamentos:", len(deptos.listar()))

print("=== PRUEBA DE SEGURIDAD ' OR '1'='1 ===")
ataque = empleados.listar(nombre_contiene="' OR '1'='1")
print(f"Resultado ataque (empleados): {len(ataque)} registros")
ataque = deptos.listar(nombre_contiene="' OR '1'='1")
print(f"Resultado ataque (departamentos): {len(ataque)} registros")

print("=== ACTUALIZAR ===")
ana.set_salario(1050000)
print("Filas cambiadas:", empleados.actualizar(ana))
print("Salario guardado:", empleados.obtener("12345678-9").get_salario())
operaciones.set_nombre("Operaciones y Soporte")
print("Filas cambiadas:", deptos.actualizar(operaciones))

print("=== ERRORES DEL DOMINIO ===")
try:
    empleados.guardar(ana)
except RutDuplicado as error:
    print("RutDuplicado:", error)
try:
    ana.set_salario(-5)
except SueldoInvalido as error:
    print("SueldoInvalido:", error)
try:
    deptos.eliminar(operaciones.get_id())
except ErrorDeDominio as error:
    print("ErrorDeDominio:", error)
print("RUT inexistente:", empleados.obtener("00000000-0"))

print("=== TRANSACCIÓN: ASIGNAR + BITÁCORA ===")
proyectos.asignar_empleado("12345678-9", panel.get_id())
print("Asignaciones:", proyectos.contar_asignaciones(),
      "| Bitácora:", proyectos.contar_bitacora())
try:
    proyectos.asignar_empleado("12345678-9", panel.get_id())
except ErrorDeDominio as error:
    print("Asignación repetida:", error)
try:
    proyectos.asignar_empleado("12345678-9", 999)
except ErrorDeDominio as error:
    print("Proyecto inexistente:", error)
print("Asignaciones:", proyectos.contar_asignaciones(),
      "| Bitácora:", proyectos.contar_bitacora())

print("=== ELIMINAR ===")
print("Empleado archivado:", empleados.eliminar("12345678-9"))
print("Lo busco de nuevo:", empleados.obtener("12345678-9"))
print("Departamento eliminado:", deptos.eliminar(temporal.get_id()))
print("Lo busco de nuevo:", deptos.obtener(temporal.get_id()))