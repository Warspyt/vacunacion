import sqlite3
from sqlite3 import Error
import datetime
class Plan:                                                                               #Clase Plan
  def __init__(self, idplan, edadminima, edadmaxima, fechainicioplan, fechafinplan):
    self.idplan = idplan
    self.edadminima = edadminima
    self.edadmaxima = edadmaxima
    self.fechainicioplan = datetime.datetime(fechainicioplan, 1, 1).strftime("%d/%m/%Y")
    self.fechafinplan = datetime.datetime(fechafinplan, 1, 1).strftime("%d/%m/%Y")

p1 = Plan(1, 60, 80, 2021, 2022)
p2 = Plan(2, 50, 59, 2022, 2023)
p3 = Plan(3, 40, 49, 2023, 2024)
p4 = Plan(4, 30, 39, 2024, 2025)
p5 = Plan(5, 20, 29, 2025, 2026)
p6 = Plan(6, 16, 19, 2026, 2027)

listaPlanes = [p1,p2,p3,p4,p5,p6]                                                         #No olvidar agregar cada plan nuevo a la lista de planes

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


infoPlanVacunacion()
