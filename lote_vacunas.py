""" Se importan las librerias para el manejo de las bases de datos
    y de las fechas"""
import validaciones as vl
from datetime import datetime
from datetime import date

class Lotes:
    def __init__(self):
        pass

    ''' Funcion para crear la tabla de los lotes de vacunas dentro de la base de datos del
        programa, la cual toma como parametro la conexion de la misma'''

    def tabla_vacunas(self, con):
        """ Se crea una tabla para el lote de vacunas verificando que no exista aun, haciendo uso del objeto cursor
            y el metodo execute que utiliza el CREATE TABLE dentro de los parametros"""
        cursorObj = con.cursor()

        cursorObj.execute("""CREATE TABLE IF NOT EXISTS LoteVacunas(nolote integer PRIMARY KEY, fabricante text,
                          tipovacuna text, cantidadrecibida integer, cantidadusada integer, dosisnecesarias integer,
                          temperatura text, efectividad text, tiempoproteccion text, fechavencimiento text, imagen text, reserva integer)""")
        con.commit()


    ''' Funcion para guardar la informacion que se le solicita al usuario
        sobre un lote de vacunas que se creara'''

    def info_lote(self):
        """ Se pide al usuario el numero del lote a crear a partir de un bucle que se rompe cuando la
            informacion es aceptable, donde se verifica que el dato sea un valor numerico y su longitud
            sea menor a 13 digitos"""
        print("Ingrese la informacion del lote:\n")
        
        nolote = vl.Dato(input("Numero de lote: "))

        while not nolote.TipoDatoNum() or not nolote.longitud(12):
            nolote = vl.Dato(input("Ingrese un numero de lote valido: "))

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
        while not op_fabricante.TipoDatoNum() or not op_fabricante.rango(7) :
            op_fabricante = vl.Dato(input("Ingrese una opcion valida: "))

        ''' Con los condicionales if y else, segun la opcion ingresada se asignan los valores preestablecidos para
            cada vacuna,los cuales estan asignados de acuerdo a la informacion que se encuentra en internet sobre cada
            una de las mmismas'''
        if op_fabricante.variable == '1':
            fabricante = "Sinovac"
            tipovacuna = "Virus desactivado"
            dosisnecesarias = 2
            temperatura = "2 a 8°C"
            efectividad = "78%"
            tiempoproteccion = "120 dias"
        elif op_fabricante.variable == '2':
            fabricante = "Pfizer"
            tipovacuna = "En base a proteinas"
            dosisnecesarias = 2
            temperatura = "-25 a -15°C"
            efectividad = "95%"
            tiempoproteccion = "210 dias"
        elif op_fabricante.variable == '3':
            fabricante = "Moderna"
            tipovacuna = "ARN/ADN"
            dosisnecesarias = 2
            temperatura = "-20°C"
            efectividad = "94%"
            tiempoproteccion = "238 dias"
        elif op_fabricante.variable == '4':
            fabricante = "Sputnik V"
            tipovacuna = "Vector viral"
            dosisnecesarias = 2
            temperatura = "-18°C"
            efectividad = "92%"
            tiempoproteccion = "238 dias"
        elif op_fabricante.variable == '5':
            fabricante = "AstraZeneca"
            tipovacuna = "Vector viral"
            dosisnecesarias = 2
            temperatura = "2 a 8°C"
            efectividad = "70%"
            tiempoproteccion = "120 dias"
        elif op_fabricante.variable == '6':
            fabricante = "Sinopharm"
            tipovacuna = "Virus desactivado"
            dosisnecesarias = 2
            temperatura = "2 a 8°C"
            efectividad = "80%"
            tiempoproteccion = "120 dias"
        elif op_fabricante.variable == '7':
            fabricante = "Covaxim"
            tipovacuna = "Virus desactivado"
            dosisnecesarias = 2
            temperatura = "2 a 8°C"
            efectividad = "81%"
            tiempoproteccion = "180 dias"

        ''' Se solicita la cantidad de vacuna por medio de un bucle que se rompe cuando las condiciones son
            validas, verificando que el valor ingresado sea numerico y tenga una longitud menor a 7 digitos'''
        cantidadrecibida = vl.Dato(input("Cantidad recibida: "))

        while  not cantidadrecibida.TipoDatoNum() or not cantidadrecibida.longitud(6):
            cantidadrecibida = vl.Dato(input("Ingrese una cantidad valida: "))

        cantidadusada = 0
        reserva = 0

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
                fechavencimiento = datetime(int(anoven.variable), int(mesven.variable), int(diaven.variable)).strftime("%d/%m/%Y")
                break
            else:
                print("La fecha de vencimiento no es valida: ")
        print("Fecha ingresada: " + fechavencimiento)

        ''' Se solicita al usuario la ruta de una imagen de la vacuna, que posteriormente sera incluida
            dentro de la interfaz grafica del programa'''
        imagen = input("Ingrese la ruta de la imagen de una vacuna: ")
        print("Funcion de imagen en desarrollo, proximamente mas funcional...")

        ''' Se guardan los datos del lote a crear en un contenedor de tipo tupla para su posterior uso'''
        lote = (nolote.variable, fabricante, tipovacuna, cantidadrecibida.variable, cantidadusada, dosisnecesarias, temperatura, efectividad,
                tiempoproteccion, fechavencimiento, imagen, reserva)
        return lote


    ''' Funcion para crear un nuevo lote de vacunas, que toma como parametro la conexion a la
        base de datos y el contenedor tupla que almacena la informacion del nuevo lote'''

    def crear_lote(self, con, lote):
        """ Se crea un nuevo lote de vacunas con la informacion recolectada del usuario, haciendo uso del
            objeto cursor y el metodo execute que utiliza el INSERT INTO dentro de los parametros"""
        cursorObj = con.cursor()
        cursorObj.execute("""INSERT INTO LoteVacunas(nolote, fabricante, tipovacuna,
                          cantidadrecibida, cantidadusada, dosisnecesarias, temperatura, efectividad,
                          tiempoproteccion, fechavencimiento, imagen, reserva)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", lote)
        con.commit()


    ''' Funcion para consultar la informacion de los lotes vigentes a la fecha, que toma como
        parametro la conexion con la base de datos del programa'''

    def consultar_lote(self, con):
        """ Se muestran los lotes existentes en la base de datos que a la fecha tienen vigencia, haciendo uso
            del objeto cursor y el metodo execute que utiliza el SELECT dentro de los parametros"""
        cursorObj = con.cursor()

        print("\n           LOTES VIGENTES\n")
        cursorObj.execute('SELECT * FROM LoteVacunas')
        listado = cursorObj.fetchall()

        datoslote = []

        ''' Se verifica que la fecha de vencimiento de cada lote sea mayor a la actual, a partir del iterador for
            que recorre cada lote de vacunas existente en la base de datos'''
        factual = datetime.now().strftime("%Y/%m/%d")

        for ids in listado:
            llote = (ids[9]).split("/")
            venlote = datetime(int(llote[2]), int(llote[1]), int(llote[0])).strftime("%Y/%m/%d")
            if venlote > factual and ids[3] > ids[4]:
                print("•", ids[0])
            datoslote.append(ids[0])

        ''' Se termina la funcion en caso de que la base de datos no tenga informacion o no existan lotes vigentes
            a la fecha y se notifica al usuario'''
        if len(datoslote) == 0:
            print("En este momento no hay lotes vigentes.")
            return

        ''' Se solicita el numero del lote a consultar por medio de un bucle que se rompe cuando las condiciones son
            validas, verificando que el valor ingresado sea numerico y se encuentre dentro de la base de datos'''
        c_lote = input("\nNumero de lote a consultar: ")

        while True:
            if c_lote.isdigit() and int(c_lote) in datoslote:
                break
            else:
                c_lote = input("Ingrese un numero de lote valido: ")

        ''' Se extrae de la base de datos la informacion del lote indicado, haciendo uso del objeto cursor y el metodo
            execute que utiliza el SELECT dentro de los parametros'''
        cursorObj.execute('SELECT * FROM LoteVacunas where nolote= ' + c_lote)
        filas = cursorObj.fetchall()
        lfila = (filas[0][9]).split("/")
        venfila = datetime(int(lfila[2]), int(lfila[1]), int(lfila[0])).strftime("%Y/%m/%d")
        if venfila < factual or filas[0][3] <= filas[0][4]:
            print("ESTE LOTE NO SE ENCUENTRA VIGENTE\n")

        ''' Se muestra en pantalla la informacion del lote con un formato de tabla hecho con simbolos a partir del
            metodo format'''
        print("+{:-<10}+{:-<15}+{:-<21}+{:-<15}+{:-<10}+{:-<8}+{:-<15}+{:-<15}+{:-<25}+{:-<15}+{:-<15}+".format("", "", "",
                                                                                                                "", "", "",
                                                                                                                "", "", "",
                                                                                                                "", ""))
        print("|{:^10}|{:^15}|{:^21}|{:^15}|{:^10}|{:^8}|{:^15}|{:^15}|{:^25}|{:^15}|{:^15}|".format("lote", "Fabricante",
                                                                                                     "Tipo de vacuna",
                                                                                                     "Recibidas", "Usadas",
                                                                                                     "Dosis", "Temperatura",
                                                                                                     "Efectividad",
                                                                                                     "Tiempo de Proteccion",
                                                                                                     "Vencimiento",
                                                                                                     "imagen"))
        print("+{:-<10}+{:-<15}+{:-<21}+{:-<15}+{:-<10}+{:-<8}+{:-<15}+{:-<15}+{:-<25}+{:-<15}+{:-<15}+".format("", "", "",
                                                                                                                "", "", "",
                                                                                                                "", "", "",
                                                                                                                "", ""))
        for nolote, fabricante, tipovacuna, cantidadrecibida, cantidadusada, dosisnecesarias, temperatura, efectividad, tiempoproteccion, fechavencimiento, imagen, reserva in filas:
            print("|{:^10}|{:^15}|{:^21}|{:^15}|{:^10}|{:^8}|{:^15}|{:^15}|{:^25}|{:^15}|{:^15}|".format(nolote, fabricante,
                                                                                                         tipovacuna,
                                                                                                         cantidadrecibida,
                                                                                                         cantidadusada,
                                                                                                         dosisnecesarias,
                                                                                                         temperatura,
                                                                                                         efectividad,
                                                                                                         tiempoproteccion,
                                                                                                         fechavencimiento,
                                                                                                         imagen, reserva))
        print("+{:-<10}+{:-<15}+{:-<21}+{:-<15}+{:-<10}+{:-<8}+{:-<15}+{:-<15}+{:-<25}+{:-<15}+{:-<15}+".format("", "", "",
                                                                                                                "", "", "",
                                                                                                                "", "", "",
                                                                                                                "", ""))
        con.commit()


Lotes = Lotes()
Lotes.info_lote()
