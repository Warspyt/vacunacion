""" Se importan las librerias para el manejo de las bases de datos, las fechas, envio de correos
    electronicos y las conexiones con los modulos de afiliacion y lotes de vacunas"""
from datetime import datetime
from datetime import date
import sqlite3
from sqlite3 import Error
import re


"""def VerTipDatoAlpha(self):
    if dato.isalpha() == false:
        tipo = "alfabetico"
        sel
        """


class Afiliado:
    def __init__(self, con):
        self.__conexion = con
        self.__cursorObj = con.cursor()
        self.__ident = ""
        self.__nombre = ""
        self.__apellido = ""
        self.__direccion = ""
        self.__telefono = ""
        self.__email = ""
        self.__ciudad = ""
        self.__nacimiento = ""
        self.__afiliacion = ""
        self.__desafiliacion = ""
        self.__vacunado = ""

    """ Acceso privado al cursor de la db"""

    def getcursorObj(self):
        return self.__cursorObj

    def getconexion(self):
        return self.__conexion
    """ Acceso privado al numero de identificacion"""
    def setident(self, ident):
        self.__ident = ident

    def getident(self):
        return self.__ident
    """ Acceso privado al nombre"""
    def setnombre(self, nombre):
        self.__nombre = nombre

    def getnombre(self):
        return self.__nombre

    """ Acceso privado al apellido"""
    def setapellido(self):
        return self.__apellido

    def getapellido(self):
        return self.__apellido

    """ Acceso privado al direccion"""

    def setdireccion(self, direccion):
        self.__direccion = direccion

    def getdireccion(self):
        return self.__direccion

    """ Acceso privado al telefono"""

    def settelefono(self, telefono):
        self.__telefono = telefono

    def gettelefono(self):
        return self.__telefono

    """ Acceso privado al email"""

    def setemail(self, email):
        self.__email = email

    def getemail(self):
        return self.__email

    """ Acceso privado ciudad"""

    def setciudad(self, ciudad):
        self.__ciudad = ciudad

    def getciudad(self):
        return self.__ciudad

    """ Acceso privado al nacimiento"""

    def setnacimiento(self, nacimiento):
        self.__nacimiento = nacimiento

    def getnacimiento(self):
        return self.__nacimiento

    """ Acceso privado al afiliacion"""

    def setafiliacion(self, afiliacion):
        self.__afiliacion = afiliacion

    def getafiliacion(self):
        return self.__afiliacion
    """ Acceso privado al desafiliacion"""

    def setdesafiliacion(self, desafiliacion):
        self.__desafiliacion = desafiliacion

    def getdesafiliacion(self):
        return self.__desafiliacion
    """ Acceso privado al vacunado"""

    def setvacunado(self, vacunado):
        self.__vacunado = vacunado

    def getvacunado(self):
        return self.__vacunado

    def leer_info(self):

        """ Funcion para guardar la informacion que se le solicita al usuario
            sobre un afiliado que se creara """

        while True:
            """ Por medio de un bucle se verifica que el dato ingresado para la identificacion sea valor numerico
                    y una longitud  max de de 13 caracteres"""
            try:
                ident = int(input("Número de identificación: "))
                lenid = str(ident)

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
            ''' Por medio de un bucle se verifica que el dato ingresado para el nombre sea valor un caracter alfabetico
                            y una longitud  max de de 20 caracteres'''
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
            ''' Por medio de un bucle se verifica que el dato ingresado para el apellido sea valor un caracter alfabetico
                                    y una longitud  max de de 20 caracteres'''
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
            ''' Por medio de un bucle se verifica que el dato ingresado para la direccion sea valor un caracter alfanumerico
                                    y una longitud  max de de 20 caracteres, se usa un diccionario para remplazar
                                    los  simbolos y poder realizar la verificacion de la cadena'''
            # mensaje para que el usuario sepa que le solicitamos la direccion y validamso sea alfa numerica isalmun
            direccion = (input("Direccion: "))
            # adress = (direccion.replace(" ", "")).isalnum()
            dictionary = {'#': "", ' ': '', '/': "", '-': ""}
            transtable = direccion.maketrans(dictionary)
            adress = direccion.translate(transtable)
            direccion = direccion.ljust(20)
            if not adress or len(direccion) > 20:
                adress = False
                print("\nEscriba una Direccion Valida")

        while True:
            try:
                ''' Por medio de un bucle se verifica que el dato ingresado para el telefono sea valor un numero
                                                y una longitud  max de 12 caracteres'''
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
            # validacion por medio de la  funcion con regex

            valido = self.es_correo_valido(email)
            if not valido:
                print("\nescriba un correo valido: ")

        city = False
        # bucle para pedir la ciudad
        while not city:
            ''' Por medio de un bucle se verifica que el dato ingresado para el ciudad sea valor un caracter  alfabetico
                                                        y una longitud  max de 20 caracteres'''
            # mensaje para que el usuario sepa que le solicitamos la ciudad
            ciudad = (input("Ciudad: "))
            city = (ciudad.replace(" ", "")).isalpha()
            if not city or len(ciudad) > 21:
                # variable que indica si el valor es válido
                # inicialmente no lo es
                city = False
                print("\nEscriba una ciudad Valida: ")

        # mensaje para que el usuario sepa que le solicitamos el dia de nacimiento
        while True:
            ''' Por medio de un bucles se verifica que el dato ingresado parala fecha de nacimiento  sean digitos, entre
                un rango especifico como dias menores a  32, meses menores  a 13, que  el año tenga  4 digitos
                y luego se pasa a un formato  fecha'''
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
        self.__desafiliacion = " "
        # Por defecto el usuario  ingresa como no  vacunado
        self.__vacunado = "N"

        datos = (
            self.getident(), self.getnombre(), self.getapellido(), self.getdireccion(), self.gettelefono(), self.getemail(), self.getciudad(),
            self.getnacimiento(), self.getafiliacion(), self.getdesafiliacion(),
            self.getvacunado())
        return datos

    def insertar_tabla(self, datos):
        """ Se crea un nuevo afiliado con la informacion recolectada del usuario, haciendo uso del
            objeto cursor y el metodo execute que utiliza el INSERT INTO dentro de los parametros
            """


        try:
            self.getcursorObj().execute('''INSERT INTO afiliados (id ,nombre,apellidos ,direccion,telefono ,email, ciudad ,nacimiento,
            afiliacion,desafiliacion,vacunado) VALUES(?, ?, ?, ?, ?,?,?, ?, ?, ?,?)''', datos)
            self.getconexion().commit()
        except OperationalError:
            print("\nVerifique la informacion ingresada.")
            return

    def tabla_afiliados(self):
        """
                 Se crea el objeto de conexión.
                 El objeto cursor se crea utilizando el objeto de conexión
                 se ejecuta el método execute con la consulta CREATE TABLE como parámetro         """

        self.getcursorObj().execute("CREATE TABLE IF NOT EXISTS afiliados(id integer PRIMARY KEY,nombre text,apellidos text,"
                          "direccion text,telefono integer,email text, ciudad text,nacimiento text,afiliacion text,"
                          "desafiliacion text,vacunado text)")
        self.getconexion().commit()
    """
             por medio del modulo re busca  concidencias de expresiones regulares para validar los caracteres  
             y formato del  correo         """

    def vacunar(self):
        """ Funcion que se utiliza para operar en la base de datos"""

        try:
            ''' se selecciona en la  DB los registros que  no estan vacunadosy no estan desafiliados
                en caso de no encontrar  que los afiliados esten vacunados y desafiliados nos indicara que no hay 
                a quien vacunar'''
            self.getcursorObj().execute('SELECT * FROM afiliados where vacunado = "N" AND desafiliacion = " "')
            self.getcursorObj().fetchall()[0]
        except IndexError:
            print("\nNo hay usuarios que no se encuentren vacunados en este momento.")
            return

        ident = input("id del afiliado a vacunar: ")
        # Verifica que el id ingresado se encuentre en la base de datos y no este desafiliado
        while True:
            if ident.isdigit() and len(ident) < 13:
                buscar = 'SELECT * FROM afiliados where id= ' + ident + ' AND desafiliacion = " "'
                self.getcursorObj().execute(buscar)
                afil_b = self.getcursorObj().fetchall()
                if len(afil_b) != 0:
                    # Verificar que el afiliado no este vacunado
                    if afil_b[0][10] == 'S':
                        print("El afiliado ya se encuentra vacunado")
                        return
                    else:
                        break
                else:
                    print("\n El id " + str(ident) + " no se encuentra afiliado")
                    return
            # verificacion de longitud
            if len(ident) > 13:
                print("El numero de identificacion no puede tener mas de 12 digitos.")
            ident = input("Ingrese un id valido: ")

        vacunado = str(ident)
        print("\t1 - Registrar Vacunacion del  afiliado")
        print("\t2 - Volver al Menu  Anterior")
        option = input("Seleccione una opcion: ")
        if option == '1':
            # se hace el update del afiliado en el campo vacunado con un print informando
            sql = 'SELECT vacunado FROM afiliados WHERE id =' + vacunado
            self.getcursorObj().execute(sql)
            registros = self.getcursorObj().fetchall()

            if 'S' not in registros[0]:
                actualizar = 'update afiliados SET vacunado = "S" where id =' + vacunado

                self.getcursorObj().execute(actualizar)
                print("El afiliado ", vacunado, "fue vacunado")
                self.getconexion().commit()

            else:
                print(" El afiliado ya se encuentra vacunado")

        elif option == "2":
            return
        else:
            print("")
            input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")

    def desafiliar(self):
        """ Funcion que se utiliza para operar en la base de datos"""


        try:
            # recorremos la DB  en busqueda de registros sin desafiliacion
            self.getcursorObj().execute('SELECT * FROM afiliados where desafiliacion = " "')
            self.getcursorObj().fetchall()[0]
        except IndexError:
            print("\nNo hay usuarios registrados en este momento.")
            return

        desafiliado = input("identificacion del usuario a desafiliar: ")
        # Verifiar que el id ingresado se encuentre en la base de datos
        while True:
            if desafiliado.isdigit() and len(desafiliado) < 13:
                buscar = 'SELECT * FROM afiliados where id= ' + desafiliado + ' AND desafiliacion = " "'
                self.getcursorObj().execute(buscar)
                afil_b = self.getcursorObj().fetchall()
                if len(afil_b) != 0:
                    break
                else:
                    print(
                        "El id " + str(desafiliado) + " no se encuentra en la base de datos o ya se encuentra desafiliado")
                return
            if len(desafiliado) > 13:
                print("El numero de identificacion no puede tener mas de 12 digitos.")
            desafiliado = input("Ingrese un id valido: ")
        f = datetime.now()
        dia = str(f.day).rjust(2, "0")
        mes = str(f.month).rjust(2, "0")
        ano = str(f.year).rjust(2, "0")
        desafiliacion = dia + "/" + mes + "/" + ano
        print("la fecha de desafiliacion es: ", desafiliacion)
        actualizar = 'update afiliados SET desafiliacion = (?)  where id=(?)'
        self.getcursorObj().execute(actualizar, (desafiliacion, desafiliado))
        print("El afiliado ", desafiliado, "fue desafiliado")
        self.getconexion().commit()

    ''' Funcion para consultar la informacion de los afiliados,
        la cual toma como parametro la conexion con la base de datos del programa'''

    def consulta(self):

        try:
            # recorre la DB para verificar que no este vacia
            self.getcursorObj().execute('SELECT * FROM afiliados')
            self.getcursorObj().fetchall()[0]
        except IndexError:

            print("\nNo hay usuarios registrados en este momento.")
            return

        ident = input("Número de identificación: ")
        lenid = str(ident)

        if len(lenid) > 13:
            print("El numero de identificacion no puede tener mas de 12  digitos.")
            return
        # Verifica que el id ingresado se encuentre en la base de datos
        while True:
            if ident.isdigit():
                buscar = 'SELECT * FROM afiliados where id= ' + ident
                self.getcursorObj().execute(buscar)
                afil_b = self.getcursorObj().fetchall()
                if len(afil_b) != 0:
                    break
                else:
                    print("El id " + str(ident) + " no se encuentra en la base de datos")
            ident = input("Ingrese un id valido: ")

        # muestra la informacion del afiliado consultado

        print("+{:-<12}+{:-<20}+{:-<20}+{:-<30}+{:-<12}+{:-<25}+{:-<20}+{:-<10}+{:-<10}+{:-<15}+{:-<10}+".format("", "", "",
                                                                                                                 "", "", "",
                                                                                                                 "", "", "",
                                                                                                                 "", ""))
        print("|{:^12}|{:^20}|{:^20}|{:^30}|{:^12}|{:^25}|{:^20}|{:^10}|{:^10}|{:^15}|{:^10}|".format("Documento", "Nombre",
                                                                                                      "Apellido",
                                                                                                      "Direccion",
                                                                                                      "Telefono", "Email",
                                                                                                      "Ciudad",
                                                                                                      "Nacimiento",
                                                                                                      "Afiliacion",
                                                                                                      "Desafiliacion",
                                                                                                      "Vacunado"))
        print("+{:-<12}+{:-<20}+{:-<20}+{:-<30}+{:-<12}+{:-<25}+{:-<20}+{:-<10}+{:-<10}+{:-<15}+{:-<10}+".format("", "", "",
                                                                                                                 "", "", "",
                                                                                                                 "", "", "",
                                                                                                                 "", ""))
        for idaf, nombre, apellido, direccion, telefono, email, ciudad, nacimiento, afiliacion, desafiliacion, vacunado in afil_b:
            print("|{:^12}|{:^20}|{:^20}|{:^30}|{:^12}|{:^25}|{:^20}|{:^10}|{:^10}|{:^15}|{:^10}|".format(idaf, nombre,
                                                                                                          apellido,
                                                                                                          direccion,
                                                                                                          telefono, email,
                                                                                                          ciudad,
                                                                                                          nacimiento,
                                                                                                          afiliacion,
                                                                                                          desafiliacion,
                                                                                                          vacunado))
        print("+{:-<12}+{:-<20}+{:-<20}+{:-<30}+{:-<12}+{:-<25}+{:-<20}+{:-<10}+{:-<10}+{:-<15}+{:-<10}+".format("", "", "",
                                                                                                                 "", "", "",
                                                                                                                 "", "", "",
                                                                                                                 "", ""))
        self.getconexion().commit()

    def es_correo_valido(self, email):
        # funcion valida el formato del correo
        regex = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        mailvalido = (re.search(regex, email))
        return mailvalido

# def cerrar_db(con):
    # con.close()

# def main():
# con = sql_afiliado()
# tabla_afiliados(con)
# afiliado = leer_info()
# insertar_tabla(con, afiliado)
# consulta(con)
# cerrar_db(con)
# main()