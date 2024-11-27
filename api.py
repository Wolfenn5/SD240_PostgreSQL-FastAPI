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

# conda activate ejerciciopostgres
# python -m uvicorn api:app --reload
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

@app.get("/usuarios/{id}")
def usuario_por_id(id: int, sesion:Session=Depends(generador_sesion)):
    print ("Api consultando usuario por id")
    return repo.usuario_por_id(sesion, id) # Sin importar lo que devuelva la funcion (en este caso un objeto de tipo usuario), fastapi lo convierte a JSON

# # simulamos consulta a la base:
# def usuario_por_id(id: int):
#     print("buscando usuario por id:", id)
#     return usuarios[id]

@app.get("/usuarios")
def lista_usuarios(sesion:Session=Depends(generador_sesion)): 
    print ("Api consultando todos los usuarios")
    return repo.lista_usuarios(sesion)


# # Simulamos consulta a la base
# def lista_usuarios(*,lote:int=10,pag:int,orden:Optional[str]=None): #parametros de consulta ?lote=10&pag=1
#     print("lote:",lote, " pag:", pag, " orden:", orden)
#     return usuarios

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

@app.put("/usuario/{id}")
def actualizar_usuario(id:int, usuario:UsuarioBase):
    #simulamos consulta
    usr_act = usuarios[id]
    #simulamos la actualización
    usr_act["nombre"] = usuario.nombre
    usr_act["edad"] = usuario.edad
    usr_act["domicilio"] = usuario.domicilio    

    return usr_act
    
@app.delete("/usuario/{id}")
def borrar_usuario(id:int):
    #simulamos una consulta
    if id>=0 and id< len(usuarios):
        usuario = usuarios[id]
    else:
        usuario = None
    
    if usuario is not None:
        usuarios.remove(usuario)
    
    return {"status_borrado", "ok"}



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



@app.get("/fotos")
def lista_fotos(sesion:Session=Depends(generador_sesion)): 
    print ("Api consultando todas las fotos")
    return repo.lista_fotos(sesion)



# "/compras?id_usuario={id_usuar}&precio={prec}"
# http://127.0.0.1:8000/compras?id_usuario=2&precio=500
# SELECT *FROM app.compras where id_usuario=2 AND precio>=500
@app.get("/compras")
def lista_compras(id_usuario:int,precio:float,sesion:Session=Depends(generador_sesion)): # primero van los parametros obligatorios y luego los opcionales, en este caso el id usuario y precio son obligatorios
    # si se quiere que los valores sean por default habria que cambiar id_usuario:int,precio:float
    print ("/compras?id_usuario={id_usuar}&precio={prec}")
    return repo.lista_compras(sesion)





# "/usuarios?edad={edad1}&edad={edad2}"
# http://127.0.0.1:8000/usuarios?edad_minima=2&edad_maxima=10
# SELECT *FROM app.usuarios where edad>=2 AND edad<=10
@app.get("/usuarios")
def lista_usuarios(edad_minima:int, edad_maxima:int, sesion:Session=Depends(generador_sesion)): 
    print ("SELECT *FROM app.usuarios where edad>=2 AND edad<=10")
    return repo.devuelve_usuarios_por_edad(sesion)




# Ejercicio GET pero mapeando las tablas desde modelos.py

@app.get("/fotos/{id}") # se coloca -->    /fotos/1   /fotos/2 ...
def foto_por_id(id: int, sesion:Session=Depends(generador_sesion)): # Se obtiene el id de la foto a consultar y aparte una sesion por default si es que no se genera
    print ("Api consultando fotos por id")
    return repo.foto_por_id(sesion, id) # Sin importar lo que devuelva la funcion (en este caso un objeto de tipo foto), fastapi lo convierte a JSON


@app.get("/compras/{id}") # se coloca -->   /compras/1   /compras/2 ....
def compra_por_id(id: int, sesion:Session=Depends(generador_sesion)): # Se obtiene el id de la compra a consultar
    print ("Api consultando compras por id")
    return repo.compra_por_id(sesion, id) # Sin importar lo que devuelva la funcion (en este caso un objeto de tipo compra), fastapi lo convierte a JSON

