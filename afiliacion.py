from datetime import datetime
from datetime import date
import sqlite3
from sqlite3 import Error
import re


def sql_afiliado():
    # funcion que crea la base de datos
    try:
        con = sqlite3.connect('sisgenvac.db')
        #print("Conexion realizada: DB creada")
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
    # funcion valida el formato del correo
    regex = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    mailvalido = (re.search(regex, email))
    return mailvalido


def leer_info():
    while True:
        try:
            ident = int(input("Número de identificación: "))
        except ValueError:
            print("escriba un número de identificacion valido.")
            continue
        else:
            break

    name = False
    # bucle para pedir el nombre
    while not name:
        # mensaje para que el usuario sepa que le solicitamos el nombre
        nombre = (input("Nombre: "))



        name = (nombre.replace(" ", "")).isalpha()
        nombre = nombre.ljust(20)

        if not name or len(nombre) > 20:
            name = False
            print("\nEscriba un Nombre Valido")

    lastname = False
    # bucle para pedir el apellido
    while not lastname:
        # mensaje para que el usuario sepa que le solicitamos el nombre
        apellido = (input("Apellido: "))
        lastname = (apellido.replace(" ", "")).isalpha()
        apellido = apellido.ljust(20)

        if not lastname or len(apellido) > 20:
            lastname = False
            print("\nEscriba un Apellido Valido")

    direccion = (input("direccion: "))

    while True:
        try:
            telefono = int(input("Telefono: "))
        except ValueError:
            print("Escriba un numero de telefono valido.")
            continue
        else:
            break
    # variable que indica si el valor es válido
    # inicialmente no lo es
    valido = False
    # bucle para pedir el valor
    while not valido:
        # mensaje para que el usuario sepa que le solicitamos un correo
        email = (input("Correo electronico: "))
        valido = es_correo_valido(email)
        if not valido:
            print("\nescriba un correo valido: ")
    ciudad = (input("ciudad: "))

    # mensaje para que el usuario sepa que le solicitamos el dia de nacimiento
    dianac = (input("Dia de Nacimiento DD: "))
    # bucle para pedir el dia de nacimiento
    while True:
        if dianac.isdigit() and 0<int(dianac)<32:
            dianac = dianac.rjust(2,"0")
            break
        else:
            dianac = input("\nEscriba el dia de nacimiento en dos digitos: ")
            
    # mensaje para que el usuario sepa que le solicitamos el mes de nacimiento
    mesnac = (input("Mes de Nacimiento MM: "))
    # bucle para pedir el mes de nacimiento
    while True:
        if mesnac.isdigit() and 0<int(mesnac)<13:
            mesnac = mesnac.rjust(2,"0")
            break
        else:
            mesnac = input("\nEscriba el mes de nacimiento en numeros entre el 1 y 12: ")

    # mensaje para que el usuario sepa que le solicitamos el año de nacimiento
    anonac = (input("Año de Nacimiento YYYY: "))
    # bucle para pedir el año de nacimiento
    while True:
        if anonac.isdigit() and len(anonac) == 4:
            anonac = anonac.rjust(4)
            break
        else:
            anonac = input("\nEscriba el año de nacimiento en numeros AAAA: ")

    nacimiento = dianac + "/" + mesnac + "/" + anonac
    print("nacimiento", nacimiento)


# se actualiza la fecha de afiliacion automaticamente
    f = datetime.now()
    dia = str(f.day).rjust(2, "0")
    mes = str(f.month).rjust(2, "0")
    ano = str(f.year).rjust(2, "0")
    afiliacion = dia + "/" + mes + "/" + ano
    print("la fecha de afiliacion es: ", afiliacion)

    desafiliacion = " "

    # Por defecto el usuario  ingresa como no  vacunado
    vacunado = "N"
    
    '''salir = False

    salir = False
    while not salir:
        vacunado = (input("fue vacunado?"))
        if vacunado == 'N' or vacunado == 'n':
            salir = True'''
    newafi = (ident, nombre, apellido, direccion, telefono, email, ciudad, nacimiento, afiliacion, desafiliacion, vacunado)
    return newafi


def insertar_tabla(con, newafi):
    """ Funcion que se utiliza para operar en la base de datos"""
    cursorobj = con.cursor()
    cursorobj.execute('''INSERT INTO afiliados (id ,nombre,apellidos ,direccion,telefono ,email, ciudad ,nacimiento,
    afiliacion,desafiliacion,vacunado) VALUES(?, ?, ?, ?,?,?,?, ?, ?, ?,?)''', newafi)
    con.commit()


def vacunar(con):
    """ Funcion que se utiliza para operar en la base de datos"""
    cursorobj = con.cursor()
    vacunado = input("identificacion del afiliado vacunado: ")
    actualizar = 'update afiliados SET vacunado = "s" where id ='+vacunado
    cursorobj.execute(actualizar)
    print("El afiliado ", vacunado, "fue vacunado")
    con.commit()


def desafiliar(con):
    """ Funcion que se utiliza para operar en la base de datos"""
    cursorobj = con.cursor()
    desafiliado = input("identificacion del usuario a desafiliar: ")
    f = datetime.now()
    dia = str(f.day).rjust(2, "0")
    mes = str(f.month).rjust(2, "0")
    ano = str(f.year).rjust(2, "0")
    desafiliacion = dia + "/" + mes + "/" + ano
    print("la fecha de afiliacion es: ", desafiliacion)
    actualizar = 'update afiliados SET desafiliacion = (?)  where id=(?)'
    cursorobj.execute(actualizar,(desafiliacion,desafiliado))




    print("El afiliado ", desafiliado, "fue desafiliado")
    con.commit()


def consulta(con):
    cursorobj = con.cursor()
    c_afilia = input("id del afiliado a consultar: ")
    # Verifiar que el id ingresado se encuentre en la base de datos
    while True:
        if c_afilia.isdigit():
            buscar = 'SELECT * FROM afiliados where id= ' + c_afilia
            cursorobj.execute(buscar)
            afil_b = cursorobj.fetchall()
            if len(afil_b) != 0:
                break
            else:
                print("El id " + str(c_afilia) + " no se encuentra en la base de datos")
        c_afilia = input("Ingrese un id valido: ")
        
    
    print("+{:-<12}+{:-<20}+{:-<20}+{:-<30}+{:-<15}+{:-<25}+{:-<20}+{:-<10}+{:-<10}+{:-<15}+{:-<10}+".format("", "", "", "","", "", "", "","", "", ""))
    print("|{:^12}|{:^20}|{:^20}|{:^30}|{:^15}|{:^25}|{:^20}|{:^10}|{:^10}|{:^15}|{:^10}|".format("Documento", "Nombre", "Apellido", "Direccion", "Telefono", "Email", "Ciudad","Nacimiento", "Afiliacion","Desafiliacion","Vacunado"))
    print("+{:-<12}+{:-<20}+{:-<20}+{:-<30}+{:-<15}+{:-<25}+{:-<20}+{:-<10}+{:-<10}+{:-<15}+{:-<10}+".format("", "", "", "","", "", "", "","", "", ""))
    for idaf, nombre, apellido, direccion, telefono, email, ciudad, nacimiento,afiliacion, desafiliacion, vacunado in afil_b:

        print("|{:^12}|{:^20}|{:^20}|{:^30}|{:^15}|{:^25}|{:^20}|{:^10}|{:^10}|{:^15}|{:^10}|".format(idaf, nombre, apellido,
                      direccion, telefono, email, ciudad, nacimiento,
                      afiliacion, desafiliacion, vacunado))
    print("+{:-<12}+{:-<20}+{:-<20}+{:-<30}+{:-<15}+{:-<25}+{:-<20}+{:-<10}+{:-<10}+{:-<15}+{:-<10}+".format("", "", "", "","", "", "", "","", "", ""))
    con.commit()


def cerrar_db(con):
    con.close()


#def main():
    con = sql_afiliado()
    #creartable(con)
    #afiliado = leer_info()
    #insertar_tabla(con, afiliado)
    #consulta(con)
    #cerrar_db(con)
#main()

