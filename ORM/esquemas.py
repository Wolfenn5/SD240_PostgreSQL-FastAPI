from pydantic import BaseModel
# El schema en postgres sirve para asociar la tabla de la BD 
# Tambien para acceder solo a ciertas tablas, controlar el acceso o restringir ciertas tablas a la BD
# Objetos a recibir desde el cliente
# Con esquemas recibimos lo del cliente, a diferencia de modelos que se recibe de la BD




# Definir el esquema usuario
# No se inlcuye el id ni la fecha de registro porque no se quiere que el usuario pueda modificarlos
class UsuarioBase(BaseModel):
    nombre:str
    edad:int
    domicilio:str
    email:str
    password:str


# Definir el esquema foto
class FotoBase(BaseModel):
    titulo:str
    descripcion:str

# Definir el esquema compras
class CompraBase(BaseModel):
    producto:str
    precio:float