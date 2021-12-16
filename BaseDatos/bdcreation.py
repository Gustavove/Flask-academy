import sqlite3

conn = sqlite3.connect('academiaBD')
c = conn.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS alumnos
          ([nombre] TEXT PRIMARY KEY, [edad] INTEGER, [pago_hecho] INTEGER, [tutor_legal] TEXT, [id_grupo] INTEGER REFERENCES grupos(id))
          ''')


c.execute('''
          CREATE TABLE IF NOT EXISTS aulas
          ([num] INTEGER)
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS asignaturas
          ([nombre] TEXT PRIMARY KEY)
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS matricula
          ([nombre_alumno] TEXT, [nombre_asignatura] TEXT, PRIMARY KEY(nombre_alumno, nombre_asignatura))
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS profesores
          ([nombre_profesor] TEXT PRIMARY KEY, [puntuacion] REAL)
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS grupos
          ([id] INTEGER , [asignatura] TEXT, [profesor] TEXT, [hora] TEXT, [ref_libro] INTEGER, [num_aula] INTEGER REFERENCES aulas(num), PRIMARY KEY(id, asignatura, profesor) )
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS login
          ([username] TEXT PRIMARY KEY, [password] TEXT, [tipo_usuario] TEXT)
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS mensajes
          ([profesor] TEXT, [mensaje] TEXT)
          ''')


conn.commit()