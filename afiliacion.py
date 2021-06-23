from datetime import datetime
from datetime import date
import sqlite3
from sqlite3 import Error
import re


def sql_afiliado():
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
    # funcion valida el formato del correo
    regex = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    mailvalido = (re.search(regex, email))
    return mailvalido


def leer_info():
    while True:
        try:
            ident = int(input("Número de identificación: "))
            lenid=str(ident)

            if len(lenid) > 13:
                print("El numero de identificacion no puede tener mas de 12  digitos.")
            else:
                break
        except ValueError:
            print("escriba un número de identificacion valido.")
            continue

    name = False
    # bucle para pedir el nombre
    while not name:
        # mensaje para que el usuario sepa que le solicitamos el nombre
        nombre = (input("Nombre: "))
        name = (nombre.replace(" ", "")).isalpha()
        if not name or len(nombre) > 20:
            name = False
            print("\nEscriba un Nombre Valido")
            
    lastname = False
    # bucle para pedir el apellido
    while not lastname:
        # mensaje para que el usuario sepa que le solicitamos el apellido
        apellido = (input("Apellido: "))
        lastname = (apellido.replace(" ", "")).isalpha()
        apellido = apellido.ljust(20)
        if not lastname or len(apellido) > 20:
            lastname = False
            print("\nEscriba un Apellido Valido")

    adress = False
    # bucle para pedir la direccion
    while not adress:
        # mensaje para que el usuario sepa que le solicitamos la direccion y validamso sea alfa numerica isalmun
        direccion = (input("Direccion: "))
        #adress = (direccion.replace(" ", "")).isalnum()
        dictionary = {'#': "", ' ': '','/': "",'-': ""}
        transTable = direccion.maketrans(dictionary)
        adress = direccion.translate(transTable)
        direccion = direccion.ljust(20)
        if not adress or len(direccion) > 20:
            adress = False
            print("\nEscriba una Direccion Valida")

    while True:
        try:
            telefono = int(input("Telefono: "))
            lentel = str(telefono)

            if len(lentel) > 13:
                print("El numero de telefono no puede tener mas de 12  digitos.")
            else:
                break
        except ValueError:
            print("Escriba un numero de telefono valido.")
            continue
    # variable que indica si el valor es válido
    # inicialmente no lo es
    valido = False
    # bucle para pedir el valor
    while not valido or len(email) > 20:
        # mensaje para que el usuario sepa que le solicitamos un correo
        email = (input("Correo electronico: "))
        valido = es_correo_valido(email)
        if not valido:
            print("\nescriba un correo valido: ")

    city = False
    # bucle para pedir la ciudad
    while not city:
        # mensaje para que el usuario sepa que le solicitamos la ciudad
        ciudad = (input("Ciudad: "))
        city = (ciudad.replace(" ", "")).isalpha()
        if not city or len(ciudad) > 20:
            city = False
            print("\nEscriba una ciudad Valida: ")

    # mensaje para que el usuario sepa que le solicitamos el dia de nacimiento
    while True:

        dianac = input("Fecha de nacimiento:\n\n- Dia de nacimiento: ")
        # Se verifica que el dato ingresado sea un dia existente dentro del calendario
        while True:
            if dianac.isdigit() and 0 < int(dianac) < 32:
                dianac = dianac.rjust(2, "0")
                break
            else:
                dianac = input("Escriba el dia de nacimiento en dos digitos: ")
        mesnac = input("- Mes de nacimiento: ")
        # Se verifica que el dato ingresado sea un mes existente dentro del calendario
        while True:
            if mesnac.isdigit() and 0 < int(mesnac) < 13:
                mesnac = mesnac.rjust(2, "0")
                break
            else:
                mesnac = input("Escriba el mes de nacimiento en numeros entre el 1 y 12: ")
        anosnac = input("- año de nacimiento: ")
        # Se verifica que el dato ingresado sea un año coherente para el nacimiento
        while True:
            if anosnac.isdigit() and len(anosnac) == 4:
                anosnac = anosnac.rjust(4)
                break
            else:
                anosnac = input("Escriba el año de nacimiento en numeros AAAA: ")
        # Se guardan los datos de la fecha en formato (DD/MM/AAAA)
        nacimiento = datetime(int(anosnac), int(mesnac), int(dianac)).strftime("%Y/%m/%d")
        factual = datetime.now().strftime("%Y/%m/%d")
        # nacimiento = dianac+"/"+mesnac+"/"+anosnac
        if nacimiento < factual:
            nacimiento = datetime(int(anosnac), int(mesnac), int(dianac)).strftime("%d/%m/%Y")
            break
        else:
            print("La fecha de nacimiento no es valida: ")
    print("Fecha ingresada: " + nacimiento)


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
    try:
        cursorobj.execute('SELECT * FROM afiliados where vacunado = "N" AND desafiliacion = " "')
        total = cursorobj.fetchall()[0]
    except:
        print("\nNo hay usuarios que no se encuentren vacunados en este momento.")
        return
        
    ident = input("id del afiliado a consultar: ")
    # Verifiar que el id ingresado se encuentre en la base de datos
    while True:
        if ident.isdigit() and len(ident) < 13:

            buscar = 'SELECT * FROM afiliados where id= ' + ident
            cursorobj.execute(buscar)
            afil_b = cursorobj.fetchall()
            if len(afil_b) != 0:
                # Verificar que el afiliado no este vacunado
                if afil_b[0][10] == 'S':
                    print("El afiliado ya se encuentra vacunado")
                    return
                else:
                    break
                
            else:
                print("El id " + str(ident) + " no se encuentra en la base de datos")
                
        if len(ident) > 13:
                print("El numero de identificacion no puede tener mas de 12 digitos.")
        ident = input("Ingrese un id valido: ")
            
    vacunado=str(ident)
    print("\t1 - Registrar Vacunacion del  afiliado")
    print("\t2 - Volver al Menu  Anterior")
    option = input("Seleccione una opcion: ")
    if option == '1':
        sql = 'SELECT vacunado FROM afiliados WHERE id ='+vacunado
        cursorobj.execute(sql)
        registros = cursorobj.fetchall()

        if 'S' not in registros[0]:
            actualizar = 'update afiliados SET vacunado = "S" where id =' + vacunado
            cursorobj.execute(actualizar)
            print("El afiliado ", vacunado, "fue vacunado")
            con.commit()

        else:
            print(" El afiliado ya se encuentra vacunado")

    elif option == "2":
        return
    else:
        print("")
        input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")


def desafiliar(con):
    """ Funcion que se utiliza para operar en la base de datos"""
    cursorobj = con.cursor()
    
    try:
        cursorobj.execute('SELECT * FROM afiliados where desafiliacion = " "')
        total = cursorobj.fetchall()[0]
    except:
        print("\nNo hay usuarios registrados en este momento.")
        return
    
    desafiliado = input("identificacion del usuario a desafiliar: ")
    # Verifiar que el id ingresado se encuentre en la base de datos
    while True:
        if desafiliado.isdigit() and len(desafiliado) < 13:
            buscar = 'SELECT * FROM afiliados where id= ' + desafiliado + ' AND desafiliacion = " "'
            cursorobj.execute(buscar)
            afil_b = cursorobj.fetchall()
            if len(afil_b) != 0:
                break
            else:
                print("El id " + str(desafiliado) + " no se encuentra en la base de datos o ya se encuentra desafiliado")
            return
        if len(desafiliado) > 13:
                print("El numero de identificacion no puede tener mas de 12 digitos.")
        desafiliado = input("Ingrese un id valido: ")
    f = datetime.now()
    dia = str(f.day).rjust(2, "0")
    mes = str(f.month).rjust(2, "0")
    ano = str(f.year).rjust(2, "0")
    desafiliacion = dia + "/" + mes + "/" + ano
    print("la fecha de afiliacion es: ", desafiliacion)
    actualizar = 'update afiliados SET desafiliacion = (?)  where id=(?)'
    cursorobj.execute(actualizar, (desafiliacion, desafiliado))
    print("El afiliado ", desafiliado, "fue desafiliado")
    con.commit()


def consulta(con):
    cursorobj = con.cursor()
    try:
        cursorobj.execute('SELECT * FROM afiliados')
        total = cursorobj.fetchall()[0]
    except:
        print("\nNo hay usuarios registrados en este momento.")
        return
    
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
        
    
    print("+{:-<12}+{:-<20}+{:-<20}+{:-<30}+{:-<12}+{:-<25}+{:-<20}+{:-<10}+{:-<10}+{:-<15}+{:-<10}+".format("", "", "", "","", "", "", "","", "", ""))
    print("|{:^12}|{:^20}|{:^20}|{:^30}|{:^12}|{:^25}|{:^20}|{:^10}|{:^10}|{:^15}|{:^10}|".format("Documento", "Nombre", "Apellido", "Direccion", "Telefono", "Email", "Ciudad","Nacimiento", "Afiliacion","Desafiliacion","Vacunado"))
    print("+{:-<12}+{:-<20}+{:-<20}+{:-<30}+{:-<12}+{:-<25}+{:-<20}+{:-<10}+{:-<10}+{:-<15}+{:-<10}+".format("", "", "", "","", "", "", "","", "", ""))
    for idaf, nombre, apellido, direccion, telefono, email, ciudad, nacimiento,afiliacion, desafiliacion, vacunado in afil_b:

        print("|{:^12}|{:^20}|{:^20}|{:^30}|{:^12}|{:^25}|{:^20}|{:^10}|{:^10}|{:^15}|{:^10}|".format(idaf, nombre, apellido,
                      direccion, telefono, email, ciudad, nacimiento,
                      afiliacion, desafiliacion, vacunado))
    print("+{:-<12}+{:-<20}+{:-<20}+{:-<30}+{:-<12}+{:-<25}+{:-<20}+{:-<10}+{:-<10}+{:-<15}+{:-<10}+".format("", "", "", "","", "", "", "","", "", ""))
    con.commit()


def cerrar_db(con):
    con.close()


#def main():
    #con = sql_afiliado()
    #creartable(con)
    #afiliado = leer_info()
    #insertar_tabla(con, afiliado)
    #consulta(con)
    #cerrar_db(con)
#main()
