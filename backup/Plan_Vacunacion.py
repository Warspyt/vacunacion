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
  fini = datetime.now().strftime("%d/%m/%Y")
  ffin = datetime.now().strftime("%d/%m/%Y")
  dini=0
  dfin=0
  mini=0
  mfin=0
  aini=0
  afin=0

  # Validar que la edad minima sea menor que la edad maxima
  while (emin>=emax):
    emin = input("Escriba la edad minima del plan: ")
    # Verificar que la edad sea un valor numerico mayor a cero
    while True:
        if emin.isdigit() and len(emin) <= 3 and int(emin) > 0:
            break
        else:
            print("Ingrese un valor numerico: ")
            emin = input("Escriba la edad minima del plan: ")
    emax = input("Escriba la edad maxima del plan: ")
    # Verificar que la edad sea un valor numerico mayor a cero
    while True:
        if emax.isdigit() and len(emax) <= 3 and int(emax) > 0:
            break
        else:
            print("Ingrese un valor numerico: ")
            emax = input("Escriba la edad maxima del plan: ")
    emin = int(emin)
    emax = int(emax)
    if (emin>emax):
      print("ERROR: la edad minima debe ser mayor a la maxima ingrese datos validos")
    elif (emin<=0):
      print("ERROR: la edad minima debe ser mayor a cero ingrese datos validos")
    elif (emin<=0):
      print("ERROR: la edad maxima debe ser mayor a cero ingrese datos validos")
      
  while (fini >= ffin):
      dini = input("Escriba dia de inicio del plan: ")
      while True:
          if dini.isdigit() and 0 < int(dini) <= 31:
              break
          else:
              print("Ingrese un valor numerico: ")
              dini = input("Escriba dia de inicio del plan: ")
              
      mini = input("Escriba mes de inicio del plan: ")
      while True:
          if mini.isdigit() and 0 < int(mini) <= 12:
              break
          else:
              print("Ingrese un valor numerico: ")
              mini = input("Escriba mes de inicio del plan: ")

      
      aini = input("Escriba año de inicio del plan: ")
      while True:
          if aini.isdigit() and 2020 < int(aini) <= 2050:
              break
          else:
              print("Ingrese un valor numerico: ")
              aini = input("Escriba año de inicio del plan: ")
      dini = int(dini)
      mini = int(mini)
      aini = int(aini)
      
      dfin = input("Escriba dia de fin del plan: ")
      while True:
          if dfin.isdigit() and 0 < int(dfin) <= 31:
              break
          else:
              print("Ingrese un valor numerico: ")
              dfin = input("Escriba dia de fin del plan: ")
              
      mfin = input("Escriba mes de fin del plan: ")
      while True:
          if mfin.isdigit() and 0 < int(mfin) <= 12:
              break
          else:
              print("Ingrese un valor numerico: ")
              mfin = input("Escriba mes de fin del plan: ")
              
      afin = input("Escriba año de fin del plan: ")
      while True:
          if afin.isdigit() and 2020 < int(afin) <= 2050:
              break
          else:
              print("Ingrese un valor numerico: ")
              afin = input("Escriba año de fin del plan: ")
              
      dfin = int(dfin)
      mfin = int(mfin)
      afin = int(afin)
      
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
  plan = (emin, emax, fini, ffin)
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
