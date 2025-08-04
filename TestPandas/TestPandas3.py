# Conexión a la base de datos con mysql y consulta de datos
import pymysql

miConection = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    db='inventario',)
cur = miConection.cursor()
cur.execute("SELECT documento, nombre  from usuario")
for documento, nombre in cur.fetchall():
    print(f"Documento: {documento}, Nombre: {nombre}")

miConection.close()