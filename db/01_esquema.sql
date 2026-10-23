CREATE TABLE IF NOT EXISTS departamento (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS empleado (
    rut              TEXT PRIMARY KEY,
    nombre           TEXT NOT NULL,
    telefono         TEXT,
    email            TEXT NOT NULL UNIQUE,
    fecha_ingreso    DATE NOT NULL,
    sueldo_base      INTEGER NOT NULL CHECK (sueldo_base > 0),
    contrasena_hash  TEXT NOT NULL,
    activo           INTEGER NOT NULL DEFAULT 1,
    departamento_id  INTEGER,
    FOREIGN KEY (departamento_id) REFERENCES departamento(id)
);