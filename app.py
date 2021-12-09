import sqlite3
import pandas as pd
from flask import Flask, request, jsonify

from BaseDatos import consultasBD

app = Flask(__name__)

@app.route('/', methods=['GET'])
def menu_inicial():  # put application's code here
    return '''<h1>Bienvenido a la academia</h1>'''


@app.route('/login', methods=['GET'])
def login():  # put application's code here
    return '''<h1>Bienvenido al login</h1>'''


@app.route('/alumnos', methods=['GET'])
def listar_alumnos():  # put application's code here
    return '''<h1>Bienvenido a listar alumnos</h1>'''


@app.route('/mensajes', methods=['GET'])
def mensajeria():  # put application's code here
    query_parameters = request.args
    profe = query_parameters.get('profesor')
    conn = consultasBD.connectDB()
    result = consultasBD.seleccionarmensajes(conn, profe)
    consultasBD.closeBD(conn)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
