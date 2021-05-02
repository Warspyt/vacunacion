import sqlite3
from sqlite3 import Error
from datetime import datetime
from datetime import date

def sql_lotevacunas():
    # Se crea la conexion a la base de datos y se verifica que no ocurra ningun error
    try:
        convacunas = sqlite3.connect('sisgenvac.db')
        return convacunas
    except Error:
        print(Error)

def tabla_vacunas(con):
    cursorObj = con.cursor()
    # Se crea una tabla para el lote de vacunas verificando que no exista aun
    cursorObj.execute("""CREATE TABLE IF NOT EXISTS LoteVacunas(nolote integer PRIMARY KEY, fabricante text,
                      tipovacuna text, cantidadrecibida integer, cantidadusada integer, dosisnecesarias integer,
                      temperatura text, efectividad text, tiempoproteccion text, fechavencimiento text, imagen text)""")
    con.commit()

def info_lote():
    # Se recolecta la informacion del lote que se va a crear
    print("Ingrese la informacion del lote:\n")
    nolote = input("Numero de lote: ")
    # Se verifica que el numero de lote sea un valor numerico
    while True:
        if nolote.isdigit() and len(nolote) <= 12:
            nolote = nolote.ljust(12)
            break
        else:
            nolote = input("Ingrese un numero de lote valido: ")            
    
    # Se muestran las opciones de vacunas y se asignan los valores predeterminados a las variables
    op_fabricante = input("""Seleccione un fabricante:\n
    \t1 - Sinovac
    \t2 - Pfizer
    \t3 - Moderna
    \t4 - Sputnik V
    \t5 - AstraZeneca
    \t6 - Sinopharm
    \t7 - Covaxim\n\nSeleccione una opcion: """)
    # Se verifica que el valor ingresado se un numero y este entre las opciones
    while True:
        if op_fabricante.isdigit() and 0<int(op_fabricante)<8:
            break
        else:
            op_fabricante = input("Ingrese una opcion valida: ")
    if op_fabricante == '1':
        fabricante = "Sinovac"
        tipovacuna = "Virus desactivado"
        dosisnecesarias = 2
        temperatura = "2 a 8°C"
        efectividad = "78%"
        tiempoproteccion = "120 dias"
    elif op_fabricante == '2':
        fabricante = "Pfizer"
        tipovacuna = "En base a proteinas"
        dosisnecesarias = 2
        temperatura = "-25 a -15°C"
        efectividad = "95%"
        tiempoproteccion = "210 dias"
    elif op_fabricante == '3':
        fabricante = "Moderna"
        tipovacuna = "ARN/ADN"
        dosisnecesarias = 2
        temperatura = "-20°C"
        efectividad = "94%"
        tiempoproteccion = "238 dias"
    elif op_fabricante == '4':
        fabricante = "Sputnik V"
        tipovacuna = "Vector viral"
        dosisnecesarias = 2
        temperatura = "-18°C"
        efectividad = "92%"
        tiempoproteccion = "238 dias"
    elif op_fabricante == '5':
        fabricante = "AstraZeneca"
        tipovacuna = "Vector viral"
        dosisnecesarias = 2
        temperatura = "2 a 8°C"
        efectividad = "70%"
        tiempoproteccion = "120 dias"
    elif op_fabricante == '6':
        fabricante = "Sinopharm"
        tipovacuna = "Virus desactivado"
        dosisnecesarias = 2 
        temperatura = "2 a 8°C"
        efectividad = "80%"
        tiempoproteccion = "120 dias"
    elif op_fabricante == '7':
        fabricante = "Covaxim"
        tipovacuna = "Virus desactivado"
        dosisnecesarias = 2
        temperatura = "2 a 8°C"
        efectividad = "81%"
        tiempoproteccion = "180 dias"
    
    cantidadrecibida = input("Cantidad recibida: ")
    # Se verifica que el valor ingresado sea numerico
    while True:
        if cantidadrecibida.isdigit() and len(cantidadrecibida) <= 6:
            cantidadrecibida = cantidadrecibida.ljust(6)
            break
        else:
            cantidadrecibida = input("Ingrese una cantidad valida: ")
            
    cantidadusada = 0

    # Verificar que la fecha de vencimiento sea posterior a la fecha actual
    while True:

        diaven = input("Fecha de vencimiento:\n\n- Dia de vencimiento: ")
        # Se verifica que el dato ingresado sea un dia existente dentro del calendario
        while True:
            if diaven.isdigit() and 0<int(diaven)<32:
                diaven = diaven.rjust(2,"0")
                break
            else:
                diaven = input("Escriba el dia de vencimiento en dos digitos: ")
        mesven = input("- Mes de vencimiento: ")
        # Se verifica que el dato ingresado sea un mes existente dentro del calendario
        while True:
            if mesven.isdigit() and 0<int(mesven)<13:
                mesven = mesven.rjust(2,"0")
                break
            else:
                mesven = input("Escriba el mes de vencimiento en numeros entre el 1 y 12: ")
        anoven = input("- año de vencimiento: ")
        # Se verifica que el dato ingresado sea un año coherente para el vencimiento
        while True:
            if anoven.isdigit() and len(anoven) == 4 and int(anoven)>2020:
                anoven = anoven.rjust(4)
                break
            else:
                anoven = input("Escriba el año de vencimiento en numeros AAAA: ")
        # Se guardan los datos de la fecha en formato (DD/MM/AAAA)
        fechavencimiento = datetime(int(anoven), int(mesven), int(diaven)).strftime("%Y/%m/%d")
        factual = datetime.now().strftime("%Y/%m/%d")
        #fechavencimiento = diaven+"/"+mesven+"/"+anoven
        if fechavencimiento > factual:
            fechavencimiento = datetime(int(anoven), int(mesven), int(diaven)).strftime("%d/%m/%Y")
            break
        else:
            print("La fecha de vencimiento no es valida: ")
    print("Fecha ingresada: " + fechavencimiento)
    
    imagen = input("Ingrese la ruta de la imagen de una vacuna: ")
    print("Funcion de imagen en desarrollo, proximamente mas funcional...")
    
    #Se guardan los datos del lote creado
    lote = (nolote, fabricante, tipovacuna, cantidadrecibida, cantidadusada, dosisnecesarias, temperatura, efectividad, tiempoproteccion, fechavencimiento, imagen)
    return lote

def crear_lote(con, lote):
    # Se crea un nuevo lote con la informacion recolectada del usuario
    cursorObj = con.cursor()
    cursorObj.execute("""INSERT INTO LoteVacunas(nolote, fabricante, tipovacuna,
                      cantidadrecibida, cantidadusada, dosisnecesarias, temperatura, efectividad,
                      tiempoproteccion, fechavencimiento, imagen)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", lote)
    con.commit()

def consultar_lote(con):
    cursorObj = con.cursor()

    # Se muestran los lotes existentes en la base de datos 
    print("\n           LOTES VIGENTES\n")
    cursorObj.execute('SELECT * FROM LoteVacunas')
    listado = cursorObj.fetchall()
    datoslote = []

    # Verificar la fecha para mostrar los lotes vigentes
    factual = datetime.now().strftime("%Y/%m/%d")
    vigencia = ""
    
    for ids in listado:
        llote = (ids[9]).split("/")
        venlote = datetime(int(llote[2]), int(llote[1]), int(llote[0])).strftime("%Y/%m/%d")
        if venlote > factual: 
            print("•", ids[0])
        datoslote.append(ids[0])
    c_lote = input("\nNumero de lote a consultar: ")
    # Se verifica que el lote sea un valor numerico y se encuentre dentro de la base de datos
    while True:
        if c_lote.isdigit() and int(c_lote) in datoslote:
            break
        else:
            c_lote = input("Ingrese un numero de lote valido: ")

    # Se busca el lote en la base de datos y se extrae la informacion
    cursorObj.execute('SELECT * FROM LoteVacunas where nolote= ' + c_lote)
    filas = cursorObj.fetchall()
    lfila = (filas[0][9]).split("/")
    venfila = datetime(int(lfila[2]), int(lfila[1]), int(lfila[0])).strftime("%Y/%m/%d")
    if venfila < factual:
        print("ESTE LOTE NO SE ENCUENTRA VIGENTE\n")
        
    # Se muestra la informacion al usuario en forma de tabla

    print("+{:-<10}+{:-<15}+{:-<21}+{:-<15}+{:-<10}+{:-<8}+{:-<15}+{:-<15}+{:-<25}+{:-<15}+{:-<15}+".format("", "", "", "","", "", "", "","", "", ""))
    print("|{:^10}|{:^15}|{:^21}|{:^15}|{:^10}|{:^8}|{:^15}|{:^15}|{:^25}|{:^15}|{:^15}|".format("lote", "Fabricante", "Tipo de vacuna", "Recibidas", "Usadas", "Dosis", "Temperatura", "Efectividad","Tiempo de Proteccion","Vencimiento","imagen"))
    print("+{:-<10}+{:-<15}+{:-<21}+{:-<15}+{:-<10}+{:-<8}+{:-<15}+{:-<15}+{:-<25}+{:-<15}+{:-<15}+".format("", "", "", "","", "", "", "","", "", ""))
    for nolote, fabricante, tipovacuna,cantidadrecibida, cantidadusada, dosisnecesarias, temperatura, efectividad,tiempoproteccion, fechavencimiento, imagen in filas:

        print("|{:^10}|{:^15}|{:^21}|{:^15}|{:^10}|{:^8}|{:^15}|{:^15}|{:^25}|{:^15}|{:^15}|".format(nolote, fabricante, tipovacuna,
                      cantidadrecibida, cantidadusada, dosisnecesarias, temperatura, efectividad,
                      tiempoproteccion, fechavencimiento, imagen))
    print("+{:-<10}+{:-<15}+{:-<21}+{:-<15}+{:-<10}+{:-<8}+{:-<15}+{:-<15}+{:-<25}+{:-<15}+{:-<15}+".format("", "", "", "","", "", "", "","", "", ""))
    print(vigencia)
    con.commit()


#def main():
    #convacunas = sql_lotevacunas()
    #tabla_vacunas(convacunas)
    #lote = info_lote()
    #crear_lote(convacunas, lote)
    #consultar_lote(convacunas)
    
#main() 
    
