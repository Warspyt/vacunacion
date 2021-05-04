import sqlite3
from sqlite3 import Error
from datetime import datetime
from datetime import date
import lote_vacunas

def sql_vac():
    # funcion que crea la base de datos
    try:
        con = sqlite3.connect('sisgenvac.db')
        # print("Conexion realizada: DB creada")
        return con
    except Error:
        print('Se ha producido un error al crear la conexion', Error)
    
    
    
def lote_v (con):
    cursorObj = con.cursor()
    
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
        # Se guardan los datos de la fecha en formato (DD/MM/AAAA)
        fechaprog1 = datetime(int(anoprog), int(mesprog), int(diaprog)).strftime("%Y/%m/%d")
        factual = datetime.now().strftime("%Y/%m/%d")
        #fechavencimiento = diaven+"/"+mesven+"/"+anoven
        if fechaprog1 >= factual:
            fechaprog = datetime(int(anoprog), int(mesprog), int(diaprog)).strftime("%d/%m/%Y")
            break
        else:
            print("La fecha de inicio no es valida: ")
    print("Fecha ingresada: " + fechaprog)

    
    # Se extraen los Planes vigentes en la base de datos
    cursorObj.execute('SELECT * FROM PlanVacunacion')
    listado = cursorObj.fetchall()
    planesvigentes = []

    # Verificar la fecha para mostrar los planes vigentes a la fecha programada

    for ids in listado:
        lplan = (ids[4]).split("/")
        venplan = datetime(int(lplan[2]), int(lplan[1]), int(lplan[0])).strftime("%Y/%m/%d")
        if venplan > fechaprog1:
            #print("•", ids[0],"para afiliados entre ",ids[1] ," y ", ids[2], "años")
            iplan = (ids[3]).split("/")
            iniplan = datetime(int(iplan[2]), int(iplan[1]), int(iplan[0])).strftime("%Y/%m/%d")
            planesvigentes.append((ids[0], iniplan))
    planesvigentes.sort(key = lambda x : x[1])
    #print(planesvigentes)

    candidatos = []
    for rec in planesvigentes:

        cursorObj.execute('SELECT * FROM PlanVacunacion where idplan= ' + str(rec[0]))
        planselect = cursorObj.fetchall()
        eminplan = int(planselect[0][1])
        emaxplan = int(planselect[0][2])

        # Se busca el plan en la base de datos y se extrae la informacion
        cursorObj.execute("SELECT * FROM afiliados where vacunado= 'N'")
        novacunados = cursorObj.fetchall()
        
        for edad in novacunados:
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
            if eminplan <= edadaf <= emaxplan and edad[0] not in candidatos:
                candidatos.append(edad[0])
    print(candidatos)   
con = sql_vac()
lote_v(con)


