# ============================================================
# main.py
# Este es el archivo PRINCIPAL del programa. Es el que hay que
# ejecutar para correr el sistema de biblioteca.
# Se encarga de mostrar el menú y llamar a las funciones que
# están definidas en operaciones.py.
# ============================================================

import operaciones   # importamos el archivo con las operaciones de la biblioteca


def mostrar_menu():
    """
    Muestra las opciones disponibles del sistema por consola.
    Tenerla en una función aparte facilita reutilizarla o
    modificarla sin tocar el resto del programa.
    """
    print("\n===== SISTEMA DE BIBLIOTECA =====")
    print("1. Registrar libro")
    print("2. Registrar usuario")
    print("3. Prestar libro")
    print("4. Devolver libro")
    print("5. Listar libros")
    print("6. Listar préstamos activos")
    print("7. Ver libros más solicitados")
    print("8. Ver cantidad total de préstamos")
    print("9. Salir")


def main():
    """
    Función principal del programa. Muestra el menú dentro de
    un bucle repetitivo (while) hasta que el usuario elige
    salir, y ejecuta la función correspondiente según la
    opción elegida.
    """
    print("Bienvenido/a al Sistema de Biblioteca")

    # Bucle infinito controlado (estructura repetitiva) que se
    # repite hasta que el usuario elige la opción de salir (9).
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")   # dato ingresado por el usuario

        # Estructura condicional que decide qué función ejecutar
        # según la opción elegida por el usuario.
        if opcion == "1":
            operaciones.registrar_libro()

        elif opcion == "2":
            operaciones.registrar_usuario()

        elif opcion == "3":
            operaciones.prestar_libro()

        elif opcion == "4":
            operaciones.devolver_libro()

        elif opcion == "5":
            operaciones.listar_libros()

        elif opcion == "6":
            operaciones.listar_prestamos_activos()

        elif opcion == "7":
            operaciones.libros_mas_solicitados()

        elif opcion == "8":
            operaciones.cantidad_prestamos_realizados()

        elif opcion == "9":
            print("¡Hasta luego!")
            break   # corta el bucle while y termina el programa

        else:
            # Manejo de error para opciones no válidas del menú.
            print("⚠ Opción inválida. Por favor, elija una opción del 1 al 9.")


# Esto asegura que main() se ejecute solo cuando corremos este
# archivo directamente (y no si lo importáramos desde otro lado).
if __name__ == "__main__":
    main()
