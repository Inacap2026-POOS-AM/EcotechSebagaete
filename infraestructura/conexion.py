import os
import sqlite3
from contextlib import contextmanager

from dotenv import load_dotenv

load_dotenv()


def obtener_conexion():
    """Abre y retorna una conexión activa a SQLite."""
    ruta_bd = os.getenv("DB_NOMBRE", "ecotech.db")
    conn = sqlite3.connect(ruta_bd)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def transaccion():
    """Confirma si todo sale bien, deshace si falla y siempre cierra."""
    conn = obtener_conexion()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()