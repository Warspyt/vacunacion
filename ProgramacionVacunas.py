import sqlite3
from sqlite3 import Error
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


def asignarVacuna(con, info):
    # Se asigna la cita para la vacuna con la informacion del usuario y la vacuna
    cursorObj = con.cursor()
    cursorObj.execute("""INSERT INTO ProgramacionVacunas(noid, nombre, apellido,
                      ciudadvacunacion, nolote, fabricante, fechaprogramada, horaprogramada)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", info)
    con.commit()


def main():
    prog = sql_prog()
    tabla_prog(prog)
    info = infoCita(prog)
    asignarVacuna(prog, info)
    
main()
