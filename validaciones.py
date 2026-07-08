# ============================================================
# validaciones.py
# Este archivo agrupa todas las funciones que se encargan de
# validar los datos que ingresa el usuario por teclado.
# Separarlas acá permite reutilizarlas desde cualquier parte
# del programa sin repetir código.
# ============================================================


def validar_numero_entero(texto):
    """
    Intenta convertir un texto ingresado por el usuario a un
    número entero (int).
    Si el usuario escribe algo que no es un número (por ejemplo
    letras), se produce un error 'ValueError' que capturamos con
    try/except para no romper el programa.
    Devuelve el número si es válido, o None si no lo es.
    """
    try:
        # Intentamos la conversión de texto a número entero.
        numero = int(texto)
        return numero
    except ValueError:
        # Si falla la conversión, devolvemos None como aviso de error.
        return None


def validar_entero_positivo(numero):
    """
    Verifica que el número sea válido (no None) y mayor a cero.
    Se usa, por ejemplo, para la cantidad de copias de un libro.
    """
    # Chequeamos primero que no sea None y después que sea mayor a 0.
    return numero is not None and numero > 0


def validar_libro_existe(diccionario_libros, isbn):
    """
    Chequea si el ISBN ingresado está registrado en el
    diccionario de libros.
    """
    return isbn in diccionario_libros


def validar_usuario_existe(diccionario_usuarios, dni):
    """
    Chequea si el DNI ingresado está registrado en el
    diccionario de usuarios.
    """
    return dni in diccionario_usuarios


def pedir_entero_positivo(mensaje):
    """
    Pide un número entero positivo al usuario y lo valida.
    Si el usuario ingresa un valor incorrecto, vuelve a
    preguntar hasta que sea válido. Esto evita que el
    programa se caiga por un dato mal ingresado.
    """
    while True:
        # input() siempre devuelve texto, por eso hay que validar.
        texto_ingresado = input(mensaje)
        numero = validar_numero_entero(texto_ingresado)

        if not validar_entero_positivo(numero):
            # Mensaje de error claro para el usuario.
            print("⚠ Dato inválido. Ingrese un número entero mayor a 0.")
        else:
            # Si el número es válido, salimos del bucle devolviéndolo.
            return numero


def validar_texto_no_vacio(texto):
    """
    Verifica que un texto ingresado (por ejemplo, nombre o
    título) no esté vacío ni tenga solo espacios.
    """
    return texto.strip() != ""
