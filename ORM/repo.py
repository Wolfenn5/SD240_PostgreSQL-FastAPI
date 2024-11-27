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



# Funcion para obtener la lista de todos los usuarios
def lista_usuarios(sesion:Session): # sesion de tipo Session de sqlalchemy 
    print("SELECT * from app.usuarios")
    return sesion.query(modelos.Usuario).all() # tabla a consultar PERO de modelos  y el .all es para que muestre todos con ese filtro  
    # devuelve un objeto de tipo usuario y la sesion se destruye automaticamente


# Funcion para obtener la lista de todas las fotos
def lista_fotos(sesion:Session): # sesion de tipo Session de sqlalchemy 
    print("SELECT * from app.fotos")
    return sesion.query(modelos.Foto).all() # tabla a consultar PERO de modelos  y el .all es para que muestre todos con ese filtro  
    # devuelve un objeto de tipo usuario y la sesion se destruye automaticamente


# Funcion para obtener la lista de todas las compras
def lista_compras(sesion:Session): # sesion de tipo Session de sqlalchemy 
    print("SELECT * from app.compras")
    return sesion.query(modelos.Compra).all() # tabla a consultar PERO de modelos  y el .all es para que muestre todos con ese filtro  
    # devuelve un objeto de tipo usuario y la sesion se destruye automaticamente




# Funcion para devolver las compras de un usuario
# SELECT * from app.compras where id_usuario=2 AND precio>=500

# "/compras?id_usuario={id_usuar}&precio={prec}"
def devuelve_compras_por_usuario_precio(sesion:Session,id_usuar:int,prec:float):
    print("SELECT * from app.compras where id_usuario=id_usuar AND precio>=prec")
    return sesion.query(modelos.Compra).filter(and_(modelos.Compra.id_usuario==id_usuar,modelos.Compra.precio>=prec)).all()





# Funcion para devolver una lista de usuarios de un rango de edad
# SELECT * from app.usuarios where edad>=2 AND edad<=10

# "/usuarios?edad={edad1}&edad={edad2}"
def devuelve_usuarios_por_edad(sesion:Session,edad_minima:int, edad_maxima:int):
    print("SELECT * from app.usuarios where edad>=edad_minima AND edad<=edad_maxima")
    return sesion.query(modelos.Usuario).filter(and_(modelos.Usuario.edad>=edad_minima, modelos.Usuario.edad<=edad_maxima)).all()




# Ejercicios GET para la tabla de fotos y compras

# Funcion para devolver una foto dado un id
# SELECT * from app.fotos where id= 1 

# "/fotos/{id}"
def foto_por_id(sesion:Session,id_foto:int): # sesion de tipo Session de sqlalchemy y el id_foto de tipo entero
    print("SELECT * from app.fotos where id= ")
    return sesion.query(modelos.Foto).filter(modelos.Foto.id==id_foto).first() # tabla a consultar PERO de modelos.py para tabla Foto
    # devuelve un objeto de tipo foto y la sesion se destruye automaticamente




# Funcion para deolver una compra dado un id
# SELECT * from app.compras where id=3

# "/compras/{id}"
def compra_por_id(sesion:Session,id_compra:int): # sesion de tipo Session de sqlalchemy y el id_compra de tipo entero
    print("SELECT * from app.compras where id= ")
    return sesion.query(modelos.Compra).filter(modelos.Compra.id==id_compra).first() # tabla a consultar PERO de modelos.py para tabla Compra  
    # devuelve un objeto de tipo compra y la sesion se destruye automaticamente
