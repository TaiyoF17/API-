from dataclasses import dataclass

@dataclass
class Comment:
    id:int|None
    id_publicacion:int
    id_usuario:int
    contenido:str
    creado_en:str|None
