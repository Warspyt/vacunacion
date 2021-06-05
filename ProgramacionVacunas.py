import sqlite3
from sqlite3 import Error
from datetime import datetime
from datetime import date
from datetime import timedelta
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
                      apellido text, ciudadvacunacion text,direccion text, telefono integer, email text,
                      nolote integer, fabricante text, fechaprogramada text, horaprogramada text, fechaorden text)""")
    con.commit()

def asignarVacuna(con, info):
    # Se asigna la cita para la vacuna con la informacion del usuario y la vacuna
    cursorObj = con.cursor()
    cursorObj.execute("""INSERT INTO ProgramacionVacunas(noid, nombre, apellido,
                      ciudadvacunacion, direccion, telefono, email, nolote, fabricante,
                      fechaprogramada, horaprogramada, fechaorden)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", info)
    con.commit()

def infoCita(con):
    
    cursorObj = con.cursor()

    cursorObj.execute('SELECT * FROM ProgramacionVacunas')
    ultimoregistro = cursorObj.fetchall()[-1]
    ultfechares = ultimoregistro[9]
    ulthorares = ultimoregistro[10]
    ultimoreg = datetime(int(ultfechares[6:10]), int(ultfechares[3:5]), int(ultfechares[:2]), int(ulthorares[:2]), int(ulthorares[3:5])).strftime("%Y/%m/%d %H:%M")
    
    while True:

        diaprog = input("Fecha de inicio del agendamiento de citas:\n\n- Dia de inicio: ")
        # Se verifica que el dato ingresado sea un dia existente dentro del calendario
        while True:
            if diaprog.isdigit() and 0<int(diaprog)<32:
                diaprog = diaprog.rjust(2,"0")
                break
            else:
                diaprog = input("Escriba el dia de inicio en dos digitos: ")
        mesprog = input("- Mes de inicio: ")
        # Se verifica que el dato ingresado sea un mes existente dentro del calendario
        while True:
            if mesprog.isdigit() and 0<int(mesprog)<13:
                mesprog = mesprog.rjust(2,"0")
                break
            else:
                mesprog = input("Escriba el mes de inicio en numeros entre el 1 y 12: ")
        anoprog = input("- año de inicio: ")
        # Se verifica que el dato ingresado sea un año coherente para el vencimiento
        while True:
            if anoprog.isdigit() and len(anoprog) == 4 and int(anoprog)>2020:
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
        # Se guardan los datos de la fecha en formato (DD/MM/AAAA)
        fechaprog1 = datetime(int(anoprog), int(mesprog), int(diaprog), int(hourprog), int(minprog)).strftime("%Y/%m/%d %H:%M")
        factual = datetime.now().strftime("%Y/%m/%d %H:%M")
        #fechavencimiento = diaven+"/"+mesven+"/"+anoven
        if fechaprog1 >= factual and fechaprog1 >= ultimoreg:
            fechaprog = datetime(int(anoprog), int(mesprog), int(diaprog), int(hourprog), int(minprog)).strftime("%d/%m/%Y %H:%M")
            break
        else:
            print("La fecha de inicio no es valida: ")
    print("Fecha y hora ingresada: " + fechaprog)
    
    # Se muestran los lotes existentes en la base de datos
    cursorObj.execute('SELECT * FROM LoteVacunas ORDER BY fechavencimiento')
    listado = cursorObj.fetchall()
    # Verificar la fecha para mostrar los lotes vigentes
    lotesvigentes = []
    totalvacunas = 0
    for ids in listado:
        llote = (ids[9]).split("/")
        venlote = datetime(int(llote[2]), int(llote[1]), int(llote[0])).strftime("%Y/%m/%d")
        if venlote > fechaprog1 and ids[3] > ids[4] + ids[11]:
            disponible = ids[3]- ids[4] - ids[11] 
            totalvacunas += disponible
            lotesvigentes.append([ids[0], venlote, disponible])
    lotesvigentes.sort(key=lambda x: x[1])

    print("lotes vigentes")
    print(lotesvigentes)
    print("total vacunas")
    print(totalvacunas)

    # Si no hay lotes vigentes o no hay vacunas no se continua

    if len(lotesvigentes) == 0:
        print("No hay lotes vigentes a la fecha")
        return

    elif totalvacunas <= 0:
        print("No hay vacunas a la fecha")
        return
    
    # totalvacunas = totalvacunas 
    # ordenlotes = lotesvigentes
    
    # Se extraen los Planes vigentes en la base de datos
    cursorObj.execute('SELECT * FROM PlanVacunacion')
    listado = cursorObj.fetchall()
    planesvigentes = []

    # Verificar la fecha para mostrar los planes vigentes a la fecha programada

    for ids in listado:
        lplan = (ids[4]).split("/")
        venplan = datetime(int(lplan[2]), int(lplan[1]), int(lplan[0])).strftime("%Y/%m/%d")
        iplan = (ids[3]).split("/")
        iniplan = datetime(int(iplan[2]), int(iplan[1]), int(iplan[0])).strftime("%Y/%m/%d")
        if venplan > fechaprog1 > iniplan:
            planesvigentes.append((ids[0], iniplan, venplan))
    planesvigentes.sort(key = lambda x : x[1])

    print("planes vigentes")
    print(planesvigentes)
    if len(planesvigentes) == 0:
        print("No hay planes de vacunacion vigentes a la fecha")
        return


    # Verificacion en la agenda existente

    cursorObj.execute("SELECT * FROM ProgramacionVacunas")
    inscritos = cursorObj.fetchall()
    agendaExistente = []
    
    for ins in inscritos:
        agendaExistente.append(ins[0])
    
    candidatos = []
    candporplan = []
    for rec in planesvigentes:
        if len(candidatos) < totalvacunas:

            cursorObj.execute('SELECT * FROM PlanVacunacion where idplan= ' + str(rec[0]))
            planselect = cursorObj.fetchall()
            eminplan = int(planselect[0][1])
            emaxplan = int(planselect[0][2])

            # Se busca el plan en la base de datos y se extrae la informacion
            cursorObj.execute("SELECT * FROM afiliados where vacunado= 'N'")
            novacunados = cursorObj.fetchall()
        
            edadvalida = []
            for edad in novacunados:
                if len(candidatos) < totalvacunas:
                    # Calcular edad
                    nacimiento = edad[7].split("/")
                    now= datetime.now()
                    dia = now.strftime("%d")
                    mes = now.strftime("%m")
                    ano = now.strftime("%Y")

                    dano = (int(ano) - int(nacimiento[2]))*365
                    dmes = (int(mes) - int(nacimiento[1]))*30
                    ddia = int(dia) - int(nacimiento[0])
                    edadaf = (dano + dmes + ddia)//365
                    if eminplan <= edadaf <= emaxplan and edad[0] not in candidatos and edad[0] not in agendaExistente:
                        candidatos.append(edad[0])
                        edadvalida.append(edad[0])
                else:
                    break
            candporplan.append(edadvalida)
        else:
            break

    print("candidatos por plan")
    print(candporplan)
    if len(candporplan) == 0:
        print("No hay afiliados dentro de los planes vigentes sin cita de vacunacion a la fecha")
        return
    

    # Establecer primera fecha
    if fechaprog1 < planesvigentes[0][1]:
        ultimafecha = planesvigentes[0][1]
    else:
        ultimafecha = fechaprog1
    
    for asignar in range(0, len(planesvigentes)):
        if totalvacunas > 0:
            if ultimafecha < planesvigentes[asignar][1]:
                 ultimafecha = planesvigentes[asignar][1]
            for cita in candporplan[asignar]:
                #print(cita)
                #print(planesvigentes[asignar])
                
                if ultimafecha <= planesvigentes[asignar][2] and totalvacunas > 0:
                    cursorObj.execute("SELECT * FROM afiliados where id= " + str(cita))
                    af = cursorObj.fetchall()[0]
                    # Asignar cita
                    noid = af[0]
                    nombre = af[1]
                    apellido = af[2]
                    ciudad = af[6]
                    direccion = af[3]
                    telefono = af[4]
                    email = af[5]
                    # agregar una hora luego de la hora y fecha asignada
                    fechaprogramada = ultimafecha[8:10] + ultimafecha[4:8] + ultimafecha[:4]
                    fechaorden = ultimafecha
                    horaprogramada = ultimafecha[11:]
                    ultimafecha = (datetime.strptime(ultimafecha, '%Y/%m/%d %H:%M') + timedelta(hours = 1)).strftime('%Y/%m/%d %H:%M')

                    # print(lotesvigentes)
                    while True:
                        if ultimafecha < lotesvigentes[0][1] and lotesvigentes[0][2] > 0:
                            cursorObj.execute("SELECT * FROM LoteVacunas where nolote= " + str(lotesvigentes[0][0]))
                            lot = cursorObj.fetchall()[0]
                            nolote = lotesvigentes[0][0]
                            fabricante = lot[1]
                            lotesvigentes[0][2] -= 1
                            totalvacunas -= 1
                            resv = str(lot[11] + 1)
                            cursorObj.execute('update LoteVacunas SET reserva = ' + resv + ' where nolote = ' + str(lotesvigentes[0][0]))
                            break
                        else:
                            lotesvigentes.pop(0)
                        if len(lotesvigentes) == 0 or totalvacunas == 0:
                            break
                    infcita = (noid, nombre, apellido, ciudad, direccion, telefono, email, nolote, fabricante, fechaprogramada, horaprogramada, fechaorden)
                    asignarVacuna(con, infcita)

                else:
                    # Se sigue con los afiliados del siguiente plan
                    break
        else:
            break

def consulta_individual(con):
    cursorObj = con.cursor()
    conafi = input("\nNumero de identificacion del afiliado: ")
    # Verifiar que la identificacion ingresada se encuentre en la base de datos
    while True:
        if conafi.isdigit():
            buscar = 'SELECT * FROM ProgramacionVacunas where noid= ' + conafi
            cursorObj.execute(buscar)
            afil_b = cursorObj.fetchall()
            if len(afil_b) != 0:
                afil_b = afil_b[0]
                break
            else:
                print("El id " + str(conafi) + " no se encuentra en la base de datos")
        conafi = input("Ingrese un id valido: ")
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

def agenda(con):
    cursorObj = con.cursor()
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
    while True:
        if campo.isdigit() and 0 < int(campo) < 10:
            break
        else:
            campo = input("Seleccione una opcion valida: ")
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
        
    # Organizar la agenda
    cursorObj.execute('SELECT * FROM ProgramacionVacunas ORDER BY ' + order + ' ASC')
    mostrar = cursorObj.fetchall()
    print("\AGENDACION DE CITAS POR " +  guia + "\n")
    '''counter = 1
    for item in mostrar:
        print("\n                    PACIENTE " + str(counter))
        print("\n➸ Identificacion:", item[0])
        print("➸ Nombre:", item[1])
        print("➸ Apellido:", item[2])
        print("➸ Direccion:", item[4])
        print("➸ Telefono:", item[5])
        print("➸ Correo:", item[6])
        print("➸ Ciudad de vacunacion:", item[3])
        print("➸ Vacuna:", item[8])
        print("➸ Fecha y hora programada:", item[9], "a las", item[10])
        counter += 1'''

    # Con tabla
    print("+{:-<12}+{:-<20}+{:-<20}+{:-<20}+{:-<20}+{:-<20}+{:-<20}+{:-<10}+{:-<12}+{:-<17}+{:-<10}+".format("",
                                                                                                                "", "",
                                                                                                                "", "",
                                                                                                                "", "",
                                                                                                                "", "",
                                                                                                                "",""))
    print("|{:^12}|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|{:^10}|{:^12}|{:^17}|{:^10}|".format("Documento",
                                                                                                      "Nombre",
                                                                                                      "Apellido",
                                                                                                      "Ciudad",
                                                                                                      "Direccion",
                                                                                                      "Telefono", "Correo",
                                                                                                      "Lote",
                                                                                                      "Vacuna",
                                                                                                      "Fecha Vacunacion", "Hora"))
    print("+{:-<12}+{:-<20}+{:-<20}+{:-<20}+{:-<20}+{:-<20}+{:-<20}+{:-<10}+{:-<12}+{:-<17}+{:-<10}+".format("",
                                                                                                                "", "",
                                                                                                                "", "",
                                                                                                                "", "",
                                                                                                                "", "",
                                                                                                                "",""))
    for idaf, nombre, apellido, direccion, telefono, email, ciudad, nacimiento, afiliacion, desafiliacion, vacunado,test in mostrar:
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
                                                                                                                 "",""))

    con.commit()
     
    

def main():
    prog = sql_prog()
    tabla_prog(prog)
    infoCita(prog)
    #agenda(prog)
    
main()
    
