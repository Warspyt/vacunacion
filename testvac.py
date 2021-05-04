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


def avencer(con):
    cursorObj = con.cursor()
    # Se muestran los lotes existentes en la base de datos
    cursorObj.execute('SELECT * FROM LoteVacunas ORDER BY fechavencimiento')
    listado = cursorObj.fetchall()
    # Verificar la fecha para mostrar los lotes vigentes
    factual = datetime.now().strftime("%Y/%m/%d")
    lotesvigentes = []
    for ids in listado:
        llote = (ids[9]).split("/")
        venlote = datetime(int(llote[2]), int(llote[1]), int(llote[0])).strftime("%Y/%m/%d")
        if venlote > factual and ids[3] > ids[4]:
            disponible= ids[3]- ids[4]
            ilote = (ids[9]).split("/")
            inilote = datetime(int(ilote[2]), int(ilote[1]), int(ilote[0])).strftime("%Y/%m/%d")
            lotesvigentes.append((ids[0], inilote))
            lotesvigentes.sort(key=lambda x: x[0])
            print(lotesvigentes)





convacunas = sql_lotevacunas()
avencer(convacunas)