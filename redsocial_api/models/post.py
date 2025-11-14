from dataclasses import dataclass

@dataclass
class Post:
    id:int|None
    id_usuario:int
    titulo:str
    contenido:str
    imagen_base64:str|None
    creado_en:str|None
