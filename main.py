""" Se importan los dintintos modulos que componene nuestro programa"""
import sqlite3
from sqlite3 import Error
import afiliacion as af
import lote_vacunas as lv
import plan_vacunacion as pl
import ProgramacionVacunas as prgva

"""cada modulo tiene su propio menu, afiliacion, lote de vacunas,vacunacion y programacion vacunacion"""
class conexion:
    def __init__(self):
        pass
    
    def sql_conexion(self):
        """ Se crea la conexion a la base de datos usando el metodo connect, creando el archivo en caso de que no exista y se verifica que
            no ocurra ningun error a partir de un try - except"""
        try:
            con = sqlite3.connect('sisgenvac.db')
            return con
        except Error:
            print(Error)

class menu(conexion):
    def __init__(self):
        pass
    
    def menuafi(self):
        """Por medio de un bucle se verifica  la opcion seleccionada y en caso de no elegir una valida se le informara """
        while True:
            # Mostramos el menu
            print('\nA D M I N I S T R A R  A F I L I A D O S')
            print("\t1 - Crear Afiliado")
            print("\t2 - Vacunar Afiliado")
            print("\t3 - Consultar Afiliado")
            print("\t4 - Desafiliar Usuario")
            print("\t5 - Regresar Al Menu Principal")
            option = input("Seleccione una opcion: ")
            if option == '1':
                print('\n')
                afiliado = afi.leer_info()
                afi.insertar_tabla(con, afiliado)
            elif option == "2":
                # Aca se se vacuna a la gente
                afi.vacunar(con)
            elif option == "3":
                # Aca se consulta el afiliado
                afi.consulta(con)
            elif option == "4":
                # Aca se desafilia el afiliado y queda con la fecha del momento
                afi.desafiliar(con)
            elif option == "5":
                return
            else:
                print("")
                input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")


    def menulote(self):
        while True:
            """Por medio de un bucle se verifica  la opcion seleccionada y en caso de no elegir una valida se le informara """
            # Mostramos el menu
            print('\nA D M I N I S T R A R  V A C U N A S')
            print("\t1 - Crear lotes")
            print("\t2 - Consultar Lote")
            print("\t3 - Regresar Al Menu Principal")
            option = input("Seleccione una opcion: ")
            if option == "1":
                # Aca se crea el lote
                lote = lt.info_lote()
                lt.crear_lote(lote)
            elif option == "2":
                # Aca se consulta el lote
                lt.consultar_lote()
            elif option == "3":
                return
            else:
                input("\nNo has pulsado ninguna opción correcta...\npulsa una tecla para continuar")


    def menuvac(self):
        while True:
            """Por medio de un bucle se verifica  la opcion seleccionada y en caso de no elegir una valida se le informara """
            # Mostramos el menu
            print('\nP L A N  V A C U N A C I O N')
            print("\t1 - Crear Plan")
            print("\t2 - Consultar Plan")
            print("\t3 - Regresar Al Menu Principal")
            option = input("Seleccione una opcion: ")
            if option == '1':
                # Aca se crea el plan
                plv.recibirPlan()
            elif option == '2':
                # Aca se consulta el plan
                plv.consultaplan()
            elif option == "3":
                return
            else:
                input("\nNo has pulsado ninguna opción correcta...\npulsa una tecla para continuar")


    def provac(self):
        while True:
            # Mostramos el menu
            """Por medio de un bucle se verifica  la opcion seleccionada y en caso de no elegir una valida se le informara """
            print('\nP R O G R A M A  V A C U N A C I O N')
            print("\t1 - Crear Programacion")
            print("\t2 - Consultar Agenda")
            print("\t3 - Consulta Individual")
            print("\t4 - Regresar Al Menu Principal")
            option = input("Seleccione una opcion: ")
            if option == '1':
                # Aca se crea la agendacion de citas
                prg.infoCita()

            elif option == '2':
                # Aca se consulta la agenda completa
                prg.agenda()
                
            elif option == "3":
                # Aca se consulta la cita por identificacion del afiliado
                prg.consulta_individual()
            elif option == "4":
                return
            else:
                input("\nNo has pulsado ninguna opción correcta...\npulsa una tecla para continuar")
                

    def mainmenu(self):
        """ Se crean todas las tablas necesarias de la base de datos para su
            manipulacion dentro del programa"""
        
        op = menu()
        
        global con
        global lt
        global prg
        global afi
        global plv
        
        con = op.sql_conexion()
        lt = lv.Lotes(con)
        prg = prgva.Agenda(con)
        afi = af.Afiliado()
        plv = pl.Plan(con)
        
        afi.tabla_afiliados(con)
        lt.tabla_vacunas()
        plv.tabla_plan()
        prg.tabla_prog()
        
        """
        este es el menu principal apartir de este  se despliegan los submenus de cada modulo
        """
        while True:
            print('\nS I S T E M A   D E   G E S T I Ó N   D E   V A C U N A C I Ó N ')
            print("Selecciona una opción:")
            print("\t1 - Administrar Afiliados")
            print("\t2 - Administrar Vacunas")
            print("\t3 - Plan Vacunacion")
            print("\t4 - Programa Vacunacion")
            print("\t5 - salir")

            # Mostramos el menu
            # solicituamos una opción al usuario
            opcionmenu = input("Seleccione una opcion:  ")

            if opcionmenu == "1":
                op.menuafi()
            elif opcionmenu == "2":
                op.menulote()
            elif opcionmenu == "3":
                op.menuvac()
            elif opcionmenu == "4":
                op.provac()
            elif opcionmenu == "5":
                con.close()
                break
            else:
                input("\nNo has pulsado ninguna opción correcta...\npulsa una tecla para continuar")

mn = menu()
mn.mainmenu()
