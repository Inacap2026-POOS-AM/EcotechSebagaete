class ErrorDeDominio(Exception):
    """Base de los errores que habla el negocio, no la base de datos."""


class SueldoInvalido(ErrorDeDominio, ValueError):
    """El sueldo no cumple la regla del negocio."""


class RutDuplicado(ErrorDeDominio):
    """Ya existe un empleado con ese RUT."""


class ServicioNoDisponible(ErrorDeDominio):
    """La base de datos no responde o está bloqueada."""