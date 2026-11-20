import re
from dataclasses import dataclass
from datetime import datetime, timezone
from infraestructura.conexion import transaccion
from dominio.excepciones import ErrorDeDominio, ServicioNoDisponible

try:
    import bcrypt
    _HAS_BCRYPT = True
except ImportError:
    _HAS_BCRYPT = False

try:
    from argon2 import PasswordHasher
    from argon2.exceptions import VerifyMismatchError
    _HAS_ARGON2 = True
except ImportError:
    _HAS_ARGON2 = False


PATRON_CIUDAD = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñüÜ\s\-\.]{2,60}$")
PATRON_MONEDA = re.compile(r"^[A-Z]{3}$")


def validar_ciudad(ciudad: str) -> str:
    if not isinstance(ciudad, str) or not ciudad.strip():
        raise ErrorDeDominio("Debe ingresar un nombre de ciudad válido.")
    limpia = " ".join(ciudad.strip().split())
    if not PATRON_CIUDAD.match(limpia):
        raise ErrorDeDominio("El nombre de ciudad contiene caracteres no permitidos.")
    return limpia


def validar_moneda(codigo: str) -> str:
    if not isinstance(codigo, str) or not codigo.strip():
        raise ErrorDeDominio("Debe ingresar un código de moneda (ej. USD, CLP, EUR).")
    limpio = codigo.strip().upper()
    if not PATRON_MONEDA.match(limpio):
        raise ErrorDeDominio("El código de moneda debe tener exactamente 3 letras (ISO 4217).")
    return limpio


def hashear_contrasena(password: str) -> str:
    if not isinstance(password, str) or len(password) < 8:
        raise ErrorDeDominio("La contraseña debe tener al menos 8 caracteres.")
    if _HAS_BCRYPT:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    if _HAS_ARGON2:
        return PasswordHasher().hash(password)
    raise ErrorDeDominio("Instale 'bcrypt' o 'argon2-cffi' para almacenar contraseñas con salt.")


def verificar_contrasena(password: str, hash_almacenado: str) -> bool:
    if not password or not hash_almacenado:
        return False
    if _HAS_BCRYPT and hash_almacenado.startswith(("$2a$", "$2b$", "$2y$")):
        return bcrypt.checkpw(password.encode("utf-8"), hash_almacenado.encode("utf-8"))
    if _HAS_ARGON2 and hash_almacenado.startswith("$argon2"):
        try:
            return PasswordHasher().verify(hash_almacenado, password)
        except VerifyMismatchError:
            return False
    return False


@dataclass(frozen=True)
class DatoClima:
    ciudad: str
    temperatura_c: float
    estado_clima: str
    humedad_pct: float
    obtenido_en: str
    desde_cache: bool = False


@dataclass(frozen=True)
class DatoTipoCambio:
    moneda_base: str
    moneda_destino: str
    tasa: float
    obtenido_en: str
    desde_cache: bool = False


class DeserializadorExterno:
    """Valida y convierte respuestas JSON externas en modelos del sistema."""

    @staticmethod
    def deserializar_clima(ciudad: str, payload: dict, obtenido_en: str) -> DatoClima:
        current = payload.get("current") or payload.get("main")
        if not isinstance(current, dict):
            raise ErrorDeDominio("Estructura JSON de clima incompleta.")

        # Soporta formato Open-Meteo ('temperature_2m', 'relative_humidity_2m', 'weather_code')
        if "temperature_2m" in current:
            temp = current.get("temperature_2m")
            hum = current.get("relative_humidity_2m", 0.0)
            codigo = current.get("weather_code", 0)
            estado = f"Código meteorológico {codigo}"
        else:
            temp = current.get("temp")
            hum = current.get("humidity", 0.0)
            weather_list = payload.get("weather") or []
            estado = (
                weather_list[0].get("description", "Sin descripción")
                if weather_list and isinstance(weather_list[0], dict)
                else "Sin descripción"
            )

        if not isinstance(temp, (int, float)) or not isinstance(hum, (int, float)):
            raise ErrorDeDominio("Valores numéricos inválidos en datos de clima.")

        return DatoClima(
            ciudad=ciudad,
            temperatura_c=float(temp),
            estado_clima=str(estado),
            humedad_pct=float(hum),
            obtenido_en=obtenido_en,
            desde_cache=False,
        )

    @staticmethod
    def deserializar_tipo_cambio(
        base: str, destino: str, payload: dict, obtenido_en: str
    ) -> DatoTipoCambio:
        rates = payload.get("rates")
        if not isinstance(rates, dict) or destino not in rates:
            raise ErrorDeDominio("No se encontró la tasa de cambio solicitada en la respuesta.")

        tasa = rates[destino]
        if not isinstance(tasa, (int, float)) or tasa <= 0:
            raise ErrorDeDominio("La tasa de cambio recibida no es válida.")

        return DatoTipoCambio(
            moneda_base=base,
            moneda_destino=destino,
            tasa=float(tasa),
            obtenido_en=obtenido_en,
            desde_cache=False,
        )


class GestorServiciosExternos:
    """Coordina consumo de APIs, persistencia parametrizada y Plan B local."""

    def __init__(self, cliente_api, deserializador: DeserializadorExterno | None = None):
        self._cliente = cliente_api
        self._deserializador = deserializador or DeserializadorExterno()

    def _guardar_clima_local(self, dato: DatoClima) -> None:
        with transaccion() as conn:
            conn.execute(
                """INSERT INTO consulta_clima
                   (ciudad, temperatura_c, estado_clima, humedad_pct, obtenido_en)
                   VALUES (?, ?, ?, ?, ?)""",
                (dato.ciudad, dato.temperatura_c, dato.estado_clima, dato.humedad_pct, dato.obtenido_en),
            )

    def _obtener_ultimo_clima_local(self, ciudad: str) -> DatoClima | None:
        with transaccion() as conn:
            fila = conn.execute(
                """SELECT ciudad, temperatura_c, estado_clima, humedad_pct, obtenido_en
                   FROM consulta_clima
                   WHERE LOWER(ciudad) = LOWER(?)
                   ORDER BY id DESC LIMIT 1""",
                (ciudad,),
            ).fetchone()
        if not fila:
            return None
        return DatoClima(
            ciudad=fila[0],
            temperatura_c=fila[1],
            estado_clima=fila[2],
            humedad_pct=fila[3],
            obtenido_en=fila[4],
            desde_cache=True,
        )

    def obtener_clima(self, ciudad: str, latitud: float, longitud: float) -> DatoClima:
        ciudad_valida = validar_ciudad(ciudad)
        ahora = datetime.now(timezone.utc).isoformat()
        try:
            payload = self._cliente.get_json(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": latitud,
                    "longitude": longitud,
                    "current": "temperature_2m,relative_humidity_2m,weather_code",
                },
            )
            dato = self._deserializador.deserializar_clima(ciudad_valida, payload, ahora)
            self._guardar_clima_local(dato)
            return dato
        except (ServicioNoDisponible, ErrorDeDominio):
            respaldo = self._obtener_ultimo_clima_local(ciudad_valida)
            if respaldo:
                return respaldo
            raise ServicioNoDisponible(
                f"Servicio de clima no disponible y sin datos locales previos para '{ciudad_valida}'."
            )

    def _guardar_tipo_cambio_local(self, dato: DatoTipoCambio) -> None:
        with transaccion() as conn:
            conn.execute(
                """INSERT INTO tipo_cambio
                   (moneda_base, moneda_destino, tasa, obtenido_en)
                   VALUES (?, ?, ?, ?)""",
                (dato.moneda_base, dato.moneda_destino, dato.tasa, dato.obtenido_en),
            )

    def _obtener_ultimo_tipo_cambio_local(self, base: str, destino: str) -> DatoTipoCambio | None:
        with transaccion() as conn:
            fila = conn.execute(
                """SELECT moneda_base, moneda_destino, tasa, obtenido_en
                   FROM tipo_cambio
                   WHERE moneda_base = ? AND moneda_destino = ?
                   ORDER BY id DESC LIMIT 1""",
                (base, destino),
            ).fetchone()
        if not fila:
            return None
        return DatoTipoCambio(
            moneda_base=fila[0],
            moneda_destino=fila[1],
            tasa=fila[2],
            obtenido_en=fila[3],
            desde_cache=True,
        )

    def obtener_tipo_cambio(self, moneda_base: str, moneda_destino: str) -> DatoTipoCambio:
        base = validar_moneda(moneda_base)
        destino = validar_moneda(moneda_destino)
        ahora = datetime.now(timezone.utc).isoformat()
        try:
            payload = self._cliente.get_json(
                "https://api.frankfurter.app/latest",
                params={"from": base, "to": destino},
            )
            dato = self._deserializador.deserializar_tipo_cambio(base, destino, payload, ahora)
            self._guardar_tipo_cambio_local(dato)
            return dato
        except (ServicioNoDisponible, ErrorDeDominio):
            respaldo = self._obtener_ultimo_tipo_cambio_local(base, destino)
            if respaldo:
                return respaldo
            raise ServicioNoDisponible(
                f"Servicio de tipo de cambio no disponible y sin respaldo local para {base}->{destino}."
            )