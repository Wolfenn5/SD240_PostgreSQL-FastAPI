from sqlalchemy import create_engine # permite configurar la xconexion a la BD
from sqlalchemy.orm import sessionmaker # permite crear sesiones para hacer consultas
# por cada consulta, se abre y se cierra la sesion
from sqlalchemy.ext.declarative import declarative_base # definir la clase base para mapear las tablas de la BD

# 1.- Configurar la conexion BD
# Crear la URL de la BD --> nombre_servidor://usuario:password@URL_SERVIDOR:puerto/nombreBD
# el 5432 es el puerto que trae postgres por defecto
URL_BASE_DATOS = "postgresql://usuario_ejemplo:12345@localhost:5432/base_ejemplo"

# conectarse mediante el esquema app
engine= create_engine(URL_BASE_DATOS,
                      connect_args={
                          "options":"-csearch_path=app"
                      })


# 2.- Obtener clase que permite crear objetos tipo session
SessionClass = sessionmaker(engine)
# Crear funcionpara obtener objetos de la clase tipo SessionClass
def generador_sesion():
    sesion = SessionClass()
    try:
        yield sesion # es como un return sesion pero de manera segura
    finally:
        sesion.close()


# 3.- Obtener clase base para mapear tablas
BaseClass = declarative_base()