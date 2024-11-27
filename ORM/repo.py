import ORM.modelos as modelos
from sqlalchemy.orm import Session 
from sqlalchemy import and_

# Esta funcion es llamada por api.py
# Para atender GET '/usuarios/{id}'
# select * from app.usuarios where id = id_usuario      (id=2)
def usuario_por_id(sesion:Session,id_usuario:int): # sesion de tipo Session de sqlalchemy y el id_usuario de tipo entero
    print("SELECT * from app.usuarios where id= ")
    return sesion.query(modelos.Usuario).filter(modelos.Usuario.id==id_usuario).first() # tabla a consultar PERO de modelos     .filter(modelos.Usuario.id==id_usuario) es como where id=     y el firs es que de el primer elemento para devolver el objeto
    # si se quita el first() devuelve una lista y devuelve todos los usuarios
    # si se pone .all() devuelve todos con ese filtro, es decir todos los que tengan id 2,3 ...
    # devuelve un objeto de tipo usuario y la sesion se destruye automaticamente




def lista_usuarios(sesion:Session): # sesion de tipo Session de sqlalchemy 
    print("SELECT * from app.usuarios")
    return sesion.query(modelos.Usuario).all() # tabla a consultar PERO de modelos  y el .all es para que muestre todos con ese filtro  
    # devuelve un objeto de tipo usuario y la sesion se destruye automaticamente


def lista_fotos(sesion:Session): # sesion de tipo Session de sqlalchemy 
    print("SELECT * from app.fotos")
    return sesion.query(modelos.Foto).all() # tabla a consultar PERO de modelos  y el .all es para que muestre todos con ese filtro  
    # devuelve un objeto de tipo usuario y la sesion se destruye automaticamente


def lista_compras(sesion:Session): # sesion de tipo Session de sqlalchemy 
    print("SELECT * from app.compras")
    return sesion.query(modelos.Compra).all() # tabla a consultar PERO de modelos  y el .all es para que muestre todos con ese filtro  
    # devuelve un objeto de tipo usuario y la sesion se destruye automaticamente



# GET '/compras?id_usuario={id_usuar}&precio={prec}'
# SELECT *FROM app.compras where id_usuario=id_usuar AND precio>=prec
def devuelve_compras_por_usuario_precio(sesion:Session,id_usuar:int,prec:float):
    print("SELECT *FROM app.compras where id_usuario=id_usuar AND precio>=prec")
    return sesion.query(modelos.Compra).filter(and_(modelos.Compra.id_usuario==id_usuar,modelos.Compra.precio>=prec)).all()






def devuelve_usuarios_por_edad(sesion:Session,edad_minima:int, edad_maxima:int):
    print("SELECT *FROM app.usuarios where edad>=edad_minima AND edad_maxima<=eda")
    return sesion.query(modelos.Usuario).filter(and_(modelos.Usuario.edad>=edad_minima, modelos.Usuario.edad<=edad_maxima)).all()




# Ejercicio GET para la tabla de fotos y compras

def foto_por_id(sesion:Session,id_foto:int): # sesion de tipo Session de sqlalchemy y el id_foto de tipo entero
    print("SELECT * from app.fotos where id= ")
    return sesion.query(modelos.Foto).filter(modelos.Foto.id==id_foto).first() # tabla a consultar PERO de modelos.py para tabla Foto
    # devuelve un objeto de tipo foto y la sesion se destruye automaticamente


def compra_por_id(sesion:Session,id_compra:int): # sesion de tipo Session de sqlalchemy y el id_compra de tipo entero
    print("SELECT * from app.compras where id= ")
    return sesion.query(modelos.Compra).filter(modelos.Compra.id==id_compra).first() # tabla a consultar PERO de modelos.py para tabla Compra  
    # devuelve un objeto de tipo compra y la sesion se destruye automaticamente
