import sqlite3

conn = sqlite3.connect('academiaBD')
c = conn.cursor()

c.execute('''
          INSERT INTO alumnos (nombre, edad, pago_hecho, tutor_legal, id_grupo)

                VALUES
                ('Mike', 12, 0, 'Mike John', 2),
                ('Paula', 16, 0, 'Mike John', 3),
                ('Marc', 11, 0, 'Marc Fer', 1),
                ('Pedro', 12, 1, 'Gustavo Vergara', 2)
          ''')

c.execute('''
          INSERT INTO aulas (num)

                VALUES
                (1),
                (2),
                (3),
                (4),
                (5)
          ''')

c.execute('''
          INSERT INTO asignaturas (nombre)

                VALUES
                ('matematicas'),
                ('catalan'),
                ('ingles')
          ''')

c.execute('''
          INSERT INTO matricula (nombre_alumno, nombre_asignatura)

                VALUES
                ('Mike', 'ingles'),
                ('Paula', 'matematicas'),
                ('Marc', 'catalan'),
                ('Pedro', 'ingles')
          ''')

c.execute('''
          INSERT INTO profesores (nombre_profesor, puntuacion)

                VALUES
                ('Silvia', 8.2),
                ('Pepito', 9.1)
          ''')

c.execute('''
          INSERT INTO grupos (id, asignatura, profesor, hora, ref_libro, num_aula)

                VALUES
                (1, 'ingles', 'Silvia', '12:00', 0001, 01),
                (2, 'matematicas', 'Pepito', '11:00', 0003, 02),
                (3, 'ingles', 'Silvia', '18:00', 0001, 01),
                (4, 'catalan', 'Pepito', '12:00', 0002, 04)
          ''')

c.execute('''
          INSERT INTO login (username, password, tipo_usuario)

                VALUES
                ('Mike', '12345', 'Alumno'),
                ('Paula', 'paula123', 'Alumno'),
                ('Silvia', '12345','Profesor'),
                ('admin', 'admin', 'Admin')
          ''')

c.execute('''
          INSERT INTO mensajes (profesor, mensaje)

                VALUES
                ('Silvia', 'Buenas, esto es una prueba'),
                ('Pepito', 'Buenas esto es una segunta prueba'),
                ('Silvia', 'Buenas, Juan se esta portando muy mal')
          ''')

c.execute('''
          INSERT INTO ficheros (asignatura, nombre_fichero, path)

                VALUES
                ('matematicas', 'derivadas', 'derivadas.txt'),
                ('catalan', 'pronomsfebles', 'pronomsfebles.txt'),
                ('ingles', 'exercices', 'exercices.txt')
          ''')


conn.commit()