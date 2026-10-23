import os

from infraestructura.conexion import obtener_conexion


def inicializar():
    conn = obtener_conexion()
    try:
        with open("db/01_esquema.sql", encoding="utf-8") as archivo:
            conn.executescript(archivo.read())
        conn.commit()
    finally:
        conn.close()


def base_de_demostracion(nombre="demo.db"):
    """Apunta a una base desechable y limpia, sin tocar ecotech.db."""
    os.environ["DB_NOMBRE"] = nombre
    if os.path.exists(nombre):
        os.remove(nombre)
    inicializar()


if __name__ == "__main__":
    inicializar()
    print("Esquema aplicado correctamente.")