import afiliacion


def menuafi():
    while True:
        # Mostramos el menu
        print('\nA D M I N I S T R A R  A F I L I A D O S')
        print("\t1 - Crear Afiliado")
        print("\t2 - Actualizar Afiliado")
        print("\t3 - Consultar Afiliado")
        print("\t4 - Regresar Al Menu Principal")
        option = input("Seleccione una opcion: ")
        if option == '1':
            print('\n')

            afiliado = afiliacion.leer_info()
            con = afiliacion.sql_connection()
            afiliacion.insertar_tabla(con, afiliado)
        elif option == "4":
            return
        else:
            print("")
            input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")


def menulote():
    while True:
        # Mostramos el menu
        print('\nA D M I N I S T R A R  L O T E S  D E  V A C U N A S')
        print("\t1 - Crear lotes")
        print("\t2 - Consultar Lote")
        print("\t3 - Regresar Al Menu Principal")
        option = input("Seleccione una opcion: ")
        if option == '1':
            print("aca se crea el lote")
        elif option == '1':
            print("aca se consulta el lote")
        elif option == "3":
            return
        else:
            print("")
            input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")


def menuvac():
    while True:
        # Mostramos el menu
        print('\nP L A N  V A C U N A C I O N')
        print("\t1 - Crear Plan")
        print("\t2 - Consultar Plan")
        print("\t3 - Regresar Al Menu Principal")
        option = input("Seleccione una opcion: ")
        if option == '1':
            print("aca se crea el plan")
        elif option == '1':
            print("aca se consulta el plan")
        elif option == "3":
            return
        else:
            print("")
            input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")


def mainmenu():
    """
    Función que limpia la pantalla y muestra nuevamente el menu
    """
    print('\nS I S T E M A   D E   G E S T I Ó N   D E   V A C U N A C I Ó N ')
    print("Selecciona una opción:")
    print("\t1 - Administrar Afiliados")
    print("\t2 - Administrar Vacunas")
    print("\t3 - Plan Vacunacion")
    print("\t4 - salir")

    while True:
        # Mostramos el menu

        # solicituamos una opción al usuario
        opcionmenu = input("Seleccione una opcion:  ")

        if opcionmenu == "1":
            menuafi()
        elif opcionmenu == "2":
            menulote()
        elif opcionmenu == "3":
            menuvac()
        elif opcionmenu == "4":
            break
        else:
            print("")
            input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")


mainmenu()
