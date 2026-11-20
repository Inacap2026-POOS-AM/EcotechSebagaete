import os
import sqlite3
from contextlib import contextmanager
from dotenv import load_dotenv
from dominio.excepciones import ServicioNoDisponible

# El .env está en la carpeta raíz del proyecto (un nivel sobre "infraestructura")
RUTA_ENV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")

if not os.path.exists(RUTA_ENV):
    raise SystemExit(
        "Error: no se encontró el archivo .env. "
        "Copia .env.example a .env y completa los valores."
    )

load_dotenv(RUTA_ENV)


def leer_variable(nombre):
    """Lee una variable del entorno. Si falta, termina con un mensaje claro."""
    valor = os.getenv(nombre)
    if not valor:
        raise SystemExit(f"Error: falta la variable {nombre} en el archivo .env")
    return valor


def obtener_conexion():
    """Abre y retorna una conexión activa a SQLite."""
    motor = leer_variable("DB_MOTOR")
    if motor != "sqlite":
        raise SystemExit(f"Error: DB_MOTOR='{motor}' no está soportado (use sqlite)")
    conn = sqlite3.connect(leer_variable("DB_NOMBRE"))
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def transaccion():
    """Todo o nada: confirma si sale bien, deshace si falla, siempre cierra."""
    conn = obtener_conexion()
    try:
        yield conn
        conn.commit()
    except sqlite3.OperationalError as error:
        conn.rollback()
        if "locked" in str(error).lower():
            raise ServicioNoDisponible(
                "La base está ocupada o bloqueada; reintenta en un momento"
            ) from error
        raise
    except Exception:
        conn.rollback()  # deshace todo y deja subir el error, no lo oculta
        raise
    finally:
        conn.close()
