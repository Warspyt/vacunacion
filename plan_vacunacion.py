import sqlite3
from sqlite3 import Error
from datetime import datetime
from datetime import date

def sql_plan():
    # funcion que crea la base de datos
    try:
        conplan = sqlite3.connect('sisgenvac.db')
        return conplan
    except Error:
        print('Se ha producido un error al crear la conexion', Error)

def tabla_plan(con):
    cursorObj = con.cursor()
    # Se crea una tabla para los planes de vacunacion verificando que no exista aun
    cursorObj.execute("""CREATE TABLE IF NOT EXISTS PlanVacunacion(idplan integer PRIMARY KEY AUTOINCREMENT, edadmin text,
                      edadmax text, fechainicioplan text, fechafinalplan text)""")
    con.commit()

def consultaplan(con):
    cursorObj = con.cursor()

    now= datetime.now()
    dia = now.strftime("%d")
    mes = now.strftime("%m")
    ano = now.strftime("%Y")
    print("\n           PlANES EXISTENTES\n")
    compara  = 'SELECT *FROM PlanVacunacion  '
    cursorObj.execute(compara)
    listado = cursorObj.fetchall()
    for ids in listado:
        #print(ids)
        # Extraer las fechas de inicio y fin
        ini = ids[3].split("/")
        fin = ids[4].split("/")

        # Validacion para mostrar los planes de vacunacion que se encuentran activos
        if int(ini[2])< int(ano):
            if int(ano) < int(fin[2]):
                print(ids)
            elif int(ano) == int(fin[2]):
                if int(fin[1]) > int(mes):
                    print(ids)
                elif int(fin[1]) == int(mes) and int(fin[2])>= int(dia):
                    print(ids)
                   
        elif int(ini[2])== int(ano):
            if int(ini[1]) < int(mes):
                if int(ano) < int(fin[2]):
                    print(ids)
                elif int(ano) == int(fin[2]):
                    if int(fin[1]) > int(mes):
                        print(ids)
                    elif int(fin[1]) == int(mes) and int(fin[2])>= int(dia):
                        print(ids)
            elif int(ini[1]) == int(mes) and int(ini[2])<= int(dia):
                if int(ano) < int(fin[2]):
                    print(ids)
                elif int(ano) == int(fin[2]):
                    if int(fin[1]) > int(mes):
                        print(ids)
                    elif int(fin[1]) == int(mes) and int(fin[2])>= int(dia):
                        print(ids)
                           
def recibirPlan():

  emin=0
  emax=0
  fini=datetime.now().strftime("%d/%m/%Y")
  ffin=datetime.now().strftime("%d/%m/%Y")
  dini=0
  dfin=0
  mini=0
  mfin=0
  aini=0
  afin=0
  while (emin>emax or emin<=0 or emax<=0):
    emin = input("Escriba la edad minima del plan: ")
    emax = input("Escriba la edad maxima del plan: ")
    while True:
        if emin.isdigit() and emax.isdigit():
            break
        else:
            print("Ingrese un valor numerico: ")
            emin = input("Escriba la edad minima del plan: ")
            emax = input("Escriba la edad maxima del plan: ")
    emin = int(emin)
    emax = int(emax)
    if (emin>emax):
      print("ERROR: la edad minima debe ser mayor a la maxima ingrese datos validos")
    elif (emin<=0):
      print("ERROR: la edad minima debe ser mayor a cero ingrese datos validos")
    elif (emin<=0):
      print("ERROR: la edad maxima debe ser mayor a cero ingrese datos validos")
  while (fini>=ffin):
    while (dini<=0 or dini>31 or mini<=0 or mini>12 or aini<2020 or aini>2050 or dfin<=0 or dfin>31 or mfin<=0 or mfin>12 or afin<2020 or afin>2050):
      dini = input("Escriba dia de inicio del plan: ")
      mini = input("Escriba mes de inicio del plan: ")
      aini = input("Escriba año de inicio del plan: ")

      while True:
          if dini.isdigit() and mini.isdigit() and aini.isdigit():
              break
          else:
              print("Ingrese un valor numerico: ")
              dini = input("Escriba dia de inicio del plan: ")
              mini = input("Escriba mes de inicio del plan: ")
              aini = input("Escriba año de inicio del plan: ")
      dini = int(dini)
      mini = int(mini)
      aini = int(aini)
      
      dfin = input("Escriba dia de fin del plan: ")
      mfin = input("Escriba mes de fin del plan: ")
      afin = input("Escriba año de fin del plan: ")

      while True:
          if dfin.isdigit() and mfin.isdigit() and afin.isdigit():
              break
          else:
              print("Ingrese un valor numerico: ")
              dfin = input("Escriba dia de fin del plan: ")
              mfin = input("Escriba mes de fin del plan: ")
              afin = input("Escriba año de fin del plan: ")
      dfin = int(dfin)
      mfin = int(mfin)
      afin = int(afin)
      
      if (dini<=0 or dini>31 or dfin<=0 or dfin>31):
        print("ERROR: el dia inicial y final deben ser un entero entre 1 y 31 ingrese datos validos")
      elif (mini<=0 or mini>12 or mfin<=0 or mfin>12):
        print("ERROR: el mes inicial y final deben ser un entero entre 1 y 12 ingrese datos validos")
      elif (aini<2020 or aini>2050 or afin<2020 or afin>2050):
        print("ERROR: el año inicial y final deben ser un entero entre 2020 y 2050 ingrese datos validos")
    fini = datetime(aini, mini, dini).strftime("%d/%m/%Y")
    ffin = datetime(afin, mfin, dfin).strftime("%d/%m/%Y")
    if (fini>=ffin):
        print("ERROR: la fecha inicial debe ser menor a la final ingrese datos validos")
        dini=0
        dfin=0
        mini=0
        mfin=0
        aini=0
        afin=0
  plan =( emin, emax, fini, ffin)
  return plan 

def crearPlan(con, plan):
    # Se crea un nuevo plan de vacunacion con la informacion recolectada del usuario
    cursorObj = con.cursor()
    cursorObj.execute("""INSERT INTO PlanVacunacion( edadmin, edadmax,
                      fechainicioplan, fechafinalplan)VALUES ( ?, ?, ?, ?)""", plan)
    con.commit()


#def prueba():
  #conplan = sql_plan()
  #tabla_plan(conplan)
  #plan = recibirPlan()
  #crearPlan(conplan, plan)
  #infoPlanVacunacion()
  #consultaplan(conplan)

#prueba()
