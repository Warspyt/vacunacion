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

    # Se muestran los lotes existentes en la base de datos
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
    c_plan = input("\nIngrese el numero de lote a programar: ")
    # Se verifica que el lote sea un valor numerico y se encuentre dentro de la base de datos
    while True:
        if c_plan.isdigit() and int(c_plan) in datosplan:
            break
        else:
            c_plan = input("Ingrese un numero de plan valido: ")

    cursorObj = con.cursor()

    sql = "SELECT * FROM afiliados WHERE vacunado ='N'"

    mycursor.execute(sql)

    myresult = cursorObj.fetchall()

    for x in myresult:
      print(x)
con = sql_vac()
lote_v(con)

