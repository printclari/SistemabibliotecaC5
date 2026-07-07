# ============================================================
# datos.py
# Este archivo simula la "base de datos" del sistema de
# biblioteca. En un sistema real esta información vendría de
# una base de datos, pero para este trabajo la simulamos con
# diccionarios y listas guardados en memoria.
# ============================================================

# Diccionario principal de libros.
# La clave de afuera es el ISBN (código único del libro) y el
# valor es otro diccionario con los datos de ese libro.
libros = {
    "978-1": {
        "titulo": "Cien años de soledad",   # título del libro
        "autor": "Gabriel García Márquez",   # autor del libro
        "copias_totales": 2,                 # cantidad de copias que tiene la biblioteca
        "copias_disponibles": 2,             # cuántas copias están libres ahora mismo
        "veces_prestado": 0                  # contador: cuántas veces se prestó este libro
    },
    "978-2": {
        "titulo": "1984",
        "autor": "George Orwell",
        "copias_totales": 1,
        "copias_disponibles": 1,
        "veces_prestado": 0
    },
    "978-3": {
        "titulo": "El Principito",
        "autor": "Antoine de Saint-Exupéry",
        "copias_totales": 3,
        "copias_disponibles": 3,
        "veces_prestado": 0
    }
}

# Diccionario de usuarios registrados en la biblioteca.
# La clave es el DNI del usuario y el valor es su nombre.
usuarios = {
    "1001": "Ana Pérez",
    "1002": "Juan Gómez"
}

# Lista que funciona como "registro" de todos los préstamos
# realizados (activos e históricos). Cada elemento va a ser un
# diccionario con los datos de un préstamo puntual.
# Este es un ACUMULADOR de tipo lista.
prestamos = []

# Contador global de préstamos realizados (acumulador numérico,
# se usa para las estadísticas finales).
contador_prestamos = 0

# Cantidad de días que un usuario tiene para devolver un libro
# antes de que se le empiece a cobrar multa.
DIAS_PRESTAMO = 7

# Monto de multa que se cobra por cada día de atraso en la
# devolución (constante del sistema).
MULTA_POR_DIA = 100
