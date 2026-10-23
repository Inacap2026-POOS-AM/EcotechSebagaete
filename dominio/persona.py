class Persona:
    """Datos de identificación general de una persona en el sistema."""

    def __init__(self, nombre, telefono, email):
        self._nombre = nombre
        self._telefono = telefono
        self.set_email(email)

    def set_email(self, valor):
        if "@" not in valor:
            raise ValueError("El email debe contener '@'")
        self._email = valor

    def get_email(self):
        return self._email

    def get_nombre(self):
        return self._nombre

    def get_telefono(self):
        return self._telefono

    def __str__(self):
        return f"{self._nombre} <{self._email}>"