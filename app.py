import os

from flask import Flask, request, jsonify, abort, send_from_directory
from werkzeug.utils import secure_filename
from BaseDatos import consultasBD
import base64


app = Flask(__name__)
# Carpeta de archivos ingles
app.config['apuntes_ingles'] = 'C:/Users/Marc F/PycharmProjects/flaskWS/files/ingles'
# Carpeta de archivos catalan
app.config['apuntes_catalan'] = 'C:/Users/Marc F/PycharmProjects/flaskWS/files/catalan'
# Carpeta de archivos matematicas
app.config['apuntes_matematicas'] = 'C:/Users/Marc F/PycharmProjects/flaskWS/files/matematicas'
FILES_DIRECTORY = "/home/alumne/PycharmProjects/flaskWB/files"


@app.route('/', methods=['GET'])
def menu_inicial():
    return '''<h1>¡Bienvenido a la academia de Gustavo y Marc!</h1>'''


@app.route('/login', methods=['GET'])
def login():
    query_parameters = request.args
    username = query_parameters.get('username')
    password = query_parameters.get('password')
    conn = consultasBD.connectDB()
    result = consultasBD.login(conn, username, password)
    consultasBD.closeBD(conn)

    if (len(result)== 0):
        return 'Error'
    else:
        result = result[0][0]
        return result


#Marc
@app.route('/profesores/mensajes', methods=['POST'])
def new_mensaje():  # put application's code here
    conn = consultasBD.connectDB()
    #el profesor debe controlarse con el token no con un form
    profe = request.form["profesor"]
    mensaje = request.form["mensaje"]
    try:
        consultasBD.insertar_mensaje(conn, profe, mensaje)
        return "Success!"
    except:
        return "Error"


#Gustavo
@app.route('/profesores/mis_alumnos', methods=['GET'])
def nmis_alumnos():
    nombre = request.args.get("nombre")

    conn = consultasBD.connectDB()
    bd_result = consultasBD.comsulta_alumnos_profe(conn, nombre)
    consultasBD.closeBD(conn)

    result = []
    for i in bd_result:
        result.append({"Nombre":i[0], "Age":i[1], "Tutor_legal":i[2]})

    return jsonify(result)


#Marc
@app.route('/admin/mensajes', methods=['GET'])
def mensajeria():  # put application's code here
    query_parameters = request.args
    profe = query_parameters.get('profesor')
    conn = consultasBD.connectDB()
    bd_result= consultasBD.consultar_mensajes(conn, profe)
    consultasBD.closeBD(conn)

    result = []
    for i in bd_result:
        result.append({"Mensaje":i[0]})

    return jsonify(result)


#Gus
@app.route('/admin/info_alumno', methods=['GET'])
def get_info_alumno():  # put application's code here
    nombre = request.args.get("nombre")

    conn = consultasBD.connectDB()
    bd_result = consultasBD.consultar_alumno(conn, nombre)
    consultasBD.closeBD(conn)

    result = []
    for i in bd_result:
        result.append({"Nombre": i[0], "Age": i[1], "Pago_hecho": i[2], "Tutor_legal": i[3], "Id_grupo": i[4]})

    return jsonify(result)


#Gus
@app.route('/admin/lista_alumnos', methods=['GET'])
def get_lista_alumnos():
    conn = consultasBD.connectDB()
    bd_result = consultasBD.consultar_alumnos(conn)
    consultasBD.closeBD(conn)

    result = []
    for i in bd_result:
        result.append({"Nombre": i[0], "Age": i[1], "Pago_hecho": i[2], "Tutor_legal": i[3], "Id_grupo": i[4]})

    return jsonify(result)


#Marc
@app.route('/admin/lista_profes', methods=['GET'])
def get_lista_profes():
    conn = consultasBD.connectDB()
    bd_result = consultasBD.consultar_profesores(conn)
    consultasBD.closeBD(conn)

    result = []
    for i in bd_result:
        result.append({"Profesor": i[0], "Puntuacion": i[1]})

    return jsonify(result)



#Marc
@app.route('/admin/puntuacion_profes', methods=['GET'])
def get_puntuacion_profes():
    conn = consultasBD.connectDB()
    bd_result = consultasBD.consultar_profesores(conn)
    consultasBD.closeBD(conn)

    result = []
    for i in bd_result:
        result.append({"Profesor": i[0], "Puntuacion": i[1]})

    return jsonify(result)


@app.route('/admin/new_alumno', methods=['POST'])
def new_alumno():
    conn = consultasBD.connectDB()
    nombre = request.form["nombre"]
    edad = str(request.form["edad"])
    pago_hecho = request.form["pago_hecho"]
    tutor_legal = request.form["tutor_legal"]
    id_grupo = request.form["id_grupo"]

    foto = request.form["foto"]

    try:
        #Guardamos la imagen del tutor_legal
        foto = foto.encode('utf-8')
        image_64_encode = base64.decodebytes(foto)
        image_result = open('./fotos_tutores/'+ tutor_legal + '.jpg', 'wb')
        image_result.write(image_64_encode)

        consultasBD.insertar_alumno(conn, nombre, edad, pago_hecho, tutor_legal, id_grupo)
        consultasBD.closeBD(conn)
        return "Success!"
    except:
        return "Error"


#Gus
@app.route('/admin/new_profesor', methods=['POST'])
def new_profesor():
    conn = consultasBD.connectDB()
    nombre = request.form["nombre"]
    puntuacion = request.form["puntuacion"]

    print(nombre)
    print(puntuacion)
    try:
        consultasBD.insertar_profesor(conn, nombre, puntuacion)
        consultasBD.closeBD(conn)
        return "Success!"

    except:
        return "Error"


#Gus
@app.route('/admin/modificar_alumno', methods=['POST'])
def modificar_alumno():
    conn = consultasBD.connectDB()
    nombre = request.form["nombre"]
    edad = str(request.form["edad"])
    pago_hecho = str(request.form["pago_hecho"])
    tutor_legal = request.form["tutor_legal"]
    id_grupo = str(request.form["id_grupo"])

    try:
        consultasBD.modificar_alumno(conn, nombre, edad, pago_hecho, tutor_legal, id_grupo)
        consultasBD.closeBD(conn)
        return "Success!"
    except:
        return "Error"


#Marc
@app.route('/alumnos/apuntes/<path>/<file>', methods=['GET'])
def get_apuntes(path = None, file = None):  # put application's code here
    if path is None or file is None:
        return "Error"
    try:
        #if path == "matematicas" or path == "catalan" or path == "ingles":
        return send_from_directory(FILES_DIRECTORY, path + '/' + file, as_attachment=True)
    except Exception as e:
        return "Error"


#Marc & Gus
@app.route('/alumnos/puntuar_profesor', methods=['GET'])
def puntuar_profesor():  # put application's code here
    query_parameters = request.args
    profe = query_parameters.get('profesor')
    nota = float(query_parameters.get('puntuacion'))
    conn = consultasBD.connectDB()
    try:
        notamitja = consultasBD.consultar_puntuacion(conn, profe)
        notamitja = (notamitja + nota)/2
        consultasBD.insertar_puntuacion(conn, profe, notamitja)
        return "Success!"
    except:
        return "Error"


#Gus
@app.route('/alumnos/ficheros_de_asignatura', methods=['GET'])
def ficheros_de_asignatura():
    asignatura = request.args.get("asignatura")

    conn = consultasBD.connectDB()
    bd_result = consultasBD.consulta_ficheros(conn, asignatura)
    consultasBD.closeBD(conn)

    result = []
    for i in bd_result:
        result.append({"Nombre_fichero": i[0], "Path": i[1]})

    return jsonify(result)


#Gus
@app.route('/alumnos/mis_asignaturas', methods=['GET'])
def mis_asignaturas():
    nombre_alumno = request.args.get("nombre_alumno")

    conn = consultasBD.connectDB()
    bd_result = consultasBD.consulta_mis_asignaturas(conn, nombre_alumno)
    consultasBD.closeBD(conn)

    result = []
    for i in bd_result:
        result.append({"Asignatura": i[0]})

    return jsonify(result)


#Gus
@app.route('/alumnos/mis_profes', methods=['GET'])
def mis_profes():
    nombre_alumno = request.args.get("nombre_alumno")

    conn = consultasBD.connectDB()
    bd_result = consultasBD.consulta_mis_profes(conn, nombre_alumno)
    consultasBD.closeBD(conn)

    result = []
    for i in bd_result:
        result.append({"Profesor": i[0]})

    return jsonify(result)


@app.route('/admin/descargar_imagen_tutor', methods=['GET'])
def imagen_tutor():
    nombre_alumno = request.args.get("nombre")

    conn = consultasBD.connectDB()
    bd_result = consultasBD.consultar_tutor(conn, nombre_alumno)

    image = open('./fotos_tutores/' + bd_result[0][0] + '.jpg', 'rb')
    image_read = image.read()
    image_64_encode = base64.b64encode(image_read)

    return image_64_encode.decode('utf-8')

@app.route('/profesores/subir_archivo', methods=['POST'])
def subir_apuntes():
    conn = consultasBD.connectDB()
    asignatura = request.form["asignatura"]
    nombre = request.form["nombre"]
    filename = request.form["filename"]
    fichero = request.form["fichero"]

    try:
        #Guardamos la imagen del tutor_legal
        fichero = fichero.encode('utf-8')
        image_64_encode = base64.decodebytes(fichero)
        image_result = open('./files/' + asignatura + '/' + filename, 'wb')
        image_result.write(image_64_encode)

        consultasBD.insertar_fichero(conn, asignatura, nombre, filename)
        consultasBD.closeBD(conn)
        return "Success!"
    except:
        return "Error"
if __name__ == '__main__':
    app.run(debug=True)
