CREATE TABLE IF NOT EXISTS consulta_clima (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    ciudad          TEXT NOT NULL,
    temperatura_c   REAL NOT NULL,
    estado_clima    TEXT NOT NULL,
    humedad_pct     REAL NOT NULL,
    obtenido_en     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tipo_cambio (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    moneda_base     TEXT NOT NULL,
    moneda_destino  TEXT NOT NULL,
    tasa            REAL NOT NULL,
    obtenido_en     TEXT NOT NULL
);