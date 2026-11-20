import time
import requests
from dominio.excepciones import ErrorDeDominio, ServicioNoDisponible


class ApiCliente:
    """Cliente HTTP resiliente con timeout explícito, backoff y manejo de códigos."""

    def __init__(self, timeout: float = 8.0, max_reintentos: int = 3, base_backoff: float = 0.5):
        if timeout <= 0:
            raise ValueError("El timeout debe ser mayor a 0 segundos.")
        if not 1 <= max_reintentos <= 4:
            raise ValueError("Los reintentos deben estar entre 1 y 4.")
        self._timeout = timeout
        self._max_reintentos = max_reintentos
        self._base_backoff = base_backoff
        self._session = requests.Session()

    def _calcular_espera(self, intento: int, respuesta: requests.Response | None = None) -> float:
        if respuesta is not None and respuesta.status_code == 429:
            retry_after = respuesta.headers.get("Retry-After")
            if retry_after:
                try:
                    segundos = float(retry_after)
                    if segundos >= 0:
                        return min(segundos, 30.0)
                except ValueError:
                    pass
        return self._base_backoff * (2 ** intento)

    def get_json(self, url: str, params: dict | None = None) -> dict:
        if not url.startswith("https://"):
            raise ErrorDeDominio("Solo se permiten conexiones HTTPS hacia servicios externos.")

        ultimo_motivo = "Error de comunicación con el servicio externo."

        for intento in range(self._max_reintentos + 1):
            try:
                resp = self._session.get(url, params=params, timeout=self._timeout)

                if 200 <= resp.status_code < 300:
                    try:
                        data = resp.json()
                    except ValueError as exc:
                        raise ErrorDeDominio("La respuesta del servicio externo no es un JSON válido.") from exc
                    if not isinstance(data, dict):
                        raise ErrorDeDominio("Formato JSON inesperado en la respuesta externa.")
                    return data

                # 429: respetar Retry-After y reintentar si quedan intentos
                if resp.status_code == 429:
                    ultimo_motivo = "Límite de solicitudes alcanzado en el servicio externo (HTTP 429)."
                    if intento < self._max_reintentos:
                        time.sleep(self._calcular_espera(intento, resp))
                        continue
                    raise ServicioNoDisponible(ultimo_motivo)

                # Otros 4xx: error de cliente/solicitud, no se reintenta
                if 400 <= resp.status_code < 500:
                    raise ErrorDeDominio(f"Solicitud rechazada por el servicio externo (HTTP {resp.status_code}).")

                # 5xx: fallo temporal del servidor remoto, se reintenta
                if 500 <= resp.status_code < 600:
                    ultimo_motivo = f"Servicio externo no disponible temporalmente (HTTP {resp.status_code})."
                    if intento < self._max_reintentos:
                        time.sleep(self._calcular_espera(intento, resp))
                        continue
                    raise ServicioNoDisponible(ultimo_motivo)

            except requests.Timeout as exc:
                ultimo_motivo = "Tiempo de espera agotado al consultar el servicio externo."
                if intento < self._max_reintentos:
                    time.sleep(self._calcular_espera(intento))
                    continue
                raise ServicioNoDisponible(ultimo_motivo) from exc

            except requests.RequestException as exc:
                ultimo_motivo = "Error de red al intentar conectar con el servicio externo."
                if intento < self._max_reintentos:
                    time.sleep(self._calcular_espera(intento))
                    continue
                raise ServicioNoDisponible(ultimo_motivo) from exc

        raise ServicioNoDisponible(ultimo_motivo)