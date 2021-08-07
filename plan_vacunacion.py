""" Se importa el modulo de validaciones y las librerias sqlite 3 para el manejo y conexion
    de las bases de datos y datetime para el manejo, transformacion y extraccion de las de
    las fechas"""
import validaciones as vl
import sqlite3
from sqlite3 import Error
from datetime import datetime
from datetime import date

"""Clase para la creacion de un nuevo plan de vacunacion"""
class PlanVacunacion:
    """ Se guardan de manera privada todas las variables necesarias para crear una conexion o
        un nuevo plan de vacunacion y se crean las funciones set para cambiar su valor y get para
        extraerlo"""
    def __init__(self, con):
        self.__conexion = con
        self.__cursorObj = con.cursor()
        self.__emin = "informacion no disponible"
        self.__emax = "informacion no disponible"
        self.__fini = "informacion no disponible"
        self.__ffin = "informacion no disponible"

    """ Acceso privado a la conexion"""
    def getconexion(self):
        return self.__conexion

    """ Acceso privado al cursor de la db"""
    def getcursorObj(self):
        return self.__cursorObj

    """ Acceso privado a la edad minima"""
    def setemin(self, emin):
        self.__emin = emin

    def getemin(self):
        return self.__emin

    """ Acceso privado a la edad maxima"""
    def setemax(self, emax):
        self.__emax = emax

    def getemax(self):
        return self.__emax

    """ Acceso privado a la fecha de inicio"""
    def setfini(self, fini):
        self.__fini = fini

    def getfini(self):
        return self.__fini

    """ Acceso privado a la fecha de finalizacion"""
    def setffin(self, ffin):
        self.__ffin = ffin

    def getffin(self):
        return self.__ffin

"""Clase para la manipulacion del modulo de planes de vacunacion, que hereda de la clase PlanVacunacion
    y encapsula todas las funciones de manera privada"""
class Plan(PlanVacunacion):

    ''' Funcion para crear la tabla de los planes de vacunacion dentro de la base de datos del
        programa, la cual toma como parametro la conexion de la misma'''

    def __tabla_plan(self):

        """ Se crea una tabla para los planes de vacunacion verificando que no exista aun, haciendo uso del objeto cursor
            y el metodo execute que utiliza el CREATE TABLE dentro de los parametros"""

        self.getcursorObj().execute("""CREATE TABLE IF NOT EXISTS PlanVacunacion(idplan integer PRIMARY KEY AUTOINCREMENT, edadmin text,
                          edadmax text, fechainicioplan text, fechafinalplan text)""")
        self.getconexion().commit()


    ''' Funcion para consultar la informacion de los planes de vacunacion activos a la fecha,
        la cual toma como parametro la conexion con la base de datos del programa'''

    def __consultaplan(self):

        ''' Se extraen todos los planes de vacunacion de la base de datos del programa, con el objeto cursor y el
            metodo execute que utiliza el SELECT como parametro '''
        compara = 'SELECT *FROM PlanVacunacion  '
        self.getcursorObj().execute(compara)
        listado = self.getcursorObj().fetchall()

        ''' Con el iterador for a partir de una serie de condiciones se filtran los planes de vacunacion activos cuya
            fecha de inicio y fin abarca la fecha actual'''
        vigentes = []
        pendientes = []

        for ids in listado:

            ''' Se extraen las fechas de inicio y fin de cada plan de vacunacion, separandolas en dia, mes
                y año'''
            ini = ids[3].split("/")
            fechainicio = vl.Dato(datetime(int(ini[2]), int(ini[1]), int(ini[0])).strftime("%Y/%m/%d"))
            fin = ids[4].split("/")
            fechafin = vl.Dato(datetime(int(fin[2]), int(fin[1]), int(fin[0])).strftime("%Y/%m/%d"))

            if fechainicio.fecha("<=") and fechafin.fecha(">="):
                vigentes.append(ids)
            else:
                pendientes.append(ids)

        ''' Se termina la funcion en caso de que la base de datos no tenga informacion o no existan planes de 
            vacunacion activos a la fecha y se notifica al usuario'''
        if len(vigentes) == 0 and len(pendientes) == 0:
            print("\nNo hay planes de vacunacion en este momento.\n")
            return

        print("\n           PlANES DE VACUNACION ACTIVOS \n")

        if len(vigentes) != 0:
            ''' Se muestra en pantalla la informacion de los planes de vacunacion activos, con un formato de tabla hecho con
                simbolos a partir del metodo format'''

            print("+{:-<12}+{:-<20}+{:-<20}+{:-<30}+{:-<15}+".format("", "", "", "", ""))
            print("|{:^12}|{:^20}|{:^20}|{:^30}|{:^15}|".format("Plan", "Edad Minima", "Edad Maxima", "Fecha Inicio",
                                                                "Fecha Final"))
            print("+{:-<12}+{:-<20}+{:-<20}+{:-<30}+{:-<15}+".format("", "", "", "", ""))

            for idPlan, Emin, Emax, inicio, fin in vigentes:
                print("|{:^12}|{:^20}|{:^20}|{:^30}|{:^15}|".format(idPlan, Emin, Emax, inicio, fin))
                print("+{:-<12}+{:-<20}+{:-<20}+{:-<30}+{:-<15}+".format("", "", "", "", ""))
        else:
            print("No hay planes de vacunacion activos en este momento.")

        print("\n           PlANES DE VACUNACION FINALIZADOS O PENDIENTES POR INICIAR \n")
        if len(pendientes) != 0:
            ''' Se muestra en pantalla la informacion de los planes de vacunacion finalizados o que no han iniciado, con un formato de
                tabla hecho con simbolos a partir del metodo format'''

            print("+{:-<12}+{:-<20}+{:-<20}+{:-<30}+{:-<15}+".format("", "", "", "", ""))
            print("|{:^12}|{:^20}|{:^20}|{:^30}|{:^15}|".format("Plan", "Edad Minima", "Edad Maxima", "Fecha Inicio",
                                                                "Fecha Final"))
            print("+{:-<12}+{:-<20}+{:-<20}+{:-<30}+{:-<15}+".format("", "", "", "", ""))

            for idPlan, Emin, Emax, inicio, fin in pendientes:
                print("|{:^12}|{:^20}|{:^20}|{:^30}|{:^15}|".format(idPlan, Emin, Emax, inicio, fin))
                print("+{:-<12}+{:-<20}+{:-<20}+{:-<30}+{:-<15}+".format("", "", "", "", ""))
        else:
            print("No hay mas planes de vacunacion en este momento.")

        self.getconexion().commit()

    ''' Funcion para guardar la informacion que se le solicita al usuario
        sobre un plan de vacunacion que se creara'''

    def __recibirPlan(self):

        """Se solicita al usuario la edad minima y maxima del plan de vacunacion con un bucle que termina cuando
         la informacion es valida, donde se verifica que la edad minima sea menor a la maxima"""

        while True:

            ''' Por medio de un bucle se verifica que el dato ingresado para la edad minima sea un valor numerico
                mayor a cero'''
            self.setemin(vl.Dato(input("Escriba la edad minima del plan: ")))

            while not self.getemin().TipoDatoNum() or not self.getemin().longitud(3) or not self.getemin().rango(120):
                print("Ingrese un valor numerico: ")
                self.setemin(vl.Dato(input("Escriba la edad minima del plan: ")))

            ''' Por medio de un bucle se verifica que el dato ingresado para la edad maxima sea un valor numerico
                mayor a cero'''
            self.setemax(vl.Dato(input("Escriba la edad maxima del plan: ")))

            while not self.getemax().TipoDatoNum() or not self.getemax().longitud(3) or not self.getemax().rango(120):
                print("Ingrese un valor numerico: ")
                self.setemax(vl.Dato(input("Escriba la edad maxima del plan: ")))
                
            if int(self.getemin().variable) > int(self.getemax().variable):
                print("ERROR: la edad minima debe ser mayor a la maxima ingrese datos validos.")
            elif int(self.getemin().variable) <= 0:
                print("ERROR: la edad minima debe ser mayor a cero ingrese datos validos.")
            elif int(self.getemax().variable) <= 0:
                print("ERROR: la edad maxima debe ser mayor a cero ingrese datos validos.")
            else:
                break


        ''' Se pide la fecha de inicio del plan por medio de un bucle que se rompe cuando se verifica que la fecha
            ingresada sea mayor a la fecha actual'''
        
        while True:

            ''' Se solicita individualmente el dia, mes y año, verificando a partir de un bucle que los datos sean
                numericos y existan dentro del calendario'''
            dini = vl.Dato(input("Fecha de inicio:\n\n- Dia de inicio: "))
            while not dini.dia():
                dini = vl.Dato(input("Escriba el dia de inicio en dos digitos: "))
                
            mini = vl.Dato(input("- Mes de inicio: "))
            while not mini.mes():
                mini = vl.Dato(input("Escriba el mes de inicio en numeros entre el 1 y 12: "))
                    
            aini = vl.Dato(input("- año de inicio: "))
            while not aini.anio(2020, 3000):
                aini = vl.Dato(input("Escriba el año de inicio en numeros AAAA: "))

            ''' Usando el metodo strftime de la libreria datetime se guardan los valores ingresados por el
                usuario en formato de fecha (DD/MM/AAAA)'''
            fini1 = vl.Dato(datetime(int(aini.variable), int(mini.variable), int(dini.variable)).strftime("%Y/%m/%d"))

            if fini1.fecha(">="):
                self.setfini(datetime(int(aini.variable), int(mini.variable), int(dini.variable)).strftime("%d/%m/%Y"))
                break
            else:
                print("La fecha de inicio no es valida: ")
        print("Fecha de inicio ingresada: " + self.getfini())


        ''' Se pide la fecha de fin del plan por medio de un bucle que se rompe cuando se verifica que la fecha
            ingresada sea mayor a la fecha actual y a la fecha de inicio'''

        while True:

            ''' Se solicita individualmente el dia, mes y año, verificando a partir de un bucle que los datos sean
                numericos y existan dentro del calendario'''
            dfin = vl.Dato(input("Fecha de finalizacion:\n\n- Dia de finalizacion: "))
            while not dfin.dia():
                dfin = vl.Dato(input("Escriba el dia de finalizacion en dos digitos: "))
                
            mfin = vl.Dato(input("- Mes de finalizacion: "))
            while not mfin.mes():
                mfin = vl.Dato(input("Escriba el mes de finalizacion en numeros entre el 1 y 12: "))
                    
            afin = vl.Dato(input("- año de finalizacion: "))
            while not afin.anio(2020, 3000):
                afin = vl.Dato(input("Escriba el año de finalizacion en numeros AAAA: "))

            ''' Usando el metodo strftime de la libreria datetime se guardan los valores ingresados por el
                usuario en formato de fecha (DD/MM/AAAA)'''
            ffin1 = vl.Dato(datetime(int(afin.variable), int(mfin.variable), int(dfin.variable)).strftime("%Y/%m/%d"))

            if ffin1.fecha(">") and ffin1.variable > fini1.variable:
                self.setffin(datetime(int(afin.variable), int(mfin.variable), int(dfin.variable)).strftime("%d/%m/%Y"))
                break
            else:
                print("La fecha de finalizacion no es valida: ")
        print("Fecha de finalizacion ingresada: " + self.getffin())

        self.getcursorObj().execute('SELECT * FROM PlanVacunacion')
        Pexistentes = self.getcursorObj().fetchall()

        for ver in Pexistentes:
            if int(ver[1]) <= int(self.getemin().variable) <= int(ver[2]) or int(ver[1]) <= int(self.getemax().variable) <= int(ver[2]):

                compini = ver[3][6:10] + ver[3][2:6] + ver[3][:2]
                compfin = ver[4][6:10] + ver[4][2:6] + ver[4][:2]
                if compini <= fini1.variable <= compfin or compini <= ffin1.variable <= compfin:
                    print("\nDentro de la fecha estipulada, el rango de edad ingresado o parte de el, ya se encuentra dentro del plan de vacunacion numero",
                          ver[0], "que abarca el rango de edad entre los", ver[1], "y los", ver[2], "años, para las fechas entre el", ver[3], "y el",
                          ver[4], "\n")
                    return

        ''' Se guardan los datos del plan de vacunacion a crear en un contenedor de tipo tupla para su
            posterior uso'''
        infoplan = (self.getemin().variable, self.getemax().variable, self.getfini(), self.getffin())

        ''' Con el llamado a la funcion asignarvacuna se agenda la cita del paciente sobre el cual se esta iterando'''
        self.__insertar_Plan(infoplan)

        self.getconexion().commit()


    ''' Funcion para crear un nuevo lote de vacunas, que toma como parametro la conexion a la
        base de datos y el contenedor tupla que almacena la informacion del nuevo plan de vacunacion'''

    def __insertar_Plan(self, datosplan):

        """ Se crea un nuevo plan de vacunacion con la informacion recolectada del usuario, haciendo uso del
            objeto cursor y el metodo execute que utiliza el INSERT INTO dentro de los parametros"""
        self.getcursorObj().execute("""INSERT INTO PlanVacunacion( edadmin, edadmax,
                          fechainicioplan, fechafinalplan)VALUES ( ?, ?, ?, ?)""", datosplan)
        self.getconexion().commit()
