import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from BaseDatos import consultasBD

app = Flask(__name__)
# Carpeta de archivos ingles
app.config['apuntes_ingles'] = 'C:/Users/Marc F/PycharmProjects/flaskWS/files/ingles'
# Carpeta de archivos catalan
app.config['apuntes_catalan'] = 'C:/Users/Marc F/PycharmProjects/flaskWS/files/catalan'
# Carpeta de archivos matematicas
app.config['apuntes_matematicas'] = 'C:/Users/Marc F/PycharmProjects/flaskWS/files/matematicas'

@app.route('/', methods=['GET'])
def menu_inicial():  # put application's code here
    return '''<h1>¡Bienvenido a la academia de Gustavo y Marc!</h1>'''


@app.route('/login', methods=['GET'])
def login():  # put application's code here
    query_parameters = request.args
    username = query_parameters.get('username')
    password = query_parameters.get('password')
    conn = consultasBD.connectDB()
    result = consultasBD.login(conn, username, password)
    consultasBD.closeBD(conn)
    return jsonify(result)

@app.route('/alumnos', methods=['GET'])
def menu_alumnos():
    return

@app.route('/profesores', methods=['GET'])
def menu_profesores():
    return

@app.route('/admin', methods=['GET'])
def menu_administrador():
    return

#Marc
@app.route('/profesores/apuntes', methods=['POST'])
def post_apuntes():  # put application's code here
    if request.method == 'POST':
        query_parameters = request.args
        asig = query_parameters.get('asignatura')
        # obtenemos el archivo del input "archivo"
        f = request.files['archivo']
        filename = secure_filename(f.filename)
        if asig == 'matematicas':
            #Guardamos el archivo en el directorio "Archivos PDF"
            f.save(os.path.join(app.config['apuntes_matematicas'], filename))
        elif asig == 'ingles':
            #Guardamos el archivo en el directorio "Archivos PDF"
            f.save(os.path.join(app.config['apuntes_ingles'], filename))
        elif asig == 'catalan':
            #Guardamos el archivo en el directorio "Archivos PDF"
            f.save(os.path.join(app.config['apuntes_catalan'], filename))
        # Retornamos una respuesta satisfactoria
        return "<h1>Archivo subido exitosamente</h1>"

#Marc
@app.route('/profesores/mensajes', methods=['GET'])
def get_mensajes():  # put application's code here
    return

#Marc
@app.route('/admin/mensajes', methods=['GET'])
def mensajeria():  # put application's code here
    query_parameters = request.args
    profe = query_parameters.get('profesor')
    conn = consultasBD.connectDB()
    result = consultasBD.seleccionarmensajes(conn, profe)
    consultasBD.closeBD(conn)
    return jsonify(result)

#Gus
@app.route('/admin/info_alumnos', methods=['GET'])
def get_info_alumnos():  # put application's code here
    return

#Gus
@app.route('/admin/get_puntuacion_profes', methods=['GET'])
def get_puntuacion_profes():  # put application's code here
    return

#Gus (falta subir imagen papi)
@app.route('/admin/new_alumno', methods=['POST'])
def new_alumno():
    conn = consultasBD.connectDB()
    nombre = request.form["nombre"]
    edad = str(request.form["edad"])
    pago_hecho = str(request.form["pago_hecho"])
    tutor_legal = request.form["tutor_legal"]
    id_grupo = str(request.form["id_grupo"])

    try:
        consultasBD.inserta_alumno(conn, nombre, edad, pago_hecho, tutor_legal, id_grupo)
        return '''<h1>Success!</h1>'''
    except:
        return '''<h1>Fail!</h1>'''

#Gus
@app.route('/admin/new_profesor', methods=['POST'])
def new_profesor():  # put application's code here
    return

#Marc
@app.route('/admin/info_profesores', methods=['GET'])
def get_info_profesores():  # put application's code here
    return

#Gus
@app.route('/admin/modificar_profesores', methods=['POST'])
def modificar_profesores():  # put application's code here
    return

#Gus
@app.route('/admin/modificar_alumnos', methods=['POST'])
def modificar_alumnos():  # put application's code here
    return

#Marc
@app.route('/alumnos/apuntes', methods=['GET'])
def get_apuntes():  # put application's code here
    return

#Marc & Gus
@app.route('/alumnos/puntuar_profesor', methods=['POST'])
def puntuar_profesor():  # put application's code here
    return

if __name__ == '__main__':
    app.run(debug=True)
