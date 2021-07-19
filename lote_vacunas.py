""" Se importan las librerias para el manejo de las bases de datos
    y de las fechas"""
import validaciones as vl
from datetime import datetime
from datetime import date

class LoteVacunas:
    def __init__(self, con):
        self.__conexion = con
        self.__cursorObj = con.cursor()
        self.__nolote = "informacion no disponible"
        self.__fabricante = "informacion no disponible"
        self.__tipovacuna = "informacion no disponible"
        self.__cantidadrecibida = 0
        self.__cantidadusada = 0
        self.__dosisnecesarias = "informacion no disponible"
        self.__temperatura = "informacion no disponible"
        self.__efectividad = "informacion no disponible"
        self.__tiempoproteccion = "informacion no disponible"
        self.__fechavencimiento = "informacion no disponible"
        self.__imagen = "Imagen no disponible"
        self.__reserva = 0

    """ Acceso privado a la conexion"""
    def getconexion(self):
        return self.__conexion

    """ Acceso privado al cursor de la db"""
    def getcursorObj(self):
        return self.__cursorObj

    """ Acceso privado al numero de lote"""
    def setnolote(self, nolote):
        self.__nolote = nolote

    def getnolote(self):
        return self.__nolote

    """ Acceso privado al fabricante"""
    def setfabricante(self, fabricante):
        self.__fabricante = fabricante

    def getfabricante(self):
        return self.__fabricante

    """ Acceso privado al tipo de vacuna"""
    def settipovacuna(self, tipovacuna):
        self.__tipovacuna = tipovacuna

    def gettipovacuna(self):
        return self.__tipovacuna

    """ Acceso privado a la cantidad recibida"""
    def setcantidadrecibida(self, cantidadrecibida):
        self.__cantidadrecibida = cantidadrecibida

    def getcantidadrecibida(self):
        return self.__cantidadrecibida

    """ Acceso privado a la cantidad usada"""
    def getcantidadusada(self):
        return self.__cantidadusada

    """ Acceso privado a las dosis necesarias"""
    def setdosisnecesarias(self, dosisnecesarias):
        self.__dosisnecesarias = dosisnecesarias

    def getdosisnecesarias(self):
        return self.__dosisnecesarias

    """ Acceso privado a la temperatura"""
    def settemperatura(self, temperatura):
        self.__temperatura = temperatura

    def gettemperatura(self):
        return self.__temperatura

    """ Acceso privado a la efectividad"""
    def setefectividad(self, efectividad):
        self.__efectividad = efectividad

    def getefectividad(self):
        return self.__efectividad

    """ Acceso privado al tiempo de proteccion"""
    def settiempoproteccion(self, tiempoproteccion):
        self.__tiempoproteccion = tiempoproteccion

    def gettiempoproteccion(self):
        return self.__tiempoproteccion

    """ Acceso privado a la fecha de vencimiento"""
    def setfechavencimiento(self, fechavencimiento):
        self.__fechavencimiento = fechavencimiento

    def getfechavencimiento(self):
        return self.__fechavencimiento

    """ Acceso privado a la imagen"""
    def setimagen(self, imagen):
        self.__imagen = imagen

    def getimagen(self):
        return self.__imagen

    """ Acceso privado a la reserva"""
    def getreserva(self):
        return self.__reserva


class Lotes(LoteVacunas):

    """ Funcion para crear la tabla de los lotes de vacunas dentro de la base de datos del
        programa, la cual toma como parametro la conexion de la misma"""
        
    def __tabla_vacunas(self):
        """ Se crea una tabla para el lote de vacunas verificando que no exista aun, haciendo uso del objeto cursor
            y el metodo execute que utiliza el CREATE TABLE dentro de los parametros"""

        self.getcursorObj().execute("""CREATE TABLE IF NOT EXISTS LoteVacunas(nolote integer PRIMARY KEY, fabricante text,
                          tipovacuna text, cantidadrecibida integer, cantidadusada integer, dosisnecesarias integer,
                          temperatura text, efectividad text, tiempoproteccion text, fechavencimiento text, imagen text, reserva integer)""")
        
        self.getconexion().commit()

    ''' Funcion para guardar la informacion que se le solicita al usuario
        sobre un lote de vacunas que se creara'''

    def __info_lote(self):
        """ Se pide al usuario el numero del lote a crear a partir de un bucle que se rompe cuando la
            informacion es aceptable, donde se verifica que el dato sea un valor numerico y su longitud
            sea menor a 13 digitos"""
        print("Ingrese la informacion del lote:\n")

        self.setnolote(vl.Dato(input("Numero de lote: ")))

        while not self.getnolote().TipoDatoNum() or not self.getnolote().longitud(12):
            self.setnolote(vl.Dato(input("Ingrese un numero de lote valido: ")))
        
        ''' Se muestran en pantalla las opciones de vacunas y se solicita al usuario que ingrese una opcion
            identificada por el numero que la precede'''
        op_fabricante = vl.Dato(input("""Seleccione un fabricante:\n

        \t1 - Sinovac
        \t2 - Pfizer
        \t3 - Moderna
        \t4 - Sputnik V
        \t5 - AstraZeneca
        \t6 - Sinopharm
        \t7 - Covaxim\n\nSeleccione una opcion: """))

        ''' A partir de un bucle que se rompe cuando la informacion es valida, se verifica que el valor ingresado
            sea numerico y este entre las opciones dadas que son los numeros del 1 al 7'''
        while not op_fabricante.TipoDatoNum() or not op_fabricante.rango(7):
            op_fabricante = vl.Dato(input("Ingrese una opcion valida: "))

        ''' Con los condicionales if y else, segun la opcion ingresada se asignan los valores preestablecidos para
            cada vacuna,los cuales estan asignados de acuerdo a la informacion que se encuentra en internet sobre cada
            una de las mmismas'''
        if op_fabricante.variable == '1':
            self.setfabricante("Sinovac")
            self.settipovacuna("Virus desactivado")
            self.setdosisnecesarias(2)
            self.settemperatura("2 a 8°C")
            self.setefectividad("78%")
            self.settiempoproteccion("120 dias")
        elif op_fabricante.variable == '2':
            self.setfabricante("Pfizer")
            self.settipovacuna("En base a proteinas")
            self.setdosisnecesarias(2)
            self.settemperatura("-25 a -15°C")
            self.setefectividad("95%")
            self.settiempoproteccion("210 dias")
        elif op_fabricante.variable == '3':
            self.setfabricante("Moderna")
            self.settipovacuna("ARN/ADN")
            self.setdosisnecesarias(2)
            self.settemperatura("-20°C")
            self.setefectividad("94%")
            self.settiempoproteccion("238 dias")
        elif op_fabricante.variable == '4':
            self.setfabricante("Sputnik V")
            self.settipovacuna("Vector viral")
            self.setdosisnecesarias(2)
            self.settemperatura("-18°C")
            self.setefectividad("92%")
            self.settiempoproteccion("238 dias")
        elif op_fabricante.variable == '5':
            self.setfabricante("AstraZeneca")
            self.settipovacuna("Vector viral")
            self.setdosisnecesarias(2)
            self.settemperatura("2 a 8°C")
            self.setefectividad("70%")
            self.settiempoproteccion("120 dias")
        elif op_fabricante.variable == '6':
            self.setfabricante("Sinopharm")
            self.settipovacuna("Virus desactivado")
            self.setdosisnecesarias(2)
            self.settemperatura("2 a 8°C")
            self.setefectividad("80%")
            self.settiempoproteccion("120 dias")
        elif op_fabricante.variable == '7':
            self.setfabricante("Covaxim")
            self.settipovacuna("Virus desactivado")
            self.setdosisnecesarias(2)
            self.settemperatura("2 a 8°C")
            self.setefectividad("81%")
            self.settiempoproteccion("180 dias")

        ''' Se solicita la cantidad de vacuna por medio de un bucle que se rompe cuando las condiciones son
            validas, verificando que el valor ingresado sea numerico y tenga una longitud menor a 7 digitos'''
        self.setcantidadrecibida(vl.Dato(input("Cantidad recibida: ")))

        while not self.getcantidadrecibida().TipoDatoNum() or not self.getcantidadrecibida().longitud(6):
            self.setcantidadrecibida(vl.Dato(input("Ingrese una cantidad valida: ")))

        ''' Se pide la fecha de vencimiento por medio de un bucle que se rompe cuando se verifica que la fecha
            ingresada sea mayor a la fecha actual'''
        while True:

            ''' Se solicita individualmente el dia, mes y año, verificando a partir de un bucle que los datos sean
                numericos y existan dentro del calendario'''
            diaven = vl.Dato(input("Fecha de vencimiento:\n\n- Dia de vencimiento: "))
            while not diaven.dia():
                diaven = vl.Dato(input("Escriba el dia de vencimiento en dos digitos: "))
                
            mesven = vl.Dato(input("- Mes de vencimiento: "))
            while not mesven.mes():
                mesven = vl.Dato(input("Escriba el mes de vencimiento en numeros entre el 1 y 12: "))
                    
            anoven = vl.Dato(input("- año de vencimiento: "))
            while not anoven.anio(2020, 3000):
                anoven = vl.Dato(input("Escriba el año de vencimiento en numeros AAAA: "))

            ''' Usando el metodo strftime de la libreria datetime se guardan los valores ingresados por el
                usuario en formato de fecha (DD/MM/AAAA)'''
            fechavencimiento = vl.Dato(datetime(int(anoven.variable), int(mesven.variable), int(diaven.variable)).strftime("%Y/%m/%d"))

            if fechavencimiento.fecha(">"):
                self.setfechavencimiento(datetime(int(anoven.variable), int(mesven.variable), int(diaven.variable)).strftime("%d/%m/%Y"))
                break
            else:
                print("La fecha de vencimiento no es valida: ")
        print("Fecha ingresada: " + self.getfechavencimiento())

        ''' Se solicita al usuario la ruta de una imagen de la vacuna, que posteriormente sera incluida
            dentro de la interfaz grafica del programa'''
        imagen = input("Ingrese la ruta de la imagen de una vacuna: ")
        if imagen:
            self.setimagen(imagen)

        print("Funcion de imagen en desarrollo, proximamente mas funcional...")

        ''' Se guardan los datos del lote a crear en un contenedor de tipo tupla para su posterior uso'''
        lote = (self.getnolote().variable, self.getfabricante(), self.gettipovacuna(), self.getcantidadrecibida().variable, self.getcantidadusada(),
                self.getdosisnecesarias(), self.gettemperatura(), self.getefectividad(), self.gettiempoproteccion(), self.getfechavencimiento(),
                self.getimagen(), self.getreserva())

        try:
            self.__crear_lote(lote)
            self.setimagen("Imagen no disponible")
        except:
            print("\nVerifique la informacion y el numero de lote ingresado.\n")

    ''' Funcion para crear un nuevo lote de vacunas, que toma como parametro la conexion a la
        base de datos y el contenedor tupla que almacena la informacion del nuevo lote'''

    def __crear_lote(self, lote):
        """ Se crea un nuevo lote de vacunas con la informacion recolectada del usuario, haciendo uso del
            objeto cursor y el metodo execute que utiliza el INSERT INTO dentro de los parametros"""
        self.getcursorObj().execute("""INSERT INTO LoteVacunas(nolote, fabricante, tipovacuna,
                          cantidadrecibida, cantidadusada, dosisnecesarias, temperatura, efectividad,
                          tiempoproteccion, fechavencimiento, imagen, reserva)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", lote)
        
        self.getconexion().commit()

    ''' Funcion para consultar la informacion de los lotes vigentes a la fecha, que toma como
        parametro la conexion con la base de datos del programa'''

    def __consultar_lote(self):
        """ Se muestran los lotes existentes en la base de datos que a la fecha tienen vigencia, haciendo uso
            del objeto cursor y el metodo execute que utiliza el SELECT dentro de los parametros"""

        print("\n           LOTES VIGENTES\n")
        self.getcursorObj().execute('SELECT * FROM LoteVacunas')
        listado = self.getcursorObj().fetchall()

        datoslote = []

        ''' Se verifica que la fecha de vencimiento de cada lote sea mayor a la actual, a partir del iterador for
            que recorre cada lote de vacunas existente en la base de datos'''

        for ids in listado:
            llote = (ids[9]).split("/")
            venlote = vl.Dato(datetime(int(llote[2]), int(llote[1]), int(llote[0])).strftime("%Y/%m/%d"))
            if venlote.fecha(">") and ids[3] > ids[4]:
                print("•", ids[0])
            datoslote.append(ids[0])

        ''' Se termina la funcion en caso de que la base de datos no tenga informacion o no existan lotes vigentes
            a la fecha y se notifica al usuario'''
        if len(datoslote) == 0:
            print("En este momento no hay lotes vigentes.")
            return

        ''' Se solicita el numero del lote a consultar por medio de un bucle que se rompe cuando las condiciones son
            validas, verificando que el valor ingresado sea numerico y se encuentre dentro de la base de datos'''
        c_lote = vl.Dato(input("\nNumero de lote a consultar: "))

        while not c_lote.TipoDatoNum() or not vl.Dato(int(c_lote.variable)).existir(datoslote):
            c_lote = vl.Dato(input("Ingrese un numero de lote valido: "))

        ''' Se extrae de la base de datos la informacion del lote indicado, haciendo uso del objeto cursor y el metodo
            execute que utiliza el SELECT dentro de los parametros'''
        self.getcursorObj().execute('SELECT * FROM LoteVacunas where nolote= ' + c_lote.variable)
        filas = self.getcursorObj().fetchall()
        lfila = (filas[0][9]).split("/")
        venfila = vl.Dato(datetime(int(lfila[2]), int(lfila[1]), int(lfila[0])).strftime("%Y/%m/%d"))
        if venfila.fecha("<") or filas[0][3] <= filas[0][4]:
            print("ESTE LOTE NO SE ENCUENTRA VIGENTE\n")

        ''' Se muestra en pantalla la informacion del lote con un formato de tabla hecho con simbolos a partir del
            metodo format'''
        print("+{:-<10}+{:-<15}+{:-<21}+{:-<15}+{:-<10}+{:-<8}+{:-<15}+{:-<15}+{:-<25}+{:-<15}+{:-<20}+".format("", "", "",
                                                                                                                "", "", "",
                                                                                                                "", "", "",
                                                                                                                "", ""))
        print("|{:^10}|{:^15}|{:^21}|{:^15}|{:^10}|{:^8}|{:^15}|{:^15}|{:^25}|{:^15}|{:^20}|".format("lote", "Fabricante",
                                                                                                     "Tipo de vacuna",
                                                                                                     "Recibidas", "Usadas",
                                                                                                     "Dosis", "Temperatura",
                                                                                                     "Efectividad",
                                                                                                     "Tiempo de Proteccion",
                                                                                                     "Vencimiento",
                                                                                                     "imagen"))
        print("+{:-<10}+{:-<15}+{:-<21}+{:-<15}+{:-<10}+{:-<8}+{:-<15}+{:-<15}+{:-<25}+{:-<15}+{:-<20}+".format("", "", "",
                                                                                                                "", "", "",
                                                                                                                "", "", "",
                                                                                                                "", ""))
        for nolote, fabricante, tipovacuna, cantidadrecibida, cantidadusada, dosisnecesarias, temperatura, efectividad, tiempoproteccion, fechavencimiento, imagen, reserva in filas:
            print("|{:^10}|{:^15}|{:^21}|{:^15}|{:^10}|{:^8}|{:^15}|{:^15}|{:^25}|{:^15}|{:^20}|".format(nolote, fabricante,
                                                                                                         tipovacuna,
                                                                                                         cantidadrecibida,
                                                                                                         cantidadusada,
                                                                                                         dosisnecesarias,
                                                                                                         temperatura,
                                                                                                         efectividad,
                                                                                                         tiempoproteccion,
                                                                                                         fechavencimiento,
                                                                                                         imagen, reserva))
        print("+{:-<10}+{:-<15}+{:-<21}+{:-<15}+{:-<10}+{:-<8}+{:-<15}+{:-<15}+{:-<25}+{:-<15}+{:-<20}+".format("", "", "",
                                                                                                                "", "", "",
                                                                                                                "", "", "",
                                                                                                                "", ""))
        self.getconexion().commit()
