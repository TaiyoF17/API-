from typing import List, Optional
from models.post import Post
from repositories.post_repository_mysql import PostRepositoryMySQL

class PostService:
    def __init__(self, repo: PostRepositoryMySQL):
        self.repo = repo

    def listar(self) -> List[Post]:
        return self.repo.list_all()

    def obtener(self, post_id:int) -> Optional[Post]:
        return self.repo.get(post_id)

    def crear(self, user_id:int, data:dict) -> Post:
        p = Post(
            id=None,
            id_usuario=user_id,
            titulo=(data.get("titulo") or "").strip(),
            contenido=(data.get("contenido") or "").strip(),
            imagen_base64=data.get("imagen_base64"),
            creado_en=None
        )
        if not p.titulo or not p.contenido:
            raise ValueError("titulo y contenido son obligatorios")
        new_id = self.repo.add(p)
        p.id = new_id
        return p

    def actualizar(self, user_id:int, post_id:int, data:dict) -> Optional[Post]:
        p = self.obtener(post_id)
        if not p: return None
        if p.id_usuario != user_id:
            raise PermissionError("No puedes editar esta publicación")
        p.titulo = data.get("titulo", p.titulo).strip()
        p.contenido = data.get("contenido", p.contenido).strip()
        p.imagen_base64 = data.get("imagen_base64", p.imagen_base64)
        self.repo.update(post_id, p)
        return p

    def eliminar(self, user_id:int, post_id:int) -> bool:
        p = self.obtener(post_id)
        if not p: return False
        if p.id_usuario != user_id:
            raise PermissionError("No puedes eliminar esta publicación")
        return self.repo.delete(post_id) > 0

    def like(self, user_id:int, post_id:int):
        self.repo.like(post_id, user_id)

    def unlike(self, user_id:int, post_id:int):
        self.repo.unlike(post_id, user_id)
