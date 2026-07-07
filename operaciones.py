# ============================================================
# operaciones.py
# Este archivo contiene las funciones que representan las
# operaciones reales de la biblioteca: registrar libros y
# usuarios, prestar y devolver libros, calcular multas y
# mostrar estadísticas.
# Cada función está modularizada (hace una sola cosa) para que
# el programa sea más fácil de leer, probar y corregir.
# ============================================================

from datetime import datetime, timedelta   # para trabajar con fechas de préstamo y devolución
import datos                                # importamos el archivo con los datos simulados
import validaciones                         # importamos las funciones de validación


def registrar_libro():
    """
    Da de alta un libro nuevo en el sistema, pidiendo ISBN,
    título, autor y cantidad de copias.
    """
    isbn = input("Ingrese el ISBN del libro: ")   # código único que identifica al libro

    # Controlamos que no exista ya un libro con ese ISBN (evita duplicados).
    if validaciones.validar_libro_existe(datos.libros, isbn):
        print("⚠ Error: ya existe un libro registrado con ese ISBN.")
        return   # cortamos la función acá si hay un error

    titulo = input("Ingrese el título del libro: ")   # texto ingresado por el usuario

    # Validamos que el título no esté vacío.
    if not validaciones.validar_texto_no_vacio(titulo):
        print("⚠ Error: el título no puede estar vacío.")
        return

    autor = input("Ingrese el autor del libro: ")   # texto ingresado por el usuario

    # Validamos que el autor no esté vacío.
    if not validaciones.validar_texto_no_vacio(autor):
        print("⚠ Error: el autor no puede estar vacío.")
        return

    # Pedimos la cantidad de copias usando la función ya validada.
    copias = validaciones.pedir_entero_positivo("Ingrese la cantidad de copias: ")

    # Damos de alta el libro nuevo dentro del diccionario "libros".
    datos.libros[isbn] = {
        "titulo": titulo,                # guardamos el título ingresado
        "autor": autor,                  # guardamos el autor ingresado
        "copias_totales": copias,        # cantidad total de copias
        "copias_disponibles": copias,    # al principio, todas las copias están disponibles
        "veces_prestado": 0              # todavía no se prestó ninguna vez
    }

    print(f"Libro '{titulo}' registrado con éxito ({copias} copia/s).")


def registrar_usuario():
    """
    Da de alta un usuario nuevo en el sistema, pidiendo DNI
    y nombre.
    """
    dni = input("Ingrese el DNI del usuario: ")   # dato ingresado por el usuario

    # Controlamos que no exista ya un usuario con ese DNI.
    if validaciones.validar_usuario_existe(datos.usuarios, dni):
        print("⚠ Error: ya existe un usuario registrado con ese DNI.")
        return

    nombre = input("Ingrese el nombre del usuario: ")   # dato ingresado por el usuario

    # Validamos que el nombre no esté vacío.
    if not validaciones.validar_texto_no_vacio(nombre):
        print("⚠ Error: el nombre no puede estar vacío.")
        return

    # Damos de alta el usuario nuevo dentro del diccionario "usuarios".
    datos.usuarios[dni] = nombre

    print(f"Usuario '{nombre}' registrado con éxito.")


def prestar_libro():
    """
    Registra el préstamo de un libro a un usuario, controlando
    que ambos existan y que haya copias disponibles.
    """
    isbn = input("Ingrese el ISBN del libro a prestar: ")   # dato ingresado

    # Validamos que el libro exista en el sistema.
    if not validaciones.validar_libro_existe(datos.libros, isbn):
        print("⚠ Error: no existe un libro con ese ISBN.")
        return

    dni = input("Ingrese el DNI del usuario: ")   # dato ingresado

    # Validamos que el usuario exista en el sistema.
    if not validaciones.validar_usuario_existe(datos.usuarios, dni):
        print("⚠ Error: no existe un usuario con ese DNI.")
        return

    libro = datos.libros[isbn]   # tomamos el libro para no repetir código

    # Controlamos que haya al menos una copia disponible.
    if libro["copias_disponibles"] <= 0:
        print(f"⚠ Error: no hay copias disponibles de '{libro['titulo']}'.")
        return

    # Calculamos las fechas del préstamo: hoy y la fecha límite de devolución.
    fecha_prestamo = datetime.now()
    fecha_limite = fecha_prestamo + timedelta(days=datos.DIAS_PRESTAMO)

    # Armamos el diccionario que representa este préstamo puntual.
    nuevo_prestamo = {
        "isbn": isbn,                        # libro prestado
        "dni": dni,                          # usuario que se lo lleva
        "fecha_prestamo": fecha_prestamo,     # fecha en que se realizó el préstamo
        "fecha_limite": fecha_limite,         # fecha límite antes de generar multa
        "fecha_devolucion": None              # todavía no se devolvió (None = sin devolver)
    }

    # Agregamos el préstamo nuevo a la lista general (acumulador de lista).
    datos.prestamos.append(nuevo_prestamo)

    # Descontamos una copia disponible del libro (acumulador que resta).
    libro["copias_disponibles"] -= 1

    # Sumamos 1 a la cantidad de veces que se prestó este libro.
    libro["veces_prestado"] += 1

    # Sumamos 1 al contador global de préstamos realizados.
    datos.contador_prestamos += 1

    print(f"Préstamo registrado: '{libro['titulo']}' -> {datos.usuarios[dni]} "
          f"(límite de devolución: {fecha_limite.strftime('%d/%m/%Y')}).")


def devolver_libro():
    """
    Registra la devolución de un libro, calcula la multa por
    demora si corresponde, y libera la copia del libro.
    """
    isbn = input("Ingrese el ISBN del libro a devolver: ")   # dato ingresado
    dni = input("Ingrese el DNI del usuario: ")               # dato ingresado

    # Buscamos, dentro de la lista de préstamos, uno que esté
    # activo (sin devolver todavía) para ese libro y ese usuario.
    prestamo_encontrado = None

    # Recorremos la lista de préstamos con un bucle for (estructura repetitiva).
    for prestamo in datos.prestamos:
        # Un préstamo "activo" es el que todavía no tiene fecha de devolución.
        if prestamo["isbn"] == isbn and prestamo["dni"] == dni and prestamo["fecha_devolucion"] is None:
            prestamo_encontrado = prestamo   # guardamos la referencia al préstamo
            break   # cortamos el bucle apenas lo encontramos

    # Si no se encontró ningún préstamo activo, avisamos el error.
    if prestamo_encontrado is None:
        print("⚠ Error: no se encontró un préstamo activo con esos datos.")
        return

    # Registramos la fecha real de devolución como el momento actual.
    prestamo_encontrado["fecha_devolucion"] = datetime.now()

    # Calculamos si corresponde multa por atraso.
    multa = calcular_multa(prestamo_encontrado)

    # Liberamos una copia del libro (vuelve a estar disponible).
    libro = datos.libros[isbn]
    libro["copias_disponibles"] += 1

    # Mostramos el resultado según haya multa o no.
    if multa > 0:
        print(f"Devolución registrada. Multa por atraso: ${multa}")
    else:
        print("Devolución registrada sin multa.")


def calcular_multa(prestamo):
    """
    Calcula la multa de un préstamo según los días de atraso.
    Si todavía no se devolvió, calcula la multa "hasta hoy".
    Devuelve 0 si no hay atraso.
    """
    # Si ya se devolvió, usamos esa fecha; si no, usamos la fecha actual.
    if prestamo["fecha_devolucion"] is not None:
        fecha_referencia = prestamo["fecha_devolucion"]
    else:
        fecha_referencia = datetime.now()

    # Calculamos la diferencia en días entre la fecha límite y la fecha de referencia.
    dias_atraso = (fecha_referencia - prestamo["fecha_limite"]).days

    # Si hay atraso (más de 0 días), calculamos la multa; si no, es 0.
    if dias_atraso > 0:
        return dias_atraso * datos.MULTA_POR_DIA
    else:
        return 0


def listar_libros():
    """
    Muestra por pantalla todos los libros registrados, con su
    disponibilidad actual.
    """
    print("\n--- LISTADO DE LIBROS ---")

    # Si no hay libros cargados, avisamos.
    if len(datos.libros) == 0:
        print("No hay libros registrados.")
        return

    # Recorremos el diccionario de libros con un bucle for.
    for isbn, libro in datos.libros.items():
        print(f"[{isbn}] {libro['titulo']} - {libro['autor']} "
              f"({libro['copias_disponibles']}/{libro['copias_totales']} disponibles)")


def listar_prestamos_activos():
    """
    Muestra todos los préstamos que todavía no fueron devueltos.
    """
    print("\n--- PRÉSTAMOS ACTIVOS ---")

    hay_activos = False   # bandera para saber si encontramos al menos uno

    # Recorremos toda la lista de préstamos.
    for prestamo in datos.prestamos:
        # Solo nos interesan los que no tienen fecha de devolución.
        if prestamo["fecha_devolucion"] is None:
            hay_activos = True
            libro = datos.libros[prestamo["isbn"]]
            nombre_usuario = datos.usuarios[prestamo["dni"]]
            fecha_limite_texto = prestamo["fecha_limite"].strftime('%d/%m/%Y')
            print(f"{libro['titulo']} -> {nombre_usuario} (límite: {fecha_limite_texto})")

    # Si no entramos nunca al if de arriba, no hay préstamos activos.
    if not hay_activos:
        print("No hay préstamos activos.")


def libros_mas_solicitados():
    """
    Muestra un ranking de los libros más prestados, usando el
    contador 'veces_prestado' de cada libro.
    """
    print("\n--- LIBROS MÁS SOLICITADOS ---")

    # Convertimos el diccionario de libros en una lista para poder ordenarla.
    lista_libros = list(datos.libros.values())

    # Ordenamos la lista de mayor a menor según "veces_prestado".
    lista_libros.sort(key=lambda libro: libro["veces_prestado"], reverse=True)

    # Mostramos cada libro de la lista ya ordenada.
    for libro in lista_libros:
        print(f"{libro['titulo']}: {libro['veces_prestado']} préstamo/s")


def cantidad_prestamos_realizados():
    """
    Muestra la cantidad total de préstamos realizados en el
    sistema (usa el contador acumulador).
    """
    print(f"\nCantidad total de préstamos realizados: {datos.contador_prestamos}")
