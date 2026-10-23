import hashlib
import os
import sqlite3
from datetime import date

from dominio.departamento import Departamento
from dominio.empleado import Empleado
from inicializar_bd import inicializar
from repositorio.departamento_repositorio import DepartamentoRepositorio
from repositorio.empleado_repositorio import EmpleadoRepositorio

ruta_bd = os.getenv("DB_NOMBRE", "ecotech.db")
if os.path.exists(ruta_bd):
    os.remove(ruta_bd)
inicializar()

deptos = DepartamentoRepositorio()
empleados = EmpleadoRepositorio()
clave = hashlib.sha256("clave123".encode()).hexdigest()

print("=== CREAR ===")
operaciones = deptos.guardar(Departamento(None, "Operaciones"))
print(operaciones)
temporal = deptos.guardar(Departamento(None, "Temporal"))
print(temporal)
ana = Empleado("12345678-9", "Ana Rojas", "+56911111111",
               "ana@ecotech.cl", date(2024, 3, 1), 950000, clave)
empleados.guardar(ana, departamento_id=operaciones.get_id())

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

print("=== QUÉ PASA CUANDO ALGO FALLA ===")
try:
    empleados.guardar(ana)
except sqlite3.IntegrityError as error:
    print("RUT duplicado:", error)
try:
    deptos.eliminar(operaciones.get_id())
except sqlite3.IntegrityError as error:
    print("Borrar departamento con empleados:", error)
try:
    ana.set_salario(-5)
except ValueError as error:
    print("Salario inválido:", error)
print("RUT inexistente:", empleados.obtener("00000000-0"))

print("=== ELIMINAR ===")
print("Empleado archivado:", empleados.eliminar("12345678-9"))
print("Lo busco de nuevo:", empleados.obtener("12345678-9"))
print("Departamento eliminado:", deptos.eliminar(temporal.get_id()))
print("Lo busco de nuevo:", deptos.obtener(temporal.get_id()))