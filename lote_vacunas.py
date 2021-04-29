import sqlite3
from sqlite3 import Error

def sql_lotevacunas():
    try:
        convacunas = sqlite3.connect('sisgenvac.db')
        return convacunas
    except Error:
        print(Error)

def tabla_vacunas(con):
    cursorObj = con.cursor()
    cursorObj.execute("""CREATE TABLE IF NOT EXISTS LoteVacunas(nolote integer PRIMARY KEY, fabricante text,
                      tipovacuna text, cantidadrecibida integer, cantidadusada integer, dosisnecesarias integer,
                      temperatura text, efectividad text, tiempoproteccion text, fechavencimiento text, imagen text)""")
    con.commit()

def info_lote():
    print("Ingrese la informacion del lote:\n")
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
        tipovacuna = "Virus desactivado"
        dosisnecesarias = 2
        temperatura = "2 a 8°C"
        efectividad = "78%"
        tiempoproteccion = "120 dias"
    elif op_fabricante == 2:
        fabricante = "Pfizer"
        tipovacuna = "En base a proteinas"
        dosisnecesarias = 2
        temperatura = "-25 a -15°C"
        efectividad = "95%"
        tiempoproteccion = "210 dias"
    elif op_fabricante == 3:
        fabricante = "Moderna"
        tipovacuna = "ARN/ADN"
        dosisnecesarias = 2
        temperatura = "-20°C"
        efectividad = "94%"
        tiempoproteccion = "238 dias"
    elif op_fabricante == 4:
        fabricante = "Sputnik V"
        tipovacuna = "Vector viral"
        dosisnecesarias = 2
        temperatura = "-18°C"
        efectividad = "92%"
        tiempoproteccion = "238 dias"
    elif op_fabricante == 5:
        fabricante = "AstraZeneca"
        tipovacuna = "Vector viral"
        dosisnecesarias = 2
        temperatura = "2 a 8°C"
        efectividad = "70%"
        tiempoproteccion = "120 dias"
    elif op_fabricante == 6:
        fabricante = "Sinopharm"
        tipovacuna = "Virus desactivado"
        dosisnecesarias = 2 
        temperatura = "2 a 8°C"
        efectividad = "80%"
        tiempoproteccion = "120 dias"
    elif op_fabricante == 7:
        fabricante = "Covaxim"
        tipovacuna = "Virus desactivado"
        dosisnecesarias = 2
        temperatura = "2 a 8°C"
        efectividad = "81%"
        tiempoproteccion = "180 dias"
    
    cantidadrecibida = input("Cantidad recibida: ")
    cantidadrecibida = cantidadrecibida.ljust(6)
    cantidadusada = 0
    diaven = input("Fecha de vencimiento:\n- Dia de vencimiento: ")
    diaven = diaven.rjust(2,"0")
    mesven = input("- Mes de vencimiento: ")
    mesven = mesven.rjust(2,"0")
    anoven = input("- ano de vencimiento: ")
    anoven = anoven.rjust(4)
    fechavencimiento = diaven+"/"+mesven+"/"+anoven
    print("Fecha ingresada: " + fechavencimiento)
    imagen = input("Ingrese la ruta de la imagen de una vacuna: ")
    print("Funcion de imagen en desarrollo, proximamente mas funcional...")
    lote = (nolote, fabricante, tipovacuna, cantidadrecibida, cantidadusada, dosisnecesarias, temperatura, efectividad, tiempoproteccion, fechavencimiento, imagen)
    return lote

def crear_lote(con, lote):
    cursorObj = con.cursor()
    cursorObj.execute("""INSERT INTO LoteVacunas(nolote, fabricante, tipovacuna,
                      cantidadrecibida, cantidadusada, dosisnecesarias, temperatura, efectividad,
                      tiempoproteccion, fechavencimiento, imagen)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", lote)
    con.commit()

def consultar_lote(con):
    cursorObj = con.cursor()
    c_lote = input("Numero de lote a consultar: ")
    cursorObj.execute('SELECT * FROM LoteVacunas where nolote= ' + c_lote)
    filas = cursorObj.fetchall()
    
    for ver in filas:
        vnolote = ver[0]
        vfabricante = ver[1]
        vtipovacuna = ver[2]
        vcantidadrecibida = ver[3]
        vcantidadusada = ver[4]
        vdosisnecesarias = ver[5]
        vtemperatura = ver[6]
        vefectividad = ver[7]
        vtiempoproteccion = ver[8]
        vfechavencimiento = ver[9]
        vimagen = ver[10]

    print("\n          INFORMACION DEL LOTE " , vnolote, "\n")
    print("- No. lote: ", vnolote)
    print("- Fabricante: ", vfabricante)
    print("- Tipo de vacuna: ", vtipovacuna)
    print("- Cantidad recibida: ", vcantidadrecibida)
    print("- Cantidad usada: ", vcantidadusada)
    print("- Dosis necesarias: ", vdosisnecesarias)
    print("- Temperatura de almacenamiento: ", vtemperatura)
    print("- Efectividad: ", vefectividad)
    print("- Tiempo de proteccion: ", vtiempoproteccion)
    print("- Fecha de vencimiento: ", vfechavencimiento)
    print("- Imagen(enlace): ", vimagen)
        
    con.commit()


#def main():
    #convacunas = sql_lotevacunas()
    #tabla_vacunas(convacunas)
    #lote = info_lote()
    #crear_lote(convacunas, lote)
    #consultar_lote(convacunas)

    
