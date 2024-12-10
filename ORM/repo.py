import ORM.modelos as modelos
from sqlalchemy.orm import Session 
from sqlalchemy import and_
import ORM.esquemas as esquemas


#########################

# Usuarios

#########################


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



# Funcion para devolver una lista de usuarios de un rango de edad
# SELECT * from app.usuarios where edad>=2 AND edad<=10
# "/usuarios?edad={edad1}&edad={edad2}"
def devuelve_usuarios_por_edad(sesion:Session,edad_minima:int, edad_maxima:int):
    print("SELECT * from app.usuarios where edad>=edad_minima AND edad<=edad_maxima")
    return sesion.query(modelos.Usuario).filter(and_(modelos.Usuario.edad>=edad_minima, modelos.Usuario.edad<=edad_maxima)).all()



# Funcion para borrar usuario con BD
# DELETE from app.usuarios where id= {id_usuario}
# '/usuarios/{id}'
def borrar_usuario_por_id(sesion:Session, id_usuario:int):
    print("DELETE from app.usuarios where id= ", id_usuario)
    # 1.- Antes de borrar primero se va a verificar que existe con un SELECT
    usr= usuario_por_id(sesion,id_usuario) # la sesion se pasa como un argumento y no como sesion:Session, porque se crearia una doble sesion
    # 2.- Se borra
    if usr is not None:
        sesion.delete(usr)
        # 3.- Se confirma que se hizo el cambio, se hace asi para que se hagan todos juntos si es que se borran muchos usarios 
        sesion.commit() # Se hacen todos los cambios de un "jalon"
    respuesta = {
        "mensaje": "usuario eliminado"
    }
    return respuesta




# Funcion para buscar fotos por un id de usuario dado
# GET '/usuarios/{id}/fotos/'
# SELECT * from app.fotos where id_usuario=id
def fotos_por_id_usuario(sesion:Session,id_usr:int):
    print("SELECT * from app.fotos where id_usuario=",id_usr)
    return sesion.query(modelos.Foto).filter(modelos.Foto.id_usuario==id_usr).all() # devuelve una lista de objetos






# Funcion para borrar fotos por un id de usuario dado con BD
# DELETE 'usuarios/{id}/fotos'
# DELETE * from app.fotos where id_usuario=
def borrar_fotos_por_id_usuario(sesion:Session,id_usuario:int):
    print("DELETE * from app.fotos where id_usuario=", id_usuario)
    # 1.- Antes de borrar primero se va a verificar que existe con un SELECT
    fotos_usr = fotos_por_id_usuario(sesion,id_usuario) 
    # 2.- Se borra, pero como hay que hacer un delete por cada foto se usa un iterador
    if fotos_usr is not None: # Si existe, entonces itera
        for foto_usuario in fotos_usr:
            sesion.delete(foto_usuario)
            # 3.- Se confirma que se hizo el cambio, se hace asi para que se hagan todos juntos si es que se borran muchos usarios 
        sesion.commit() # Se hacen todos los cambios de un "jalon"
    respuesta = {
        "mensaje": "fotos del usuario eliminadas"
    }
    return respuesta


# Funcion para buscar compras por un id de usuario dado
# GET '/usuarios/{id}/compras/'
# SELECT * from app.compras where id_usuario=id
def compras_por_id_usuario(sesion:Session,id_usr:int):
    print("SELECT * from app.compras where id_usuario=id")
    return sesion.query(modelos.Compra).filter(modelos.Compra.id_usuario==id_usr).all() # devuelve una lista de objetos



# Funcion para borrar compras por un id de usuario dado
# DELETE 'usuarios/{id}/compras'
# DELETE * from app.compras where id_usuario=
def borrar_compras_por_id_usuario(sesion:Session,id_usuario:int):
    print("DELETE * from app.compras where id_usuario=", id_usuario)
    compras_usr = compras_por_id_usuario(sesion,id_usuario) 
    # Como hay que hacer un delete por cada foto se usa un iterador
    if compras_usr is not None: # Si existe, entonces itera
        for compra_usuario in compras_usr:
            sesion.delete(compra_usuario)
        sesion.commit()
    respuesta = {
        "mensaje": "compras del usuario eliminadas"
    }
    return respuesta




# Funcion para actualizar datos de usuario
# PUT '/usuarios/{id}'
def actualiza_usuario(sesion:Session, id_usuario:int, usr_esquema:esquemas.UsuarioBase):
    # 1.- Primero se verifica que el usuario exista
    usr_bd = usuario_por_id(sesion, id_usuario) # objeto de la clase de la BD
    # 2.- Si existe, entonces se actualizan los datos
    if usr_bd is not None:
        usr_bd.nombre = usr_esquema.nombre
        usr_bd.edad = usr_esquema.edad
        usr_bd.domicilio = usr_esquema.domicilio
        usr_bd.email = usr_esquema.email
        usr_bd.password = usr_esquema.password
    # 3.- Confirmar los cambios
        sesion.commit()
    # 4.- Refrescar/actualizar los cambios
        sesion.refresh(usr_bd)
    # 5.- Imprimir los datos nuevos
        print(usr_esquema)
        return (usr_esquema)
    else:
        respuesta = {"mensaje" : "No existe el usuario"}
        return respuesta



#########################

# Fotos

#########################

# Funcion para obtener la lista de todas las fotos
def lista_fotos(sesion:Session): # sesion de tipo Session de sqlalchemy 
    print("SELECT * from app.fotos")
    return sesion.query(modelos.Foto).all() # tabla a consultar PERO de modelos  y el .all es para que muestre todos con ese filtro  
    # devuelve un objeto de tipo usuario y la sesion se destruye automaticamente


# Funcion para devolver una foto dado un id
# SELECT * from app.fotos where id= 1 
# "/fotos/{id}"
def foto_por_id(sesion:Session,id_foto:int): # sesion de tipo Session de sqlalchemy y el id_foto de tipo entero
    print("SELECT * from app.fotos where id= ")
    return sesion.query(modelos.Foto).filter(modelos.Foto.id==id_foto).first() # tabla a consultar PERO de modelos.py para tabla Foto
    # devuelve un objeto de tipo foto y la sesion se destruye automaticamente





def actualiza_fotos(sesion:Session, id_foto:int, foto_esquema:esquemas.FotoBase):
    # 1.- Primero se verifica que la foto exista
    foto_bd = foto_por_id(sesion, id_foto) # objeto de la clase de la BD
    # 2.- Si existe, entonces se actualizan los datos
    if foto_bd is not None:
        foto_bd.titulo = foto_esquema.titulo
        foto_bd.descripcion = foto_esquema.descripcion
    # 3.- Confirmar los cambios
        sesion.commit()
    # 4.- Refrescar/actualizar los cambios
        sesion.refresh(foto_bd)
    # 5.- Imprimir los datos nuevos
        print(foto_esquema)
        return (foto_esquema)
    else:
        respuesta = {"mensaje" : "No existe la foto"}
        return respuesta


#########################

# Compras

#########################



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



# Funcion para deolver una compra dado un id
# SELECT * from app.compras where id=3
# "/compras/{id}"
def compra_por_id(sesion:Session,id_compra:int): # sesion de tipo Session de sqlalchemy y el id_compra de tipo entero
    print("SELECT * from app.compras where id= ")
    return sesion.query(modelos.Compra).filter(modelos.Compra.id==id_compra).first() # tabla a consultar PERO de modelos.py para tabla Compra  
    # devuelve un objeto de tipo compra y la sesion se destruye automaticamente




def actualiza_compras(sesion:Session, id_compra:int, compra_esquema:esquemas.CompraBase):
    # 1.- Primero se verifica que la compra exista
    compra_bd = compra_por_id(sesion, id_compra) # objeto de la clase de la BD
    # 2.- Si existe, entonces se actualizan los datos
    if compra_bd is not None:
        compra_bd.producto = compra_esquema.producto
        compra_bd.precio = compra_esquema.precio
    # 3.- Confirmar los cambios
        sesion.commit()
    # 4.- Refrescar/actualizar los cambios
        sesion.refresh(compra_bd)
    # 5.- Imprimir los datos nuevos
        print(compra_esquema)
        return (compra_esquema)
    else:
        respuesta = {"mensaje" : "No existe la compra"}
        return respuesta
