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
    print("\n           PlANES ACTIVOS EXISTENTES\n")
    compara  = 'SELECT *FROM PlanVacunacion  '
    cursorObj.execute(compara)
    listado = cursorObj.fetchall()

    # Planes a mostrar
    vigentes = []

    for ids in listado:
        #print(ids)
        # Extraer las fechas de inicio y fin
        ini = ids[3].split("/")
        fin = ids[4].split("/")

        # Validacion para mostrar los planes de vacunacion que se encuentran activos
        if int(ini[2])< int(ano):
            if int(ano) < int(fin[2]):
                vigentes.append(ids)
            elif int(ano) == int(fin[2]):
                if int(fin[1]) > int(mes):
                    vigentes.append(ids)
                elif int(fin[1]) == int(mes) and int(fin[2])>= int(dia):
                    vigentes.append(ids)
                   
        elif int(ini[2])== int(ano):
            if int(ini[1]) < int(mes):
                if int(ano) < int(fin[2]):
                    vigentes.append(ids)
                elif int(ano) == int(fin[2]):
                    if int(fin[1]) > int(mes):
                        vigentes.append(ids)
                    elif int(fin[1]) == int(mes) and int(fin[2])>= int(dia):
                        vigentes.append(ids)
            elif int(ini[1]) == int(mes) and int(ini[2])<= int(dia):
                if int(ano) < int(fin[2]):
                    vigentes.append(ids)
                elif int(ano) == int(fin[2]):
                    if int(fin[1]) > int(mes):
                        vigentes.append(ids)
                    elif int(fin[1]) == int(mes) and int(fin[2])>= int(dia):
                        vigentes.append(ids)


    print("+{:-<12}+{:-<20}+{:-<20}+{:-<30}+{:-<15}+".format("", "", "", "", ""))
    print("|{:^12}|{:^20}|{:^20}|{:^30}|{:^15}|".format("Plan", "Edad Minima", "Edad Maxima", "Fecha Inicio",
                                                            "Fecha Final"))
    print("+{:-<12}+{:-<20}+{:-<20}+{:-<30}+{:-<15}+".format("", "", "", "", ""))


    for idPlan, Emin, Emax, inicio, fin in vigentes:
        print("|{:^12}|{:^20}|{:^20}|{:^30}|{:^15}|".format(idPlan, Emin, Emax, inicio, fin))
        print("+{:-<12}+{:-<20}+{:-<20}+{:-<30}+{:-<15}+".format("", "","", "", ""))
                           
def recibirPlan():

  emin=0
  emax=0

  # Validar que la edad minima sea menor que la edad maxima
  while (emin >= emax):
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


# Verificar que la fecha de inicio sea posterior a la fecha actual
    while True:

        dini = input("Fecha de inicio del plan:\n\n- Dia de inicio: ")
        # Se verifica que el dato ingresado sea un dia existente dentro del calendario
        while True:
            if dini.isdigit() and 0<int(dini)<32:
                dini = dini.rjust(2,"0")
                break
            else:
                dini = input("Escriba el dia de inicio en dos digitos: ")
        mini = input("- Mes de inicio: ")
        # Se verifica que el dato ingresado sea un mes existente dentro del calendario
        while True:
            if mini.isdigit() and 0<int(mini)<13:
                mini = mini.rjust(2,"0")
                break
            else:
                mini = input("Escriba el mes de inicio en numeros entre el 1 y 12: ")
        aini = input("- año de inicio: ")
        # Se verifica que el dato ingresado sea un año coherente para el vencimiento
        while True:
            if aini.isdigit() and len(aini) == 4 and int(aini)>2020:
                aini = aini.rjust(4)
                break
            else:
                aini = input("Escriba el año de inicio en numeros AAAA: ")
        # Se guardan los datos de la fecha en formato (DD/MM/AAAA)
        fini = datetime(int(aini), int(mini), int(dini)).strftime("%Y/%m/%d")
        factual = datetime.now().strftime("%Y/%m/%d")
        #fechavencimiento = diaven+"/"+mesven+"/"+anoven
        if fini > factual:
            fini = datetime(int(aini), int(mini), int(dini)).strftime("%d/%m/%Y")
            break
        else:
            print("La fecha de inicio del plan no es valida: ")
    print("Fecha de inicio ingresada: " + fini)

# Verificar que la fecha de fin sea posterior a la fecha actual y a la fecha de inicio
    while True:

        dfin = input("Fecha de finalizacion del plan:\n\n- Dia de finalizacion: ")
        # Se verifica que el dato ingresado sea un dia existente dentro del calendario
        while True:
            if dfin.isdigit() and 0<int(dfin)<32:
                dfin = dfin.rjust(2,"0")
                break
            else:
                dfin = input("Escriba el dia de finalizacion en dos digitos: ")
        mfin = input("- Mes de finalizacion: ")
        # Se verifica que el dato ingresado sea un mes existente dentro del calendario
        while True:
            if mfin.isdigit() and 0<int(mfin)<13:
                mfin = mfin.rjust(2,"0")
                break
            else:
                mini = input("Escriba el mes de finalizacion en numeros entre el 1 y 12: ")
        afin = input("- año de finalizacion: ")
        # Se verifica que el dato ingresado sea un año coherente para el vencimiento
        while True:
            if afin.isdigit() and len(afin) == 4 and int(afin)>2020:
                afin = afin.rjust(4)
                break
            else:
                afin = input("Escriba el año de finalizacion en numeros AAAA: ")
        # Se guardan los datos de la fecha en formato (DD/MM/AAAA)
        ffin = datetime(int(afin), int(mfin), int(dfin)).strftime("%Y/%m/%d")
        factual = datetime.now().strftime("%Y/%m/%d")
        #fechavencimiento = diaven+"/"+mesven+"/"+anoven
        if ffin > factual and ffin > fini:
            ffin = datetime(int(afin), int(mfin), int(dfin)).strftime("%d/%m/%Y")
            break
        else:
            print("La fecha de finalizacion del plan no es valida: ")
    print("Fecha de finalizacion ingresada: " + ffin)

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
