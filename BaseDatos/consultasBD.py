import sqlite3
from sqlite3 import Error
import pandas as pd

def connectDB():
    conn = None
    try:
        conn = sqlite3.connect('/home/alumne/PycharmProjects/flaskWB/BaseDatos/academiaBD')
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

#Gustavo
def insertar_alumno(conn, nombre, edad, pago_hecho, tutor_legal, id_grupo):
    c = conn.cursor()
    try:
        nou_alumne = (nombre, edad, pago_hecho, tutor_legal, id_grupo)
        query = '''INSERT INTO alumnos (nombre, edad, pago_hecho, tutor_legal, id_grupo) 
        VALUES (?,?,?,?,?)'''
        c.execute(query, nou_alumne)
        conn.commit()
    except Error as e:
        print(e)

#Gustavo
def insertar_profesor(conn, nombre, puntuacion):
    c = conn.cursor()
    try:
        nou_profe = (nombre, puntuacion)
        query = '''INSERT INTO profesores (nombre_profesor, puntuacion) 
        VALUES (?,?)'''
        c.execute(query, nou_profe)
        conn.commit()

    except Error as e:
        print(e)


def insertar_mensaje(conn, profesor, mensaje):
    c = conn.cursor()
    try:
        new_message = (profesor, mensaje)
        query = '''INSERT INTO mensajes (profesor, mensaje) 
        VALUES (?,?)'''
        c.execute(query, new_message)
        conn.commit()
    except Error as e:
        print(e)

    return

def insertar_puntuacion(conn, profesor, puntuacion):
    c = conn.cursor()
    try:
        modificadores = (puntuacion, profesor)
        query = " UPDATE profesores SET puntuacion = ? WHERE nombre_profesor = ?"
        c.execute(query, modificadores)
        conn.commit()
    except Error as e:
        print(e)

    return

def consultar_puntuacion(conn, profesor):
    query = "SELECT puntuacion FROM profesores p WHERE nombre_profesor = ?"
    c = conn.cursor()
    tofilter = []
    tofilter.append(profesor)
    result = c.execute(query, tofilter).fetchone()[0]
    return result

def consultar_mensajes(conn, profesor):
    query = "SELECT mensaje FROM mensajes m WHERE profesor = ?"
    c = conn.cursor()
    tofilter = []
    tofilter.append(profesor)
    result = c.execute(query, tofilter).fetchall()
    return result

def consultar_profesores(conn):
    query = "SELECT * FROM profesores p"
    c = conn.cursor()
    result = c.execute(query).fetchall()
    return result

#Gastavo
def consultar_alumno(conn, nombre):
    query = "SELECT * FROM alumnos a WHERE nombre = ?"
    c = conn.cursor()
    tofilter = []
    tofilter.append(nombre)
    result = c.execute(query, tofilter).fetchall()
    return result


#Gastavo
def consultar_alumnos(conn):
    query = "SELECT * FROM alumnos a"
    c = conn.cursor()
    result = c.execute(query).fetchall()
    return result

#Gustavo
def modificar_alumno(conn, nombre, edad, pago_hecho, tutor_legal, id_grupo):

    modificadores = (edad, pago_hecho, tutor_legal, id_grupo, nombre)

    try:
        query= ''' UPDATE alumnos
                      SET edad = ? ,
                          pago_hecho = ? ,
                          tutor_legal = ?,
                          id_grupo = ?
                      WHERE nombre = ?'''
        c = conn.cursor()
        c.execute(query, modificadores)
        conn.commit()
    except Error as e:
        print(e)

def comsulta_alumnos_profe(conn, nombre_profe):
    #Devuelve los alumnos que tiene el profe en sus grupos

    query = ''' SELECT a.nombre, a.edad, a.tutor_legal FROM alumnos a, grupos g WHERE a.id_grupo = g.id AND g.profesor = ?'''
    c = conn.cursor()
    tofilter = []
    tofilter.append(nombre_profe)
    result = c.execute(query, tofilter).fetchall()
    return result

def consulta_ficheros(conn, asignatura):

    query = ''' SELECT nombre_fichero, path FROM ficheros WHERE asignatura = ?'''
    c = conn.cursor()
    tofilter = []
    tofilter.append(asignatura)
    result = c.execute(query, tofilter).fetchall()
    return result

def consulta_mis_asignaturas(conn, nombre_alumno):

    query = ''' SELECT m.nombre_asignatura FROM alumnos a, matricula m WHERE a.nombre = ? AND m.nombre_alumno=?'''
    c = conn.cursor()
    consultores = (nombre_alumno, nombre_alumno)

    result = c.execute(query, consultores).fetchall()
    return result

def consulta_mis_profes(conn, nombre_alumno):

    query = ''' SELECT g.profesor FROM alumnos a, grupos g WHERE a.nombre = ? AND a.id_grupo = g.id'''
    c = conn.cursor()
    tofilter = []
    tofilter.append(nombre_alumno)

    result = c.execute(query, tofilter).fetchall()
    return result


#Gastavo
def consultar_tutor(conn, nombre):
    query = "SELECT tutor_legal FROM alumnos a WHERE nombre = ?"
    c = conn.cursor()
    tofilter = []
    tofilter.append(nombre)
    result = c.execute(query, tofilter).fetchall()
    return result

def insertar_fichero(conn, asignatura, nombre, path):
    c = conn.cursor()
    try:
        new_puntuacion = (asignatura, nombre, path)
        query = '''INSERT INTO ficheros (asignatura, nombre_fichero, path) 
        VALUES (?,?, ?)'''
        c.execute(query, new_puntuacion)
        conn.commit()
    except Error as e:
        print(e)

    return


