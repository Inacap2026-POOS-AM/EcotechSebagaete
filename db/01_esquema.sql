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

CREATE TABLE IF NOT EXISTS proyecto (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre        TEXT NOT NULL,
    descripcion   TEXT,
    fecha_inicio  DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS empleado_proyecto (
    empleado_rut  TEXT NOT NULL,
    proyecto_id   INTEGER NOT NULL,
    PRIMARY KEY (empleado_rut, proyecto_id),
    FOREIGN KEY (empleado_rut) REFERENCES empleado(rut) ON DELETE CASCADE,
    FOREIGN KEY (proyecto_id)  REFERENCES proyecto(id)  ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS bitacora (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha         DATE NOT NULL,
    accion        TEXT NOT NULL,
    empleado_rut  TEXT NOT NULL,
    proyecto_id   INTEGER NOT NULL,
    FOREIGN KEY (empleado_rut) REFERENCES empleado(rut),
    FOREIGN KEY (proyecto_id)  REFERENCES proyecto(id)
);