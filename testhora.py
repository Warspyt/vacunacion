import sqlite3
from sqlite3 import Error
from datetime import datetime
from datetime import date
from datetime import timedelta
import lote_vacunas


def sql_vac():
    # funcion que crea la base de datos
    try:
        con = sqlite3.connect('sisgenvac.db')
        # print("Conexion realizada: DB creada")
        return con
    except Error:
        print('Se ha producido un error al crear la conexion', Error)


def lote_v(con):
    cursorObj = con.cursor()

    while True:

        diaprog = input("Fecha de inicio del agendamiento de citas:\n\n- Dia de inicio: ")
        # Se verifica que el dato ingresado sea un dia existente dentro del calendario
        while True:
            if diaprog.isdigit() and 0 < int(diaprog) < 32:
                diaprog = diaprog.rjust(2, "0")
                break
            else:
                diaprog = input("Escriba el dia de inicio en dos digitos: ")
        mesprog = input("- Mes de inicio: ")
        # Se verifica que el dato ingresado sea un mes existente dentro del calendario
        while True:
            if mesprog.isdigit() and 0 < int(mesprog) < 13:
                mesprog = mesprog.rjust(2, "0")
                break
            else:
                mesprog = input("Escriba el mes de inicio en numeros entre el 1 y 12: ")
        anoprog = input("- año de inicio: ")
        # Se verifica que el dato ingresado sea un año coherente para el vencimiento
        while True:
            if anoprog.isdigit() and len(anoprog) == 4 and int(anoprog) > 2020:
                anoprog = anoprog.rjust(4)
                break
            else:
                anoprog = input("Escriba el año de inicio en numeros AAAA: ")
                # Se verifica que el dato ingresado sea un año coherente para el vencimiento
        hourprog = input("- Hora de inicio: ")
        while True:
             if hourprog.isdigit() and 0 < int(hourprog) < 25:
                 hourprog = hourprog.rjust(2)
                 break
             else:
                hourprog = input("Escriba la hora de inicio en numeros entre el 1 y 24: ")
        minprog = input("- minutos de inicio: ")
        while True:
            if minprog.isdigit() and 0 < int(minprog) < 61:
                minprog = minprog.rjust(2)
                break
            else:
                minprog = input("Escriba la hora de inicio en numeros entre el 1 y 60: ")
        # Se guardan los datos de la fecha en formato (DD/MM/AAAA)
        fechaprog1 = datetime(int(anoprog), int(mesprog), int(diaprog),int(hourprog),int(minprog)).strftime('%d/%m/%Y %H:%M')
        factual = datetime.now().strftime('%d/%m/%Y %H:%M')
        # fechavencimiento = diaven+"/"+mesven+"/"+anoven



        if fechaprog1 >= factual:
            fechaprog = datetime(int(anoprog), int(mesprog), int(diaprog)).strftime("%d/%m/%Y")
            break
        else:
            print("La fecha de inicio no es valida: ")


    print("Fecha ingresada: " ,fechaprog, type(fechaprog))
    print("Fecha ingresada: ",fechaprog1 , type(fechaprog1))
    fecha_cad1 = fechaprog1
    fecha1 = datetime.strptime(fecha_cad1, '%d/%m/%Y %H:%M')
    print("Fecha ingresada: ", fecha1, type(fecha1))


    newdate = fecha1 + timedelta(hours=1)
    print("hora mas  30 minutos:",newdate)
    a = 1
    while a < 10:
        newdate=newdate+timedelta(minutes=30)
        print(newdate)
        a = a + 1


con = sql_vac()
lote_v(con)


