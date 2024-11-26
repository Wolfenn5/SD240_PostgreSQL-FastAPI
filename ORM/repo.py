import ORM.modelos as modelos
from sqlalchemy.orm import Session

# Esta funcion es llamada por api.py
# Para atender GET '/usuarios/{id}'
# select * from app.usuarios where id = id_usuario      (id=2)
def usuario_por_id(sesion:Session,id_usuario:int): # sesion de tipo Session de sqlalchemy y el id_usuario de tipo entero
    print("SELECT * from app.usuarios where id= ")
    return sesion.query(modelos.Usuario).filter(modelos.Usuario.id==id_usuario).first() # tabla a consultar PERO de modelos     .filter(modelos.Usuario.id==id_usuario) es como where id=     y el firs es que de el primer elemento
    # devuelve un objeto de tipo usuario y la sesion se destruye automaticamente




# Ejercicio GET para la tabla de fotos y compras

def foto_por_id(sesion:Session,id_foto:int): # sesion de tipo Session de sqlalchemy y el id_foto de tipo entero
    print("SELECT * from app.fotos where id= ")
    return sesion.query(modelos.Foto).filter(modelos.Foto.id==id_foto).first() # tabla a consultar PERO de modelos.py para tabla Foto
    # devuelve un objeto de tipo foto y la sesion se destruye automaticamente


def compra_por_id(sesion:Session,id_compra:int): # sesion de tipo Session de sqlalchemy y el id_compra de tipo entero
    print("SELECT * from app.compras where id= ")
    return sesion.query(modelos.Compra).filter(modelos.Compra.id==id_compra).first() # tabla a consultar PERO de modelos.py para tabla Compra  
    # devuelve un objeto de tipo compra y la sesion se destruye automaticamente
