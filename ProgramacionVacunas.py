""" Se importan las librerias para el manejo de las bases de datos, las fechas, envio de correos
    electronicos y las conexiones con los modulos de afiliacion y lotes de vacunas"""
import sqlite3
from sqlite3 import Error
from datetime import datetime
from datetime import date
from datetime import timedelta
import afiliacion
import lote_vacunas
import smtplib

''' Funcion para establecer la conexion con la base de datos del
    programa'''


def sql_prog():
    """ Se crea la conexion a la base de datos usando el metodo connect, creando el archivo en caso de que no exista y se verifica que
        no ocurra ningun error a partir de un try - except"""
    try:
        prog = sqlite3.connect('sisgenvac.db')
        return prog
    except Error:
        print(Error)


''' Funcion para crear la tabla de la programacion de vacunas dentro de la base de datos del
    programa, la cual toma como parametro la conexion de la misma'''


def tabla_prog(con):
    """ Se crea una tabla para la programacion de vacunas verificando que no exista aun, haciendo uso del objeto cursor
        y el metodo execute que utiliza el CREATE TABLE dentro de los parametros"""
    cursorObj = con.cursor()

    cursorObj.execute("""CREATE TABLE IF NOT EXISTS ProgramacionVacunas(noid integer, nombre text,
                      apellido text, ciudadvacunacion text,direccion text, telefono integer, email text,
                      nolote integer, fabricante text, fechaprogramada text, horaprogramada text, fechaorden text)""")
    con.commit()


''' Funcion para guardar una cita asignada a un paciente en la base de datos, la cual toma
    como parametros la conexion con la base de datos y la informacion del paciente'''


def asignarvacuna(con, info):
    """ Se guarda la cita asignada con la informacion recolectada sobre el paciente, haciendo uso del
        objeto cursor y el metodo execute que utiliza el INSERT INTO dentro de los parametros"""
    cursorObj = con.cursor()

    cursorObj.execute("""INSERT INTO ProgramacionVacunas(noid, nombre, apellido,
                      ciudadvacunacion, direccion, telefono, email, nolote, fabricante,
                      fechaprogramada, horaprogramada, fechaorden)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", info)
    con.commit()


''' Funcion para generar la agendacion de citas a partir de una fecha y hora ingresadas
    por el usuario, la cual toma como parametro la conexion con la base de datos'''


def infoCita(con):
    """ Se guarda la ultima fecha y hora asignada en la agenda de citas con el metodo strftime de la libreria
        datetime y usando el objeto cursor y el metodo execute que utiliza el SELECT como parametro"""
    cursorObj = con.cursor()

    cursorObj.execute('SELECT * FROM ProgramacionVacunas')
    ultimoregistro = cursorObj.fetchall()
    if len(ultimoregistro) != 0:
        ultimoregistro = ultimoregistro[-1]
        ultfechares = ultimoregistro[9]
        ulthorares = ultimoregistro[10]
        ultimoreg = datetime(int(ultfechares[6:10]), int(ultfechares[3:5]), int(ultfechares[:2]), int(ulthorares[:2]),
                             int(ulthorares[3:5])).strftime("%Y/%m/%d %H:%M")

    ''' Se pide la fecha y hora de inicio de la agendacion de citas por medio de un bucle que se rompe
        cuando se verifica que la fecha ingresada sea mayor a la fecha actual y a la ultima fecha
        asignada dentro de la agenda'''
    while True:

        ''' Se solicita individualmente el dia, mes, año, hora y minuto verificando a partir de un bucle
            que los datos sean numericos y existan dentro del calendario y horario covencional'''
        diaprog = input("Fecha de inicio del agendamiento de citas:\n\n- Dia de inicio: ")
        while True:
            if diaprog.isdigit() and 0 < int(diaprog) < 32:
                diaprog = diaprog.rjust(2, "0")
                break
            else:
                diaprog = input("Escriba el dia de inicio en dos digitos: ")
        mesprog = input("- Mes de inicio: ")
        while True:
            if mesprog.isdigit() and 0 < int(mesprog) < 13:
                mesprog = mesprog.rjust(2, "0")
                break
            else:
                mesprog = input("Escriba el mes de inicio en numeros entre el 1 y 12: ")
        anoprog = input("- año de inicio: ")
        while True:
            if anoprog.isdigit() and len(anoprog) == 4 and int(anoprog) > 2020:
                anoprog = anoprog.rjust(4)
                break
            else:
                anoprog = input("Escriba el año de inicio en numeros AAAA: ")
        hourprog = input("- Hora de inicio: ")
        while True:
            if hourprog.isdigit() and 0 < int(hourprog) < 25:
                hourprog = hourprog.rjust(2)
                break
            else:
                hourprog = input("Escriba la hora de inicio en numeros entre el 1 y 24: ")
        minprog = input("- minutos de inicio: ")
        while True:
            if minprog.isdigit() and 0 <= int(minprog) < 60:
                minprog = minprog.rjust(2)
                break
            else:
                minprog = input("Escriba los minutos de inicio en numeros entre el 0 y 59: ")

        ''' Usando el metodo strftime de la libreria datetime se guardan los valores ingresados por el
            usuario en formato de fecha y hora (DD/MM/AAAA H:M)'''
        fechaprog1 = datetime(int(anoprog), int(mesprog), int(diaprog), int(hourprog), int(minprog)).strftime(
            "%Y/%m/%d %H:%M")
        factual = datetime.now().strftime("%Y/%m/%d %H:%M")

        '''En caso de que no exista una agendacion de citas previa, se ignora la funcion que
            guarda el ultimo registro'''
        if len(ultimoregistro) == 0:
            ultimoreg = factual

        if fechaprog1 >= factual and fechaprog1 >= ultimoreg:
            fechaprog = datetime(int(anoprog), int(mesprog), int(diaprog), int(hourprog), int(minprog)).strftime(
                "%d/%m/%Y %H:%M")
            break
        else:
            print("La fecha de inicio no es valida: ")
    print("Fecha y hora ingresada: " + fechaprog)

    ''' Se extraen los lotes existentes en la base de datos, haciendo uso del objeto cursor y el metodo execute que
        utiliza el SELECT dentro de los parametros'''
    cursorObj.execute('SELECT * FROM LoteVacunas ORDER BY fechavencimiento')
    listado = cursorObj.fetchall()

    ''' Se filtran los lotes de vacunas que se encuentren vigentes a la fecha en la que se iniciara la asignacion
        de citas, asiendo uso de un for para iterar sobre cada lote'''
    lotesvigentes = []
    totalvacunas = 0
    for ids in listado:
        llote = (ids[9]).split("/")
        venlote = datetime(int(llote[2]), int(llote[1]), int(llote[0])).strftime("%Y/%m/%d")
        if venlote > fechaprog1 and ids[3] > ids[4] + ids[11]:
            disponible = ids[3] - ids[4] - ids[11]
            totalvacunas += disponible
            lotesvigentes.append([ids[0], venlote, disponible])
    lotesvigentes.sort(key=lambda x: x[1])

    ''' Se verifica que hayan vacunas disponibles y lotes vigentes, en caso contrario la funcion se
        termina y se notifica al usuario'''
    if len(lotesvigentes) == 0:
        print("No hay lotes vigentes a la fecha")
        return

    elif totalvacunas <= 0:
        print("No hay vacunas a la fecha")
        return

    ''' Se extraen los planes de vacunacion existentes en la base de datos, haciendo uso del objeto cursor
        y el metodo execute que utiliza el SELECT dentro de los parametros'''
    cursorObj.execute('SELECT * FROM PlanVacunacion')
    listado = cursorObj.fetchall()
    planesvigentes = []

    ''' Se filtran los planes de vacunacion que se encuentren vigentes a la fecha en la que se iniciara la asignacion
        de citas, asiendo uso de un for para iterar sobre cada plan de vacunacion'''
    for ids in listado:
        lplan = (ids[4]).split("/")
        venplan = datetime(int(lplan[2]), int(lplan[1]), int(lplan[0])).strftime("%Y/%m/%d")
        iplan = (ids[3]).split("/")
        iniplan = datetime(int(iplan[2]), int(iplan[1]), int(iplan[0])).strftime("%Y/%m/%d")
        if venplan > fechaprog1 > iniplan:
            planesvigentes.append((ids[0], iniplan, venplan))
    planesvigentes.sort(key=lambda x: x[1])

    ''' Se verifica que hayan planes de vacunacion vigentes, en caso contrario la funcion se
        termina y se notifica al usuario'''
    if len(planesvigentes) == 0:
        print("No hay planes de vacunacion vigentes a la fecha")
        return

    ''' Se extraen los pacientes que ya tienen cita asignada, haciendo uso del objeto cursor
        y el metodo execute que utiliza el SELECT dentro de los parametros'''
    cursorObj.execute("SELECT * FROM ProgramacionVacunas")
    inscritos = cursorObj.fetchall()
    agendaExistente = []

    for ins in inscritos:
        agendaExistente.append(ins[0])

    ''' Se filtran por plan de vacunacion los pacientes que cumplen todos los requisitos para poder
        ser vacunados y se almacenan en un contenedor de tipo list '''
    candidatos = []
    candporplan = []
    for rec in planesvigentes:
        if len(candidatos) < totalvacunas:

            ''' Se extrae la edad minima y maxima de cada plan de vacunacion, haciendo uso del objeto cursor
                y el metodo execute que utiliza el SELECT dentro de los parametros'''
            cursorObj.execute('SELECT * FROM PlanVacunacion where idplan= ' + str(rec[0]))
            planselect = cursorObj.fetchall()
            eminplan = int(planselect[0][1])
            emaxplan = int(planselect[0][2])

            ''' Se extraen los pacientes afiliados que aun no estan vacunados, haciendo uso del objeto cursor
                y el metodo execute que utiliza el SELECT dentro de los parametros'''
            cursorObj.execute("SELECT * FROM afiliados where vacunado= 'N' AND desafiliacion = ' '")
            novacunados = cursorObj.fetchall()

            ''' Se filtran los pacientes cuya edad se encuentre dentro del rango del plan de vacunacion
                sobre el que se esta iterando'''
            edadvalida = []
            for edad in novacunados:
                if len(candidatos) < totalvacunas:

                    ''' Funcion para calcular la edad de cada paciente en base a la fecha de nacimiento registrada
                        en la base de datos, usando el metodo now y strftime de la libreria datetime para determinar
                        la edad a la fecha actual'''
                    nacimiento = edad[7].split("/")
                    now = datetime.now()
                    dia = now.strftime("%d")
                    mes = now.strftime("%m")
                    ano = now.strftime("%Y")

                    dano = (int(ano) - int(nacimiento[2])) * 365
                    dmes = (int(mes) - int(nacimiento[1])) * 30
                    ddia = int(dia) - int(nacimiento[0])
                    edadaf = (dano + dmes + ddia) // 365
                    if eminplan <= edadaf <= emaxplan and edad[0] not in candidatos and edad[0] not in agendaExistente:
                        candidatos.append(edad[0])
                        edadvalida.append(edad[0])
                else:
                    break
            candporplan.append(edadvalida)
        else:
            break

    ''' Se verifica que hayan afiliados existentes que cumplan los requisitos para vacunarse, en caso contrario
        la funcion se termina y se notifica al usuario'''
    if not any(candporplan):
        print(
            "No hay afiliados que cumplan los requisitos dentro de los planes vigentes y que se encuentren sin cita de vacunacion a la fecha")
        return

    ''' Se establece la variable con la primera fecha que se asignara y que ira cambiando con cada
        paciente agendado'''
    if fechaprog1 < planesvigentes[0][1]:
        ultimafecha = planesvigentes[0][1]
    else:
        ultimafecha = fechaprog1

    ''' En base a la informacion guardada en contenedores sobre los lotes, planes de vacunacion y afiliados,
        se empiezan a asignar las citas, mientras sigan habiendo vacunas y cupos en los planes de vacunacion'''
    for asignar in range(0, len(planesvigentes)):
        if totalvacunas > 0:
            if ultimafecha < planesvigentes[asignar][1]:
                ultimafecha = planesvigentes[asignar][1]
            for cita in candporplan[asignar]:

                if ultimafecha <= planesvigentes[asignar][2] and totalvacunas > 0:

                    ''' Se extrae la informacion de contacto del paciente a vacunar, haciendo uso del objeto cursor
                        y el metodo execute que utiliza el SELECT dentro de los parametros'''
                    cursorObj.execute("SELECT * FROM afiliados where id= " + str(cita))
                    af = cursorObj.fetchall()[0]

                    noid = af[0]
                    nombre = af[1]
                    apellido = af[2]
                    ciudad = af[6]
                    direccion = af[3]
                    telefono = af[4]
                    email = af[5]

                    ''' Se asigna la fecha y hora de la cita y se suma una hora para la siguiente, con el metodo timedelta
                        de la libreria datetime, guardandola en formato de fecha con el metodo strptime y strftime'''
                    fechaprogramada = ultimafecha[8:10] + ultimafecha[4:8] + ultimafecha[:4]
                    fechaorden = ultimafecha
                    horaprogramada = ultimafecha[11:]
                    ultimafecha = (datetime.strptime(ultimafecha, '%Y/%m/%d %H:%M') + timedelta(hours=1)).strftime(
                        '%Y/%m/%d %H:%M')

                    ''' Se trae la informacion del lote vigente del cual se extraera la vacuna, haciendo uso del objeto cursor
                        y el metodo execute que utiliza el SELECT dentro de los parametros'''
                    while True:
                        if ultimafecha < lotesvigentes[0][1] and lotesvigentes[0][2] > 0:
                            cursorObj.execute("SELECT * FROM LoteVacunas where nolote= " + str(lotesvigentes[0][0]))
                            lot = cursorObj.fetchall()[0]
                            nolote = lotesvigentes[0][0]
                            fabricante = lot[1]
                            lotesvigentes[0][2] -= 1
                            totalvacunas -= 1
                            resv = str(lot[11] + 1)

                            ''' Se reserva la vacuna extraida actualizando el valor de las reservas en la base de datos de los lotes,
                                haciendo uso del objeto cursor y el metodo execute que utiliza el UPDATE dentro de los parametros'''
                            cursorObj.execute('update LoteVacunas SET reserva = ' + resv + ' where nolote = ' + str(
                                lotesvigentes[0][0]))
                            break
                        else:
                            lotesvigentes.pop(0)
                        if len(lotesvigentes) == 0 or totalvacunas == 0:
                            break

                    ''' Se guardan los datos del paciente y la cita a agendar en un contenedor de tipo tupla para su posterior uso'''
                    infcita = (
                        noid, nombre, apellido, ciudad, direccion, telefono, email, nolote, fabricante, fechaprogramada,
                        horaprogramada, fechaorden)

                    ''' Con el llamado a la funcion asignarvacuna se agenda la cita del paciente sobre el cual se esta iterando'''
                    asignarvacuna(con, infcita)

                    ''' Funcion para enviar un correo electronico al paciente, notificandolo sobre la fecha y hora de
                        su cita para vacunarse, haciendo uso de la libreria smtplib'''
                    emailfrom = 'sisgenvac@gmail.com'
                    to = email
                    asunto = 'Cita para vacunacion'
                    texto = 'Cordial saludo ' + nombre.strip() + ' ' + apellido.strip() + ' , se le informa que su cita para vacunarse ha sido asignada para el ' + fechaprogramada + ' a las ' + horaprogramada + ' . Se recomienda ser puntual.'

                    mensaje = """
                    From: %s
                    To: %s
                    Subject: %s

                    %s
                    """ % (emailfrom, to, asunto, texto)

                    username = 'sisgenvac@gmail.com'
                    password = 'POO123456'

                    ''' con el metodo SMTP se crea una conexion segura al servidor de gmail y se inicia con starttls, luego se loguea
                        con el metodo login, se envia el correo con sendmail y finalmente se cierra la conexion con quit'''
                    server = smtplib.SMTP('smtp.gmail.com:587')
                    server.starttls()
                    server.login(username, password)
                    server.sendmail(emailfrom, to, mensaje)

                    server.quit()

                else:
                    # Se sigue con los afiliados del siguiente plan
                    break
        else:
            break
    print("\nLa agendacion se citas se genero con exito!!\n")
    con.commit()


''' Funcion para consultar la cita de un paciente en especifico, que toma como
    parametro la conexion con la base de datos del programa'''


def consulta_individual(con):
    """ Se verifica que existan usuarios con cita agendada, en caso contrario se
        termina la funcion y se notifica al usuario"""
    cursorObj = con.cursor()

    try:
        cursorobj.execute('SELECT * FROM ProgramacionVacunas')
        cursorobj.fetchall()[0]
    except IndexError:
        print("\nNo hay usuarios con citas asignadas en este momento.")
        return

    ''' Se solicita la identificacion del afiliado a consultar por medio de un bucle que se rompe cuando las condiciones son
        validas, verificando que el valor ingresado sea numerico y se encuentre dentro de la base de datos'''
    conafi = input("\nNumero de identificacion del afiliado: ")

    while True:
        if conafi.isdigit():

            ''' Se extrae la informacion de la cita del paciente, haciendo uso del objeto cursor
                y el metodo execute que utiliza el SELECT dentro de los parametros'''
            buscar = 'SELECT * FROM ProgramacionVacunas where noid= ' + conafi
            cursorObj.execute(buscar)
            afil_b = cursorObj.fetchall()
            if len(afil_b) != 0:
                afil_b = afil_b[0]
                break
            else:
                print("El id " + str(conafi) + " no se encuentra en la base de datos")
        conafi = input("Ingrese un id valido: ")

    ''' Se muestra en pantalla la informacion extraida, en un formato de lista a partir de
        varios print que concatenan los datos'''
    print("\n                    PROGRAMACION DE VACUNA")
    print("\n➸ Identificacion:", afil_b[0])
    print("➸ Nombre:", afil_b[1])
    print("➸ Apellido:", afil_b[2])
    print("➸ Direccion:", afil_b[4])
    print("➸ Telefono:", afil_b[5])
    print("➸ Correo:", afil_b[6])
    print("➸ Ciudad de vacunacion:", afil_b[3])
    print("➸ Vacuna:", afil_b[8])
    print("➸ Fecha y hora programada:", afil_b[9], "a las", afil_b[10])

    con.commit()


''' Funcion para consultar la agenda de citas ordenada por algun campo a eleccion, que toma como
    parametro la conexion con la base de datos del programa'''


def agenda(con):
    """ Se verifica que existan usuarios con cita agendada, en caso contrario se
        termina la funcion y se notifica al usuario"""
    cursorObj = con.cursor()

    try:
        cursorobj.execute('SELECT * FROM ProgramacionVacunas')
        cursorobj.fetchall()[0]
    except IndexError:
        print("\nAGENDACION DE CITAS\n\nNo hay usuarios con citas asignadas en este momento.")
        return

    ''' Se muestran en pantalla las opciones de los campos para generar un orden y se solicita al usuario
        que ingrese una opcion identificada por el numero que la precede'''
    print("Seleccione el campo por el que desea organizar la agenda:\n ")
    print("1  - Identificacion")
    print("2  - Nombre")
    print("3  - Apellido")
    print("4  - Direccion")
    print("5  - Telefono")
    print("6  - Correo")
    print("7  - Ciudad de vacunacion")
    print("8  - Vacuna")
    print("9  - Fecha de programacion y hora programada\n")
    campo = input("Ingrese una opcion: ")

    ''' A partir de un bucle que se rompe cuando la informacion es valida, se verifica que el valor ingresado
        sea numerico y este entre las opciones dadas que son los numeros del 1 al 9'''
    while True:
        if campo.isdigit() and 0 < int(campo) < 10:
            break
        else:
            campo = input("Seleccione una opcion valida: ")

    ''' Con los condicionales if y elif, segun la opcion ingresada se guarda el campo por el que se ordenaran
        las citas agendadas en la variable order'''
    if campo == "1":
        order = "noid"
        guia = "IDENTIFICACION"
    elif campo == "2":
        order = "nombre"
        guia = "NOMBRE"
    elif campo == "3":
        order = "apellido"
        guia = "APELLIDO"
    elif campo == "4":
        order = "direccion"
        guia = "DIRECCION"
    elif campo == "5":
        order = "telefono"
        guia = "TELEFONO"
    elif campo == "6":
        order = "email"
        guia = "CORREO"
    elif campo == "7":
        order = "ciudadvacunacion"
        guia = "CIUDAD DE VACUNACION"
    elif campo == "8":
        order = "fabricante"
        guia = "VACUNA"
    elif campo == "9":
        order = "fechaorden"
        guia = "FECHA PROGRAMADA"

    ''' Se reordena la agenda de citas existente en la base de datos, haciendo uso del objeto cursor
        y el metodo execute que utiliza el SELECT y el ORDER BY dentro de los parametros'''
    cursorObj.execute('SELECT * FROM ProgramacionVacunas ORDER BY ' + order + ' ASC')
    mostrar = cursorObj.fetchall()

    ''' Se muestra en pantalla la agenda de citas en un formato de tabla hecho con simbolos a partir del
        metodo format'''
    print("\nAGENDACION DE CITAS POR " + guia + "\n")

    print("+{:-<12}+{:-<20}+{:-<20}+{:-<20}+{:-<20}+{:-<20}+{:-<20}+{:-<10}+{:-<12}+{:-<17}+{:-<10}+".format("",
                                                                                                             "", "",
                                                                                                             "", "",
                                                                                                             "", "",
                                                                                                             "", "",
                                                                                                             "", ""))
    print("|{:^12}|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|{:^10}|{:^12}|{:^17}|{:^10}|".format("Documento",
                                                                                                  "Nombre",
                                                                                                  "Apellido",
                                                                                                  "Ciudad",
                                                                                                  "Direccion",
                                                                                                  "Telefono", "Correo",
                                                                                                  "Lote",
                                                                                                  "Vacuna",
                                                                                                  "Fecha Vacunacion",
                                                                                                  "Hora"))
    print("+{:-<12}+{:-<20}+{:-<20}+{:-<20}+{:-<20}+{:-<20}+{:-<20}+{:-<10}+{:-<12}+{:-<17}+{:-<10}+".format("",
                                                                                                             "", "",
                                                                                                             "", "",
                                                                                                             "", "",
                                                                                                             "", "",
                                                                                                             "", ""))
    for idaf, nombre, apellido, direccion, telefono, email, ciudad, nacimiento, afiliacion, desafiliacion, vacunado, test in mostrar:
        print("|{:^12}|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|{:^10}|{:^12}|{:^17}|{:^10}|".format(idaf, nombre,
                                                                                                      apellido,
                                                                                                      direccion,
                                                                                                      telefono,
                                                                                                      email, ciudad,
                                                                                                      nacimiento,
                                                                                                      afiliacion,
                                                                                                      desafiliacion,
                                                                                                      vacunado))
    print("+{:-<12}+{:-<20}+{:-<20}+{:-<20}+{:-<20}+{:-<20}+{:-<20}+{:-<10}+{:-<12}+{:-<17}+{:-<10}+".format("", "",
                                                                                                             "", "",
                                                                                                             "", "",
                                                                                                             "", "",
                                                                                                             "", "",
                                                                                                             "", ""))

    con.commit()
