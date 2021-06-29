""" Se importan las librerias para el manejo de las bases de datos
    y de las fechas"""
import sqlite3
from sqlite3 import Error
from datetime import datetime
from datetime import date

''' Funcion para establecer la conexion con la base de datos del
    programa'''


def sql_plan():
    """ Se crea la conexion a la base de datos usando el metodo connect, creando el archivo en caso de que no exista y se verifica que
        no ocurra ningun error a partir de un try - except"""
    try:
        conplan = sqlite3.connect('sisgenvac.db')
        return conplan
    except Error:
        print('Se ha producido un error al crear la conexion', Error)


''' Funcion para crear la tabla de los planes de vacunacion dentro de la base de datos del
    programa, la cual toma como parametro la conexion de la misma'''


def tabla_plan(con):
    """ Se crea una tabla para los planes de vacunacion verificando que no exista aun, haciendo uso del objeto cursor
        y el metodo execute que utiliza el CREATE TABLE dentro de los parametros"""
    cursorObj = con.cursor()

    cursorObj.execute("""CREATE TABLE IF NOT EXISTS PlanVacunacion(idplan integer PRIMARY KEY AUTOINCREMENT, edadmin text,
                      edadmax text, fechainicioplan text, fechafinalplan text)""")
    con.commit()


''' Funcion para consultar la informacion de los planes de vacunacion activos a la fecha,
    la cual toma como parametro la conexion con la base de datos del programa'''


def consultaplan(con):
    cursorObj = con.cursor()

    ''' Se extrae la fecha actual con el metodo now de la libreria datetime y se separa en dia,
        mes y año'''
    now = datetime.now()
    dia = now.strftime("%d")
    mes = now.strftime("%m")
    ano = now.strftime("%Y")

    ''' Se extraen todos los planes de vacunacion de la base de datos del programa, con el objeto cursor y el
        metodo execute que utiliza el SELECT como parametro '''
    print("\n           PlANES ACTIVOS EXISTENTES\n")
    compara = 'SELECT *FROM PlanVacunacion  '
    cursorObj.execute(compara)
    listado = cursorObj.fetchall()

    ''' Con el iterador for a partir de una serie de condiciones se filtran los planes de vacunacion activos cuya
        fecha de inicio y fin abarca la fecha actual'''
    vigentes = []

    for ids in listado:

        ''' Se extraen las fechas de inicio y fin de cada plan de vacunacion, separandolas en dia, mes
            y año'''
        ini = ids[3].split("/")
        fin = ids[4].split("/")

        if int(ini[2]) < int(ano):
            if int(ano) < int(fin[2]):
                vigentes.append(ids)
            elif int(ano) == int(fin[2]):
                if int(fin[1]) > int(mes):
                    vigentes.append(ids)
                elif int(fin[1]) == int(mes) and int(fin[2]) >= int(dia):
                    vigentes.append(ids)

        elif int(ini[2]) == int(ano):
            if int(ini[1]) < int(mes):
                if int(ano) < int(fin[2]):
                    vigentes.append(ids)
                elif int(ano) == int(fin[2]):
                    if int(fin[1]) > int(mes):
                        vigentes.append(ids)
                    elif int(fin[1]) == int(mes) and int(fin[2]) >= int(dia):
                        vigentes.append(ids)
            elif int(ini[1]) == int(mes) and int(ini[2]) <= int(dia):
                if int(ano) < int(fin[2]):
                    vigentes.append(ids)
                elif int(ano) == int(fin[2]):
                    if int(fin[1]) > int(mes):
                        vigentes.append(ids)
                    elif int(fin[1]) == int(mes) and int(fin[2]) >= int(dia):
                        vigentes.append(ids)

    ''' Se termina la funcion en caso de que la base de datos no tenga informacion o no existan planes de 
        vacunacion activos a la fecha y se notifica al usuario'''
    if len(vigentes) == 0:
        print("No hay planes de vacunacion activos en este momento.")
        return

    ''' Se muestra en pantalla la informacion de los planes de vacunacion activos, con un formato de tabla hecho con
        simbolos a partir del metodo format'''
    print("+{:-<12}+{:-<20}+{:-<20}+{:-<30}+{:-<15}+".format("", "", "", "", ""))
    print("|{:^12}|{:^20}|{:^20}|{:^30}|{:^15}|".format("Plan", "Edad Minima", "Edad Maxima", "Fecha Inicio",
                                                        "Fecha Final"))
    print("+{:-<12}+{:-<20}+{:-<20}+{:-<30}+{:-<15}+".format("", "", "", "", ""))

    for idPlan, Emin, Emax, inicio, fin in vigentes:
        print("|{:^12}|{:^20}|{:^20}|{:^30}|{:^15}|".format(idPlan, Emin, Emax, inicio, fin))
        print("+{:-<12}+{:-<20}+{:-<20}+{:-<30}+{:-<15}+".format("", "", "", "", ""))


''' Funcion para guardar la informacion que se le solicita al usuario
    sobre un plan de vacunacion que se creara'''


def recibirPlan():
    """Se solicita al usuario la edad minima y maxima del plan de vacunacion con un bucle que termina cuando
     la informacion es valida, donde se verifica que la edad minima sea menor a la maxima"""
    emin = 0
    emax = 0

    while emin >= emax:

        ''' Por medio de un bucle se verifica que el dato ingresado para la edad minima sea un valor numerico
        mayor a cero'''
        emin = input("Escriba la edad minima del plan: ")

        while True:
            if emin.isdigit() and len(emin) <= 3 and int(emin) > 0:
                break
            else:
                print("Ingrese un valor numerico: ")
                emin = input("Escriba la edad minima del plan: ")

        ''' Por medio de un bucle se verifica que el dato ingresado para la edad maxima sea un valor numerico
        mayor a cero'''
        emax = input("Escriba la edad maxima del plan: ")

        while True:
            if emax.isdigit() and len(emax) <= 3 and int(emax) > 0:
                break
            else:
                print("Ingrese un valor numerico: ")
                emax = input("Escriba la edad maxima del plan: ")
        emin = int(emin)
        emax = int(emax)
        if emin > emax:
            print("ERROR: la edad minima debe ser mayor a la maxima ingrese datos validos")
        elif emin <= 0:
            print("ERROR: la edad minima debe ser mayor a cero ingrese datos validos")
        elif emax <= 0:
            print("ERROR: la edad maxima debe ser mayor a cero ingrese datos validos")

        ''' Se pide la fecha de inicio del plan por medio de un bucle que se rompe cuando se verifica que la fecha
        ingresada sea mayor a la fecha actual'''
        while True:

            ''' Se solicita individualmente el dia, mes y año, verificando a partir de un bucle que los datos sean
            numericos y existan dentro del calendario'''
            dini = input("Fecha de inicio del plan:\n\n- Dia de inicio: ")
            while True:
                if dini.isdigit() and 0 < int(dini) < 32:
                    dini = dini.rjust(2, "0")
                    break
                else:
                    dini = input("Escriba el dia de inicio en dos digitos: ")
            mini = input("- Mes de inicio: ")
            while True:
                if mini.isdigit() and 0 < int(mini) < 13:
                    mini = mini.rjust(2, "0")
                    break
                else:
                    mini = input("Escriba el mes de inicio en numeros entre el 1 y 12: ")
            aini = input("- año de inicio: ")
            while True:
                if aini.isdigit() and len(aini) == 4 and int(aini) > 2020:
                    aini = aini.rjust(4)
                    break
                else:
                    aini = input("Escriba el año de inicio en numeros AAAA: ")

            ''' Usando el metodo strftime de la libreria datetime se guardan los valores ingresados por el
            usuario en formato de fecha (DD/MM/AAAA)'''
            fini = datetime(int(aini), int(mini), int(dini)).strftime("%Y/%m/%d")
            factual = datetime.now().strftime("%Y/%m/%d")

            if fini > factual:
                fini = datetime(int(aini), int(mini), int(dini)).strftime("%d/%m/%Y")
                break
            else:
                print("La fecha de inicio del plan no es valida: ")
        print("Fecha de inicio ingresada: " + fini)

        ''' Se pide la fecha de fin del plan por medio de un bucle que se rompe cuando se verifica que la fecha
        ingresada sea mayor a la fecha actual y a la fecha de inicio'''
        while True:

            ''' Se solicita individualmente el dia, mes y año, verificando a partir de un bucle que los datos sean
            numericos y existan dentro del calendario'''
            dfin = input("Fecha de finalizacion del plan:\n\n- Dia de finalizacion: ")
            while True:
                if dfin.isdigit() and 0 < int(dfin) < 32:
                    dfin = dfin.rjust(2, "0")
                    break
                else:
                    dfin = input("Escriba el dia de finalizacion en dos digitos: ")
            mfin = input("- Mes de finalizacion: ")
            while True:
                if mfin.isdigit() and 0 < int(mfin) < 13:
                    mfin = mfin.rjust(2, "0")
                    break
                else:
                    mfin = input("Escriba el mes de finalizacion en numeros entre el 1 y 12: ")
            afin = input("- año de finalizacion: ")
            while True:
                if afin.isdigit() and len(afin) == 4 and int(afin) > 2020:
                    afin = afin.rjust(4)
                    break
                else:
                    afin = input("Escriba el año de finalizacion en numeros AAAA: ")

            ''' Usando el metodo strftime de la libreria datetime se guardan los valores ingresados por el
            usuario en formato de fecha (DD/MM/AAAA)'''
            ffin = datetime(int(afin), int(mfin), int(dfin)).strftime("%Y/%m/%d")
            factual = datetime.now().strftime("%Y/%m/%d")

            if ffin > factual and ffin > fini:
                ffin = datetime(int(afin), int(mfin), int(dfin)).strftime("%d/%m/%Y")
                break
            else:
                print("La fecha de finalizacion del plan no es valida: ")
        print("Fecha de finalizacion ingresada: " + ffin)

    ''' Se guardan los datos del plan de vacunacion a crear en un contenedor de tipo tupla para su
      posterior uso'''
    plan = (emin, emax, fini, ffin)
    return plan


''' Funcion para crear un nuevo lote de vacunas, que toma como parametro la conexion a la
    base de datos y el contenedor tupla que almacena la informacion del nuevo plan de vacunacion'''


def crearPlan(con, plan):
    """ Se crea un nuevo plan de vacunacion con la informacion recolectada del usuario, haciendo uso del
        objeto cursor y el metodo execute que utiliza el INSERT INTO dentro de los parametros"""
    cursorObj = con.cursor()
    cursorObj.execute("""INSERT INTO PlanVacunacion( edadmin, edadmax,
                      fechainicioplan, fechafinalplan)VALUES ( ?, ?, ?, ?)""", plan)
    con.commit()
