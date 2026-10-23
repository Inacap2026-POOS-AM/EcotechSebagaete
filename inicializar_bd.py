from infraestructura.conexion import obtener_conexion


def inicializar():
    conn = obtener_conexion()
    try:
        with open("db/01_esquema.sql", encoding="utf-8") as archivo:
            conn.executescript(archivo.read())
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    inicializar()
    print("Esquema aplicado correctamente.")