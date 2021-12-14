import os

import self as self
from flask import Flask, request, jsonify, abort, send_from_directory
from werkzeug.utils import secure_filename
from BaseDatos import consultasBD

app = Flask(__name__)
# Carpeta de archivos ingles
app.config['apuntes_ingles'] = 'C:/Users/Marc F/PycharmProjects/flaskWS/files/ingles'
# Carpeta de archivos catalan
app.config['apuntes_catalan'] = 'C:/Users/Marc F/PycharmProjects/flaskWS/files/catalan'
# Carpeta de archivos matematicas
app.config['apuntes_matematicas'] = 'C:/Users/Marc F/PycharmProjects/flaskWS/files/matematicas'
UPLOAD_DIRECTORY_Mates = "C:/Users/Marc F/PycharmProjects/flaskWS/files/matematicas"

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
        if "/" in filename:
            # Return 400 BAD REQUEST
            abort(400, "no subdirectories allowed")
        else:
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
    return "<h1>Ha ocurrido un error...</h1>"

#Marc
@app.route('/profesores/mensajes', methods=['POST'])
def new_mensaje():  # put application's code here
    conn = consultasBD.connectDB()
    #el profesor debe controlarse con el token no con un form
    profe = request.form["profesor"]
    mensaje = request.form["mensaje"]
    try:
        consultasBD.insertar_mensaje(conn, profe, mensaje)
        return '''<h1>Mensaje subido correctamente!</h1>'''
    except:
        return '''<h1>Ha habido algún problema!</h1>'''

#Marc
@app.route('/admin/mensajes', methods=['GET'])
def mensajeria():  # put application's code here
    query_parameters = request.args
    profe = query_parameters.get('profesor')
    conn = consultasBD.connectDB()
    result = consultasBD.consultar_mensajes(conn, profe)
    consultasBD.closeBD(conn)
    return jsonify(result)

#Marc
@app.route('/admin/mensajes/eliminar', methods=['GET'])
def delete_mensajeria():  # put application's code here
    query_parameters = request.args
    profe = query_parameters.get('profesor')
    conn = consultasBD.connectDB()
    result = consultasBD.consultar_mensajes(conn, profe)
    consultasBD.closeBD(conn)
    return jsonify(result)

#Gus
@app.route('/admin/info_alumnos', methods=['GET'])
def get_info_alumnos():  # put application's code here
    return

#Marc
@app.route('/admin/puntuacion_profes', methods=['GET'])
def get_puntuacion_profes():  # put application's code here
    conn = consultasBD.connectDB()
    result = consultasBD.consultar_puntuaciones(conn)
    consultasBD.closeBD(conn)
    return jsonify(result)

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
        consultasBD.insertar_alumno(conn, nombre, edad, pago_hecho, tutor_legal, id_grupo)
        return '''<h1>Success!</h1>'''
    except:
        return '''<h1>Fail!</h1>'''

#Gus
@app.route('/admin/new_profesor', methods=['POST'])
def new_profesor():  # put application's code here
    conn = consultasBD.connectDB()
    try:
        #consultasBD.insertar_alumno(conn, nombre, edad, pago_hecho, tutor_legal, id_grupo)
        return '''<h1>Success!</h1>'''
    except:
        return '''<h1>Fail!</h1>'''

#Gus
@app.route('/admin/modificar_profesores', methods=['POST'])
def modificar_profesores():  # put application's code here
    return

#Gus
@app.route('/admin/modificar_alumnos', methods=['POST'])
def modificar_alumnos():  # put application's code here
    return

#Marc
@app.route('/alumnos/apuntes/<path>', methods=['GET'])
def get_apuntes(path = None):  # put application's code here
    if path is None:
        self.Error(400)
    try:
        #if path == "matematicas" or path == "catalan" or path == "ingles":
        return send_from_directory(UPLOAD_DIRECTORY_Mates, path, as_attachment=True)
    except Exception as e:
        self.log.exception(e)
        self.Error(400)
    return '''<h1>Fail!</h1>'''

#Marc & Gus
@app.route('/alumnos/puntuar_profesor', methods=['GET'])
def puntuar_profesor():  # put application's code here
    query_parameters = request.args
    profe = query_parameters.get('profesor')
    nota = query_parameters.get('nota')
    conn = consultasBD.connectDB()
    try:
        consultasBD.insertar_puntuacion(conn, profe, nota)
        return '''<h1>Success!</h1>'''
    except:
        return '''<h1>Fail!</h1>'''

if __name__ == '__main__':
    app.run(debug=True)
