import sqlite3
from sqlite3 import Error

def sql_lotevacunas():
    try:
        convacunas = sqlite3.connect('BDLote_vacunas.db')
        return convacunas
    except Error:
        print(Error)

def tabla_vacunas(con):
    cursorObj = con.cursor()
    cursorObj.execute("""CREATE TABLE IF NOT EXISTS LoteVacunas(nolote integer PRIMARY KEY, fabricante text,
                      tipovacuna text, cantidadrecibida integer, cantidadusada integer, dosisnecesarias integer,
                      temperatura text, efectividad text, tiempoproteccion text, fechavencimiento text)""")
    con.commit()

def info_lote():
    nolote = input("Numero de lote: ")
    nolote = nolote.ljust(12)
    
    # Se muestran las opciones de vacunas y se asignan los valores predeterminados a las variables
    op_fabricante = int(input("""Fabricante:\n
    \t1 - Sinovac
    \t2 - Pfizer
    \t3 - Moderna
    \t4 - Sputnik V
    \t5 - AstraZeneca
    \t6 - Sinopharm
    \t7 - Covaxim\n\nSeleccione una opcion: """))
    if op_fabricante == 1:
        fabricante = "Sinovac"
        dosisnecesarias = 2
        temperatura = "2 a 8°C"
        efectividad = "78%"
        tiempoproteccion = "120 dias"
    elif op_fabricante == 2:
        fabricante = "Pfizer"
        dosisnecesarias = 2
        temperatura = "-25 a -15°C"
        efectividad = "95%"
        tiempoproteccion = "210 dias"
    elif op_fabricante == 3:
        fabricante = "Moderna"
        dosisnecesarias = 2
        temperatura = "-20°C"
        efectividad = "94%"
        tiempoproteccion = "238 dias"
    elif op_fabricante == 4:
        fabricante = "Sputnik V"
        dosisnecesarias = 2
        temperatura = "-18°C"
        efectividad = "92%"
        tiempoproteccion = "238 dias"
    elif op_fabricante == 5:
        fabricante = "AstraZeneca"
        dosisnecesarias = 2
        temperatura = "2 a 8°C"
        efectividad = "70%"
        tiempoproteccion = "120 dias"
    elif op_fabricante == 6:
        fabricante = "Sinopharm"
        dosisnecesarias = 2 
        temperatura = "2 a 8°C"
        efectividad = "80%"
        tiempoproteccion = "120 dias"
    elif op_fabricante == 7:
        fabricante = "Covaxim"
        dosisnecesarias = 2
        temperatura = "2 a 8°C"
        efectividad = "81%"
        tiempoproteccion = "180 dias"

    # Se muestran las opciones de tipos de vacunas
    op_vacuna = int(input("""Tipo de vacuna:\n
    \t1 - Vector viral
    \t2 - ARN/ADN
    \t3 - Virus desactivado
    \t4 - En base a proteinas\n\nSeleccione una opcion: """))
    if op_vacuna == 1:
        tipovacuna = "Vector viral"
    elif op_vacuna == 2:
        tipovacuna = "ARN/ADN"
    elif op_vacuna == 3:
        tipovacuna = "Virus desactivado"
    elif op_vacuna == 4:
        tipovacuna = "En base a proteinas"
    
    cantidadrecibida = input("Cantidad recibida: ")
    cantidadrecibida = cantidadrecibida.ljust(6)
    cantidadusada = 0
    diaven = input("Fecha de vencimiento\nDia de vencimiento: ")
    diaven = diaven.rjust(2,"0")
    mesven = input("Mes de vencimiento: ")
    mesven = mesven.rjust(2,"0")
    anoven = input("ano de vencimiento: ")
    anoven = anoven.rjust(2,"0")
    fechavencimiento = diaven+"/"+mesven+"/"+anoven
    lote = (nolote, fabricante, tipovacuna, cantidadrecibida, cantidadusada, dosisnecesarias, temperatura, efectividad, tiempoproteccion, fechavencimiento)
    return lote

def crear_lote(con, lote):
    cursorObj = con.cursor()
    cursorObj.execute("""INSERT INTO LoteVacunas(nolote, fabricante, tipovacuna,
                      cantidadrecibida, cantidadusada, dosisnecesarias, temperatura, efectividad,
                      tiempoproteccion, fechavencimiento)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", lote)
    con.commit()


def main():
    convacunas = sql_lotevacunas()
    tabla_vacunas(convacunas)
    lote = info_lote()
    crear_lote(convacunas, lote)

main()

    
