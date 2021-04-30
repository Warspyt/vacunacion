import afiliacion
import lote_vacunas


def menuafi():
    while True:
        # Mostramos el menu
        print('\nA D M I N I S T R A R  A F I L I A D O S')
        print("\t1 - Crear Afiliado")
        print("\t2 - Vacunar Afiliado")
        print("\t3 - Consultar Afiliado")
        print("\t4 - Cancelar Afiliacion")
        print("\t5 - Regresar Al Menu Principal")
        option = input("Seleccione una opcion: ")
        if option == '1':
            print('\n')
            con = afiliacion.sql_afiliado()
            afiliado = afiliacion.leer_info()
            afiliacion.insertar_tabla(con, afiliado)
            con.close()
        elif option == "2":
            # Aca se se vacuna a la gente
            con = afiliacion.sql_afiliado()
            afiliacion.vacunar(con)
            con.close()
        elif option == "3":
            # Aca se consulta el afiliado
            con = afiliacion.sql_afiliado()
            afiliacion.consulta(con)
            con.close()
        elif option == "4":
            # Aca se desafilia el afiliado y queda con la fecha del momento  de la desafiliacion
            con = afiliacion.sql_afiliado()
            afiliacion.desafiliar(con)
            con.close()
        elif option == "5":
            return
        else:
            print("")
            input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")


def menulote():
    while True:
        # Mostramos el menu
        print('\nA D M I N I S T R A R  V A C U N A S')
        print("\t1 - Crear lotes")
        print("\t2 - Consultar Lote")
        print("\t3 - Regresar Al Menu Principal")
        option = input("Seleccione una opcion: ")
        if option == "1":
            # Aca se crea el lote
            convacunas = lote_vacunas.sql_lotevacunas()
            lote_vacunas.tabla_vacunas(convacunas)
            lote = lote_vacunas.info_lote()
            lote_vacunas.crear_lote(convacunas, lote)
            convacunas.close()
        elif option == "2":
            # Aca se consulta el lote
            convacunas = lote_vacunas.sql_lotevacunas()
            lote_vacunas.consultar_lote(convacunas)
            convacunas.close()
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
    while True:
        print('\nS I S T E M A   D E   G E S T I Ó N   D E   V A C U N A C I Ó N ')
        print("Selecciona una opción:")
        print("\t1 - Administrar Afiliados")
        print("\t2 - Administrar Vacunas")
        print("\t3 - Plan Vacunacion")
        print("\t4 - salir")

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
