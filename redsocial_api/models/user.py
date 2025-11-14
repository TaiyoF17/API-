from dataclasses import dataclass

@dataclass
class User:
    id:int|None
    nombre:str
    apellido:str
    correo:str
    alias:str
    contrasena_hash:str
    imagen_base64:str|None
