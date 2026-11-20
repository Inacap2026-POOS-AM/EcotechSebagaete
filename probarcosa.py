import os
from api_cliente import ApiCliente
from infraestructura.conexion import transaccion
from servicios_externos import DeserializadorExterno, GestorServiciosExternos

def asegurar_tablas_u3():
    with transaccion() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS consulta_clima (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                ciudad          TEXT NOT NULL,
                temperatura_c   REAL NOT NULL,
                estado_clima    TEXT NOT NULL,
                humedad_pct     REAL NOT NULL,
                obtenido_en     TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tipo_cambio (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                moneda_base     TEXT NOT NULL,
                moneda_destino  TEXT NOT NULL,
                tasa            REAL NOT NULL,
                obtenido_en     TEXT NOT NULL
            )
        """)

if __name__ == "__main__":
    os.environ["DB_NOMBRE"] = "fa.db"
    asegurar_tablas_u3()

    cliente = ApiCliente(timeout=10.0, max_reintentos=3, base_backoff=0.5)
    gestor = GestorServiciosExternos(cliente, DeserializadorExterno())

    clima = gestor.obtener_clima("Santiago", -33.4489, -70.6693)
    print("Guardado real (desde_cache debería ser False):", clima)

    cambio = gestor.obtener_tipo_cambio("USD", "EUR")
    print("Guardado real (desde_cache debería ser False):", cambio)