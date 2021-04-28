from datetime import datetime
import sqlite3
from sqlite3 import Error
import re


def sql_connection():
    # funcion que crea la base de datos
    try:
        con = sqlite3.connect('sisgenvac.db')
        return con
    except Error:
        print('Se ha producido un error al crear la conexion', Error)


def creartable(con):
    """
             Se crea el objeto de conexión.
             El objeto cursor se crea utilizando el objeto de conexión
             se ejecuta el método execute con la consulta CREATE TABLE como parámetro         """
    cursorobj = con.cursor()
    cursorobj.execute("CREATE TABLE IF NOT EXISTS afiliados(id integer PRIMARY KEY,nombre text,apellidos text,"
                      "direccion text,telefono integer,email text, ciudad text,nacimiento text,afiliacion text,"
                      "desafiliacion text,vacunado text)")
    con.commit()


def es_correo_valido(email):
    regex = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    if (re.search(regex, email)):
        print("email valido")

    else:
        print("email no sirve")


def leer_info():
    while True:
        try:
            ident = int(input("Número de identificación: "))
        except ValueError:
            print("escriba un número de identificacion valido.")
            continue
        else:
            break


    nombre = (input("nombre"))
    nombre = nombre.ljust(20)
    apellido = (input("apellido"))
    apellido = apellido.ljust(20)
    direccion = (input("direccion"))
    direccion = direccion.ljust(20)


    while True:
        try:
            telefono = int(input("Telefono: "))
        except ValueError:
            print("Escriba un numero de telefono valido.")
            continue
        else:
            break

    email = (input("Correo electronico: "))
    #email = email.ljust(20)
    es_correo_valido(email)



    ciudad = (input("ciudad"))
    ciudad = ciudad.ljust(20)
    dianac = (input("dia nacimiento:  "))
    dianac = dianac.rjust(2, "0")
    mesnac = (input("mes nacimiento:  "))
    mesnac = mesnac.rjust(2, "0")
    anonac = (input("ano nacimiento:  "))
    anonac = anonac.rjust(4)
    nacimiento = dianac+"/"+mesnac+"/"+anonac
    print("nacimiento", nacimiento)

    # se actualiza la fecha de afiliacion automaticamente
    f = datetime.now()
    dia = str(f.day).rjust(2, "0")
    mes = str(f.month).rjust(2, "0")
    ano = str(f.year).rjust(2, "0")
    afiliacion = dia + "/" + mes + "/" + ano
    print("la fecha formateada es:", afiliacion)

    desafiliacion = (input("desafiliacion"))
    salir = False
    while not salir:
        vacunado = (input("fue vacunado?"))
        if vacunado == 'N' or vacunado == 'n':
            salir = True
    newafi = (ident, nombre, apellido, direccion, telefono, email, ciudad, nacimiento, afiliacion, desafiliacion, vacunado)
    return newafi


def insertar_tabla(con, newafi):
    """ Funcion que se utiliza para operar en la base de datos"""
    cursorobj = con.cursor()
    cursorobj.execute('''INSERT INTO afiliados (id ,nombre,apellidos ,direccion,telefono ,email, ciudad ,nacimiento,
    afiliacion,desafiliacion,vacunado) VALUES(?, ?, ?, ?,?,?,?, ?, ?, ?,?)''', newafi)
    con.commit()


def update_table(con):
    """ Funcion que se utiliza para operar en la base de datos"""
    cursorobj = con.cursor()
    vacunado = input("identificacion del afiliado vacunado: ")
    actualizar = 'update afiliados SET vacunado = "s" where id ='+vacunado
    cursorobj.execute(actualizar)
    con.commit()


def consulta(con):
    cursorobj = con.cursor()
    afiliad = input("id del afiliado a consultar: ")
    buscar = 'SELECT * FROM afiliados where id= '+afiliad
    cursorobj.execute(buscar)
    filas = cursorobj.fetchall()
    print("Vere:  ", len(filas), " filas")
    for row in filas:
        print("el tipo de datos de row es:", type(row))
        identificacion = row[0]
        nombre = row[1]
        print(" la info de la tupla es: ", identificacion, " y ", nombre)

        print(row)
    con.commit()


def cerrar_db(con):
    con.close()


def main():
    con = sql_connection()
    creartable(con)
    #afiliado = leer_info()
    #insertar_tabla(con, afiliado)
    #update_table(con)
    # consulta(con)
    cerrar_db(con)


main()
