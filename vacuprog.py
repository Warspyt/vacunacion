import sqlite3
from sqlite3 import Error
from datetime import datetime
from datetime import date
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

    # Se muestran los Planes vigentes en la base de datos
    print("\n           PLANES VIGENTES\n")
    cursorObj.execute('SELECT * FROM PlanVacunacion')
    listado = cursorObj.fetchall()
    datosplan = []

    # Verificar la fecha para mostrar los lotes vigentes
    factual = datetime.now().strftime("%Y/%m/%d")

    for ids in listado:
        lplan = (ids[4]).split("/")
        venplan = datetime(int(lplan[2]), int(lplan[1]), int(lplan[0])).strftime("%Y/%m/%d")
        if venplan > factual:
            print("•", ids[0],"para afiliados entre ",ids[1] ," y ", ids[2], "años")
            datosplan.append(ids[0])
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
    print(novacunados)
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
con = sql_vac()
lote_v(con)

