import sqlite3
from sqlite3 import Error
from datetime import datetime
from datetime import date
import afiliacion
import lote_vacunas

def sql_prog():
    # Se crea la conexion a la base de datos y se verifica que no ocurra ningun error
    try:
        prog = sqlite3.connect('sisgenvac.db')
        return prog
    except Error:
        print(Error)

def tabla_prog(con):
    cursorObj = con.cursor()
    # Se crea una tabla para la programacion de vacunas verificando que no exista aun
    cursorObj.execute("""CREATE TABLE IF NOT EXISTS ProgramacionVacunas(noid integer, nombre text,
                      apellido text, ciudadvacunacion text,nolote integer, fabricante text,
                      fechaprogramada text, horaprogramada text)""")
    con.commit()

def infoCita(con):
    
    cursorobj = con.cursor()
    noid = input("id del afiliado: ")
    # Se verifica que el id sea un valor numerico y se encuentre dentro de la base de datos
    while True:
        if noid.isdigit():
            cursorobj.execute('SELECT * FROM afiliados where id= ' + noid)
            afil_b = cursorobj.fetchall()
            if len(afil_b) != 0:
                break
            else:
                print("El id " + str(noid) + " no se encuentra en la base de datos")
        noid = input("Ingrese un id valido: ")
    nombre = afil_b[0][1]
    apellido = afil_b[0][2]
    ciudad = afil_b[0][6]

    # Calcular edad
    nacimiento = afil_b[0][7].split("/")
    now= datetime.now()
    dia = now.strftime("%d")
    mes = now.strftime("%m")
    ano = now.strftime("%Y")

    dano = (int(ano) - int(nacimiento[2]))*365
    dmes = (int(mes) - int(nacimiento[1]))*30
    ddia = int(dia) - int(nacimiento[0])
    edad = (dano + dmes + ddia)//365
    # cuadrar
    cursorobj.execute('SELECT * FROM LoteVacunas')
    lotes = cursorobj.fetchall()
    nolote = "probando"
    fabricante = "probando"
    fechaprogramada = "probando"
    horaprogramada = "probando"
    infcita = (noid, nombre, apellido, ciudad, nolote, fabricante, fechaprogramada, horaprogramada)
    return infcita

def asignarVacuna(con, info):
    # Se asigna la cita para la vacuna con la informacion del usuario y la vacuna
    cursorObj = con.cursor()
    cursorObj.execute("""INSERT INTO ProgramacionVacunas(noid, nombre, apellido,
                      ciudadvacunacion, nolote, fabricante, fechaprogramada, horaprogramada)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", info)
    con.commit()


def menu(con):
    salir=False
    while not salir:
        opc=(input('''  Menú de programación de citas
                        1.Tipo de identificación del afiliado
                        2.Número de identificación del afiliado
                        3.Ciudad de vacunación
                        4.Salir

                        Ingrese su opción: '''))
        if (opc=='1'):
            salirInterno=False
            while not salirInterno:
                opcInterna=(input('''  Tipo de identificación del afiliado
                        1.Cédula de ciudadanía
                        2.Tarjeta de identidad
                        3.Salir

                        Ingrese su opción: '''))
                if (opcInterna=='1'):
                    print("Usted ha seleccionado la opción: Cédula de ciudadanía")
                    salirInterno=True
                elif (opcInterna=='2'):
                    print("Usted ha seleccionado la opción: Tarjeta de identidad")
                    salirInterno=True
                elif (opcInterna=='3'):
                    salirInterno=True

        if (opc=='2'):
            salirInterno=False
            while not salirInterno:
                opcInterna=(input('''  Ingrese el número de identificación del afiliado: '''))
                opcInterna=opcInterna.ljust(12)
                salirInterno=True

        if (opc=='3'):
            salirInterno=False
            while not salirInterno:
                opcInterna=(input('''  Ingrese la ciudad de vacunación para el afiliado: '''))
                opcInterna=opcInterna.ljust(20)
                salirInterno=True

        if (opc=='4'):
            salirInterno=True

#def main():
    #prog = sql_prog()
    #tabla_prog(prog)
    #info = infoCita(prog)
    #asignarVacuna(prog, info)
    
#main()
