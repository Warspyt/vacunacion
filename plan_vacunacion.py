import sqlite3
from sqlite3 import Error
import datetime
# los planes deben meterse manual mente  esto sobra en ese orden de ideas

"""
p1 = [1, 60, 80, datetime.datetime(2021, 1, 1).strftime("%d/%m/%Y"), datetime.datetime(2022, 1, 1).strftime("%d/%m/%Y")]
p2 = [2, 50, 59, datetime.datetime(2022, 1, 1).strftime("%d/%m/%Y"), datetime.datetime(2023, 1, 1).strftime("%d/%m/%Y")]
p3 = [3, 40, 49, datetime.datetime(2023, 1, 1).strftime("%d/%m/%Y"), datetime.datetime(2024, 1, 1).strftime("%d/%m/%Y")]
p4 = [4, 30, 39, datetime.datetime(2024, 1, 1).strftime("%d/%m/%Y"), datetime.datetime(2025, 1, 1).strftime("%d/%m/%Y")]
p5 = [5, 20, 29, datetime.datetime(2025, 1, 1).strftime("%d/%m/%Y"), datetime.datetime(2026, 1, 1).strftime("%d/%m/%Y")]
p6 = [6, 16, 19, datetime.datetime(2026, 1, 1).strftime("%d/%m/%Y"), datetime.datetime(2027, 1, 1).strftime("%d/%m/%Y")]


listaPlanes = [p1,p2,p3,p4,p5,p6]                                                         #No olvidar agregar cada plan nuevo a la lista de planes
"""
def sql_plan():
    # funcion que crea la base de datos
    try:
        conplan = sqlite3.connect('sisgenvac.db')
        print("Conexion realizada: DB creada")
        return conplan
    except Error:
        print('Se ha producido un error al crear la conexion', Error)

def tabla_plan(con):
    cursorObj = con.cursor()
    # Se crea una tabla para los planes de vacunacion verificando que no exista aun
    cursorObj.execute("""CREATE TABLE IF NOT EXISTS PlanVacunacion(idplan integer PRIMARY KEY AUTOINCREMENT, edadmin text,
                      edadmax text, fechainicioplan text, fechafinalplan text)""")
    con.commit()

def infoPlanVacunacion():
  id = int(input("Escriba el id del plan: "))
  for i in listaPlanes:
    if i.idplan == id:
      p=i
      break
    else:
      p=None
  edad = int(input("Escriba su edad: "))
  if (p==None):
    print("ERROR: no existe plan asignado a la id %d en la lista de planes" %(id))
  elif (edad>=p.edadminima and edad<=p.edadmaxima):
    print("Su periodo de vacunacion para el plan %d comprende entre %s y %s" %(p.idplan,p.fechainicioplan,p.fechafinplan))
  elif (edad<p.edadminima):
    print("ERROR: la edad mínima para el plan %d es %d" %(p.idplan,p.edadminima))
  else:
    print("ERROR: la edad máxima para el plan %d es %d" %(p.idplan,p.edadmaxima))

def consultaplan():
    cursorobj = con.cursor()

def recibirPlan():
  # id = len(listaPlanes)+1 # id es palabra restringida entonces no se puede usar como variable
  # siempre crea plan 7 lo que genera un error debe ser autoincrement ya lo deje  en autoincrement


  emin = int(input("Escriba la edad minima del plan: "))
  emax = int(input("Escriba la edad maxima del plan: "))
  #print(idp ,"este es  id")
  if (emin>emax):
    emax=emin

      # no las puede hacer iguales debe hacer un except conun print del error que no puede ser mayor
  dini = int(input("Escriba dia de inicio del plan: "))
  mini = int(input("Escriba mes de inicio del plan: "))
  aini = int(input("Escriba año de inicio del plan: "))
  fini = datetime.datetime(aini, mini, dini).strftime("%d/%m/%Y")
  dfin = int(input("Escriba dia de fin del plan: "))
  mfin = int(input("Escriba mes de fin del plan: "))
  afin = int(input("Escriba año de fin del plan: "))
  ffin = datetime.datetime(afin, mfin, dfin).strftime("%d/%m/%Y")
  if (fini>ffin):
    ffin=fini

      # aca lo mismo no puede igualarse por que si, si digito mal estariamso metioendo info  que no es, si queria dar otra fecha nosotros  la admitimos mal
  plan =( emin, emax, fini, ffin)
  #listaPlanes.append(plan) # Ya no es necesario, con otra funcion lo guardas en la base de datos
  #cada plan se ingresa manual
  return plan # para que la funcion te guarde los datos recogidos

def crearPlan(con, plan):
    # Se crea un nuevo plan de vacunacion con la informacion recolectada del usuario
    cursorObj = con.cursor()
    cursorObj.execute("""INSERT INTO PlanVacunacion( edadmin, edadmax,
                      fechainicioplan, fechafinalplan)VALUES ( ?, ?, ?, ?)""", plan)
    con.commit()


def  menuPlan(): # Todo esto esta en el archivo de main, solo es que pongas las funciones alla y listo :)
  print("1. Crear nuevo plan de vacunación")
  print("2. Realizar consulta plan de vacunación")
  print("3. Salir")
  op = int(input("Escriba la opción que desea ejecutar: "))
  if (op == 1):
    crearPlan()
  elif (op == 2):
    infoPlanVacunacion()
  elif (op == 3):
    quit()
  else:
    print("ERROR: Opción incorecta")

# menuPlan()
# Prueba para crear un plan y guardar los datos en la base de datos
def prueba():
  conplan = sql_plan()
  tabla_plan(conplan)
  #plan = recibirPlan()
  #crearPlan(conplan, plan)
  infoPlanVacunacion()

prueba()
