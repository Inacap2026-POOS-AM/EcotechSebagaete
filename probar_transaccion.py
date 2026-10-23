import hashlib
from datetime import date

from dominio.empleado import Empleado
from dominio.proyecto import Proyecto
from infraestructura.conexion import transaccion
from inicializar_bd import base_de_demostracion
from repositorio.empleado_repositorio import EmpleadoRepositorio
from repositorio.proyecto_repositorio import ProyectoRepositorio

base_de_demostracion("prueba_transaccion.db")
proyectos = ProyectoRepositorio()
clave = hashlib.sha256("clave123".encode()).hexdigest()
EmpleadoRepositorio().guardar(
    Empleado("12345678-9", "Ana Rojas", "+56911111111", "ana@ecotech.cl",
             date(2024, 3, 1), 950000, clave))
panel = proyectos.guardar(
    Proyecto(None, "Panel Solar", "Monitoreo", date(2026, 3, 1)))

print("--- Se corta la luz entre las dos escrituras ---")
try:
    with transaccion() as conn:
        conn.execute(
            "INSERT INTO empleado_proyecto (empleado_rut, proyecto_id) "
            "VALUES (?, ?)",
            ("12345678-9", panel.get_id()),
        )
        raise RuntimeError("fallo simulado")
except RuntimeError as error:
    print("Falló:", error)
print("Asignaciones:", proyectos.contar_asignaciones(),
      "(esperado 0: el rollback deshizo la primera escritura)")

print("--- Sin fallos ---")
proyectos.asignar_empleado("12345678-9", panel.get_id())
print("Asignaciones:", proyectos.contar_asignaciones(),
      "| Bitácora:", proyectos.contar_bitacora(), "(esperado 1 y 1)")