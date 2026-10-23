import os
import sqlite3
from contextlib import contextmanager

from dotenv import load_dotenv

from dominio.excepciones import ServicioNoDisponible

load_dotenv()


def obtener_conexion():
    """Abre y retorna una conexión activa a SQLite."""
    ruta_bd = os.getenv("DB_NOMBRE", "ecotech.db")
    conn = sqlite3.connect(ruta_bd)
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