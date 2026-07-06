"""
clases.py

Contiene las clases del sistema de biblioteca.
"""

from datetime import datetime, timedelta

DIAS_PRESTAMO = 7
MULTA_POR_DIA = 100


class Libro:

    def __init__(self, isbn, titulo, autor, copias):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.copias_totales = copias
        self.copias_disponibles = copias
        self.veces_prestado = 0

    def disponible(self):
        return self.copias_disponibles > 0

    def prestar(self):
        self.copias_disponibles -= 1
        self.veces_prestado += 1

    def devolver(self):
        self.copias_disponibles += 1

    def __str__(self):
        return (
            f"ISBN: {self.isbn}\n"
            f"Título: {self.titulo}\n"
            f"Autor: {self.autor}\n"
            f"Disponibles: {self.copias_disponibles}/{self.copias_totales}"
        )


class Usuario:

    def __init__(self, dni, nombre):
        self.dni = dni
        self.nombre = nombre
        self.prestamos = []

    def __str__(self):
        return f"{self.nombre} - DNI {self.dni}"


class Prestamo:

    def __init__(self, usuario, libro):
        self.usuario = usuario
        self.libro = libro

        self.fecha_prestamo = datetime.now()
        self.fecha_limite = self.fecha_prestamo + timedelta(days=DIAS_PRESTAMO)
        self.fecha_devolucion = None

    def activo(self):
        return self.fecha_devolucion is None

    def devolver(self):
        self.fecha_devolucion = datetime.now()

    def multa(self):

        fecha = self.fecha_devolucion or datetime.now()

        atraso = (fecha - self.fecha_limite).days

        if atraso > 0:
            return atraso * MULTA_POR_DIA

        return 0

    def __str__(self):

        estado = "ACTIVO"

        if self.fecha_devolucion:
            estado = "DEVUELTO"

        return (
            f"{self.libro.titulo}\n"
            f"Usuario: {self.usuario.nombre}\n"
            f"Estado: {estado}\n"
            f"Fecha límite: {self.fecha_limite.strftime('%d/%m/%Y')}"
        )