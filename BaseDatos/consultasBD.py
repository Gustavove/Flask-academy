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

def login(conn, username, password):
    query = "SELECT tipo_usuario FROM login l WHERE username = ? AND password = ?"
    c = conn.cursor()
    tofilter = []
    tofilter.append(username)
    tofilter.append(password)
    result = c.execute(query, tofilter).fetchall()
    return result

def inserta_alumno(conn, nombre, edad, pago_hecho, tutor_legal, id_grupo):
    c = conn.cursor()
    try:
        nou_alumne = (nombre, edad, pago_hecho, tutor_legal, id_grupo)
        query = '''INSERT INTO alumnos (nombre, edad, pago_hecho, tutor_legal, id_grupo) 
        VALUES (?,?,?,?,?)'''
        c.execute(query, nou_alumne)
        conn.commit()
    except Error as e:
        print(e)

    return

def seleccionarmensajes(conn, profesor):
    query = "SELECT mensaje FROM mensajes m WHERE profesor = ?"
    c = conn.cursor()
    tofilter = []
    tofilter.append(profesor)
    result = c.execute(query, tofilter).fetchall()
    return result

