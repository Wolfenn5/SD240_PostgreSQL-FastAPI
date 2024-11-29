from fastapi import FastAPI, UploadFile, File, Form, Depends
from typing import Optional
from pydantic import BaseModel
import shutil
import os
import uuid

import ORM.repo as repo # funciones para hacer consultas a la BD
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ORM.config import generador_sesion # generador de sesiones 

# conda create --name ejerciciopostgres   --> Para crear ambiente
# conda activate ejerciciopostgres        --> Para activar ambiente
# python -m uvicorn api:app --reload      --> Para levantar el servidor

# El cliente (navegadores) leen JSON
# Python lee diccionarios



# El ORM es el puente entre la base de datos y el codigo python
# El modelo va a tener todo menos el id
# Los schemas es para llevar cosas a la BD, no necesita conectarse a la BD
# El archivo de config se configura el engine (conexion a BD), class session (crear sesion), class base (hereda tablas)

# creación del servidor
app = FastAPI()

#definición de la base del usuario
class UsuarioBase(BaseModel):
    nombre:Optional[str]=None
    edad:int
    domicilio:str    
    
usuarios = [{
    "id": 0,
    "nombre": "Homero Simpson",
    "edad": 40,
    "domicilio": "Av. Simpre Viva"
}, {
    "id": 1,
    "nombre": "Marge Simpson",
    "edad": 38,
    "domicilio": "Av. Simpre Viva"
}, {
    "id": 2,
    "nombre": "Lisa Simpson",
    "edad": 8,
    "domicilio": "Av. Simpre Viva"
}, {
    "id": 3,
    "nombre": "Bart Simpson",
    "edad": 10,
    "domicilio": "Av. Simpre Viva"
}]


# decorator
@app.get("/")
def hola_mundo():
    print("invocando a ruta /")
    respuesta = {
        "mensaje": "hola mundo!"
    }

    return respuesta


#########################

# Usuarios

#########################

@app.get("/usuarios/{id}/compras/{id_compra}")
def compras_usuario_por_id(id: int, id_compra: int):
    print("buscando compra con id:", id_compra, " del usuario con id:", id)
    # simulamos la consulta
    compra = {
        "id_compra": 787,
        "producto": "TV",
        "precio": 14000
    }

    return compra


# # Funcion para todos los usuarios (simple)
# @app.get("/usuarios")
# def lista_usuarios(sesion:Session=Depends(generador_sesion)): 
#     print ("Api consultando todos los usuarios")
#     return repo.lista_usuarios(sesion)

# # simulando consulta a una BD:
# def usuario_por_id(id: int):
#     print("buscando usuario por id:", id)
#     return usuarios[id]



# # Simulando consulta a una BD pero con parametros de consulta
# @app.get("/usuarios")
# def lista_usuarios(*,lote:int=10,pag:int,orden:Optional[str]=None): #parametros de consulta ?lote=10&pag=1
#     print("lote:",lote, " pag:", pag, " orden:", orden)
#     return usuarios



# Funcion para consultar usuarios por id con BD
# --> /usuarios/1
@app.get("/usuarios/{id}")
def usuario_por_id(id: int, sesion:Session=Depends(generador_sesion)):
    print ("Api consultando usuario por id")
    return repo.usuario_por_id(sesion, id) # Sin importar lo que devuelva la funcion (en este caso un objeto de tipo usuario), fastapi lo convierte a JSON



# Funcion para consultar las fotos de un usuario con BD
# --> /usuarios/2/fotos
@app.get("/usuarios/{id}/fotos")
def fotos_por_id_usr(id:int, sesion:Session=Depends(generador_sesion)):
    print("API consultando fotos del usuario", id)
    return repo.fotos_por_id_usuario(sesion,id)




# Funcion para consultar las compras de un usuario con BD
# --> /usuarios/2/compras
@app.get("/usuarios/{id}/compras")
def compras_por_id_usr(id:int, sesion:Session=Depends(generador_sesion)):
    print("API consultando compras del usuario", id)
    return repo.compras_por_id_usuario(sesion,id)



# Funcion para consultar usuarios por edad y ademas todos los usuarios con BD
# SELECT *FROM app.usuarios where edad>=2 AND edad<=10

# "/usuarios?edad={edad1}&edad={edad2}"
# --> /usuarios?edad_minima=2&edad_maxima=10         para consultar por edad
# --> /usuarios                                      para consultar todos
@app.get("/usuarios")
def lista_usuarios(edad_minima:int, edad_maxima:int, sesion:Session=Depends(generador_sesion)): 
    print ("SELECT * from app.usuarios where edad>=2 AND edad<=10")
    return repo.devuelve_usuarios_por_edad(sesion, edad_minima, edad_maxima)





# Funcion para insertar un nuevo usuario
@app.post("/usuarios")
def guardar_usuario(usuario:UsuarioBase, parametro1:str):
    print("usuario a guardar:", usuario, ", parametro1:", parametro1)
    #simulamos guardado en la base.
    
    usr_nuevo = {}
    usr_nuevo["id"] = len(usuarios)
    usr_nuevo["nombre"] = usuario.nombre
    usr_nuevo["edad"] = usuario.edad
    usr_nuevo["domicilio"] = usuario.domicilio

    usuarios.append(usuario)

    return usr_nuevo



# Funcion para actualizar datos de un usuario
@app.put("/usuario/{id}")
def actualizar_usuario(id:int, usuario:UsuarioBase):
    #simulamos consulta
    usr_act = usuarios[id]
    #simulamos la actualización
    usr_act["nombre"] = usuario.nombre
    usr_act["edad"] = usuario.edad
    usr_act["domicilio"] = usuario.domicilio    

    return usr_act
    




# Funcion para borrar un usuario
# DELETE from app.usuarios where id= {id_usuario}    
@app.delete("/usuario/{id}")
def borrar_usuario(id:int, sesion:Session=Depends(generador_sesion)):
    # Antes de borrar el usuario hay que llamar a borrar fotos por id usuario y borrar compras por id usuario
    repo.borrar_compras_por_id_usuario(sesion,id)
    repo.borrar_fotos_por_id_usuario(sesion,id)
    # Y ahora si se puede borrar el usuario
    repo.borrar_usuario_por_id(sesion,id)
    return {"usuario_borrado", "ok"}


# #simulando consulta a BD
# def borrar_usuario(id:int):
#     if id>=0 and id< len(usuarios):
#         usuario = usuarios[id]
#     else:
#         usuario = None
    
#     if usuario is not None:
#         usuarios.remove(usuario)
    
#     return {"status_borrado", "ok"}







#########################

# Fotos

#########################

# Funcion para introducir fotos
@app.post("/fotos")
async def guardar_foto(titulo:str=Form(None), descripcion:str=Form(...), foto:UploadFile=File(...)):
    print("titulo:", titulo)
    print("descripcion:", descripcion)

    home_usuario=os.path.expanduser("~")
    nombre_archivo=uuid.uuid4().hex  #generamos nombre único en formato hexadecimal
    extension = os.path.splitext(foto.filename)[1]
    ruta_imagen=f'{home_usuario}/fotos-ejemplo/{nombre_archivo}{extension}'
    print("guardando imagen en ruta:", ruta_imagen)

    with open(ruta_imagen,"wb") as imagen:
        contenido = await foto.read() #read funciona de manera asyncrona
        imagen.write(contenido)

    return {"titulo":titulo, "descripcion":descripcion, "foto":foto.filename}



# Funcion para consultar todas las fotos con BD
@app.get("/fotos")
def lista_fotos(sesion:Session=Depends(generador_sesion)): 
    print ("Api consultando todas las fotos")
    return repo.lista_fotos(sesion)



# Ejercicio GET pero mapeando las tablas desde modelos.py con BD
@app.get("/fotos/{id}") # se coloca -->    /fotos/1   /fotos/2 ...
def foto_por_id(id: int, sesion:Session=Depends(generador_sesion)): # Se obtiene el id de la foto a consultar y aparte una sesion por default si es que no se genera
    print ("Api consultando fotos por id")
    return repo.foto_por_id(sesion, id) # Sin importar lo que devuelva la funcion (en este caso un objeto de tipo foto), fastapi lo convierte a JSON






#########################

# Compras

#########################




# Funcion para consultar las compras de un usuario 
# SELECT *FROM app.compras where id_usuario=2 AND precio>=500

# "/compras?id_usuario={id_usuar}&precio={prec}"
# -->  compras?id_usuario=2&precio=500         para consultar las compras del usuario 2 y precio>=500
@app.get("/compras")
def lista_compras(id_usuario:int,precio:float,sesion:Session=Depends(generador_sesion)): # primero van los parametros obligatorios y luego los opcionales, en este caso el id usuario y precio son obligatorios
    # si se quiere que los valores sean por default habria que cambiar id_usuario:int,precio:float
    print ("/compras?id_usuario={id_usuar}&precio={prec}")
    return repo.devuelve_compras_por_usuario_precio(sesion, id_usuario, precio)




# Ejercicio GET pero mapeando las tablas desde modelos.py
# Funcion para consultar compras por id
# SELECT * from app.compras where id=1

# "/compras/{id}"
# -->   /compras/1
@app.get("/compras/{id}") 
def compra_por_id(id: int, sesion:Session=Depends(generador_sesion)): # Se obtiene el id de la compra a consultar
    print ("Api consultando compras por id")
    return repo.compra_por_id(sesion, id) # Sin importar lo que devuelva la funcion (en este caso un objeto de tipo compra), fastapi lo convierte a JSON

