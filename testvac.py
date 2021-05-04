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

    for ids in listado:
        llote = (ids[9]).split("/")
        venlote = datetime(int(llote[2]), int(llote[1]), int(llote[0])).strftime("%Y/%m/%d")
        if venlote > factual and ids[3] > ids[4]:
            disponible= ids[3]- ids[4]
            print("Lote: ",ids[0] ,"recibidas: ", ids[3],"usadas: ", ids[4],"disponibles" ,disponible)

  #   SELECT * FROM( SELECT * FROM  db ORDER BY  sale_date  DESC  )   WHERE   rownum <= 10





convacunas = sql_lotevacunas()
avencer(convacunas)