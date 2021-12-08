import sqlite3
from sqlite3 import Error
import pandas as pd

def connectDB(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def selectalumnes(conn):
    c = conn.cursor()
    c.execute('''
          SELECT
          *
          FROM alumnes a
          ''')
    df = pd.DataFrame(c.fetchall(), columns=['nombre','edad', 'pago_hecho', 'tutor_legal', 'id_grupo'])
    return df



#conexion de prueba
#conn = sqlite3.connect('academiaBD')
#c = conn.cursor()
#c.execute('''
#          SELECT
#          *
#          FROM alumnos a
#          ''')
#df = pd.DataFrame(c.fetchall(), columns=['nombre','edad', 'pago_hecho', 'tutor_legal', 'id_grupo'])
#print (df)