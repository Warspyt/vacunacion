import sqlite3
from sqlite3 import Error
from datetime import datetime
from datetime import date
import lote_vacunas

def sql_vac():
    cursorObj = con.cursor()
    
    while True:

        diaprog = input("Fecha de inicio del agendamiento de citas:\n\n- Dia de inicio: ")
        # Se verifica que el dato ingresado sea un dia existente dentro del calendario
        while True:
            if diaprog.isdigit() and 0<int(diaprog)<32:
                diaprog = diaprog.rjust(2,"0")
                break
            else:
                diaprog = input("Escriba el dia de inicio en dos digitos: ")
        mesprog = input("- Mes de inicio: ")
        # Se verifica que el dato ingresado sea un mes existente dentro del calendario
        while True:
            if mesprog.isdigit() and 0<int(mesprog)<13:
                mesprog = mesprog.rjust(2,"0")
                break
            else:
                mesprog = input("Escriba el mes de inicio en numeros entre el 1 y 12: ")
        anoprog = input("- año de inicio: ")
        # Se verifica que el dato ingresado sea un año coherente para el vencimiento
        while True:
            if anoprog.isdigit() and len(anoprog) == 4 and int(anoprog)>2020:
                anoprog = anoprog.rjust(4)
                break
            else:
                anoprog = input("Escriba el año de inicio en numeros AAAA: ")
        # Se guardan los datos de la fecha en formato (DD/MM/AAAA)
        fechaprog1 = datetime(int(anoprog), int(mesprog), int(diaprog)).strftime("%Y/%m/%d")
        factual = datetime.now().strftime("%Y/%m/%d")
        #fechavencimiento = diaven+"/"+mesven+"/"+anoven
        if fechaprog1 > factual:
            fechaprog = datetime(int(anoprog), int(mesprog), int(diaprog)).strftime("%d/%m/%Y")
            break
        else:
            print("La fecha de inicio no es valida: ")
    print("Fecha ingresada: " + fechaprog)

    # Se muestran los Planes vigentes en la base de datos
    print("\n           PLANES VIGENTES\n")
    cursorObj.execute('SELECT * FROM PlanVacunacion')
    listado = cursorObj.fetchall()
    datosplan = []

    # Verificar la fecha para mostrar los planes vigentes a la fecha programada

    for ids in listado:
        lplan = (ids[4]).split("/")
        venplan = datetime(int(lplan[2]), int(lplan[1]), int(lplan[0])).strftime("%Y/%m/%d")
        if venplan > fechaprog1:
            print("•", ids[0],"para afiliados entre ",ids[1] ," y ", ids[2], "años")
            datosplan.append(ids[0])
'''
    c_plan = input("\nIngrese el numero de plan a programar: ")
    # Se verifica que el plan sea un valor numerico y se encuentre dentro de la base de datos
    while True:
        if c_plan.isdigit() and int(c_plan) in datosplan:
            break
        else:
            c_plan = input("Ingrese un numero de plan vigente: ")

    cursorObj.execute('SELECT * FROM PlanVacunacion where idplan= ' + c_plan)
    planselect = cursorObj.fetchall()
    eminplan = int(planselect[0][1])
    emaxplan = int(planselect[0][2])

    # Se busca el plan en la base de datos y se extrae la informacion
    cursorObj.execute("SELECT * FROM afiliados where vacunado= 'N'")
    novacunados = cursorObj.fetchall()
    edadvalida = []
    for edad in novacunados:
        # Calcular edad
        nacimiento = edad[7].split("/")
        now= datetime.now()
        dia = now.strftime("%d")
        mes = now.strftime("%m")
        ano = now.strftime("%Y")

        dano = (int(ano) - int(nacimiento[2]))*365
        dmes = (int(mes) - int(nacimiento[1]))*30
        ddia = int(dia) - int(nacimiento[0])
        edadaf = (dano + dmes + ddia)//365
        if eminplan <= edadaf <= emaxplan:
            edadvalida.append(edad[0])
    print(edadvalida)
 '''   
con = sql_vac()
lote_v(con)

