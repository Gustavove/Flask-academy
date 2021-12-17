import os

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

    if(len(result)== 0):
        return 'Error'
    else:
        result = result[0][0]
        return result

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
            return "Success!"
    return "Error"

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
         result.append({"Nombre": i[0], "Age": i[1], "Pago hecho": i[2], "Tutor_legal": i[3], "Id_grupo": i[4]})

     return jsonify(result)

#Marc
@app.route('/admin/puntuacion_profes', methods=['GET'])
def get_puntuacion_profes():  # put application's code here
    conn = consultasBD.connectDB()
    bd_result = consultasBD.consultar_puntuaciones(conn)
    consultasBD.closeBD(conn)

    result = []
    for i in bd_result:
        result.append({"Profesor": i[0], "Puntuacion": i[1]})

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
        consultasBD.closeBD(conn)
        return "Success!"
    except:
        return "Error"

#Gus
@app.route('/admin/new_profesor', methods=['POST'])
def new_profesor():  # put application's code here
    conn = consultasBD.connectDB()
    nombre = request.form["nombre"]
    puntuacion = request.form["puntuacion"]

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
@app.route('/alumnos/apuntes/<path>', methods=['GET'])
def get_apuntes(path = None):  # put application's code here
    if path is None:
        return "Error"
    try:
        #if path == "matematicas" or path == "catalan" or path == "ingles":
        return send_from_directory(UPLOAD_DIRECTORY_Mates, path, as_attachment=True)
    except Exception as e:
        return "Error"

#Marc & Gus
@app.route('/alumnos/puntuar_profesor', methods=['GET'])
def puntuar_profesor():  # put application's code here
    query_parameters = request.args
    profe = query_parameters.get('profesor')
    nota = query_parameters.get('nota')
    conn = consultasBD.connectDB()
    try:
        consultasBD.insertar_puntuacion(conn, profe, nota)
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


if __name__ == '__main__':
    app.run(debug=True)
