import sqlite3
from sqlite3 import Error
import pandas as pd

def connectDB():
    conn = None
    try:
        conn = sqlite3.connect('C:/Users/Marc F/PycharmProjects/flaskWS/BaseDatos/academiaBD')
    except Error as e:
        print(e)

    return conn

def closeBD(conn):
    if conn:
        conn.close()

def seleccionarmensajes(conn, profesor):
    query = "SELECT mensaje FROM mensajes m WHERE profesor = ?"
    c = conn.cursor()
    tofilter = []
    tofilter.append(profesor)
    result = c.execute(query, tofilter).fetchall()
    return result

