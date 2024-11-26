# Sirve para mapear clases
# La clase BaseClass mapea a las tablas
# Los modelos o clases modelo son las clases que mapean a las tablas
from ORM.config import BaseClass
# Importar de SQLAlchemy los tipos de datos que usan las tablas
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float # tipos de datos que usa sqlalchemy
import datetime # para calcular la hora actual



# Por convencion, el nombre de las clases se ponen en singular aunque en la BD esten en plural y empiecen con mayuscula
class Usuario(BaseClass): 
    __tablename__="usuarios" # nombre de la tabla en la BD
    id= Column(Integer, primary_key=True) # Define que es una columna, es de tipo entero y es una llave primaria
    nombre= Column(String(100)) # de 100 caracteres
    edad= Column(Integer)
    domicilio= Column(String(150))
    email= Column("email",String(100)) # representa que es un email, si no esta en el formato lo devuelve por ejemplo que le falte un @
    password= Column(String(40))
    fecha_registro=Column(DateTime(timezone=True), default=datetime.datetime.now) # cuando se inserte la fecha, se hara con la zona horaria, default para que sea con la hora del dispositivo


class Compra(BaseClass):
    __tablename__="compras"
    id= Column(Integer, primary_key=True)
    id_usuario= Column(Integer, ForeignKey(Usuario.id)) # Llave Foranea de la tabla usuario y es el id
    producto= Column(String(100))
    precio= Column(Float)


class Foto(BaseClass):
    __tablename__="fotos"
    id= Column(Integer, primary_key=True)
    id_usuario= Column(Integer, ForeignKey(Usuario.id)) 
    titulo= Column(String(100))
    descripcion= Column(String(100))
    ruta= Column(String(150))


