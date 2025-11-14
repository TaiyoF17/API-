from typing import List, Optional
from models.comment import Comment
from repositories.comment_repository_mysql import CommentRepositoryMySQL

class CommentService:
    def __init__(self, repo: CommentRepositoryMySQL):
        self.repo = repo

    def listar_por_publicacion(self, post_id:int) -> List[Comment]:
        return self.repo.list_by_post(post_id)

    def crear(self, user_id:int, post_id:int, data:dict) -> Comment:
        contenido = (data.get("contenido") or "").strip()
        if not contenido:
            raise ValueError("contenido requerido")
        c = Comment(id=None, id_publicacion=post_id, id_usuario=user_id, contenido=contenido, creado_en=None)
        c.id = self.repo.add(c)
        return c

    def actualizar(self, comment_id:int, data:dict) -> Optional[Comment]:
        contenido = (data.get("contenido") or "").strip()
        if not contenido:
            raise ValueError("contenido requerido")
        updated = self.repo.update(comment_id, contenido)
        return self.obtener(comment_id) if updated else None

    def eliminar(self, comment_id:int) -> bool:
        return self.repo.delete(comment_id) > 0

    def obtener(self, comment_id:int) -> Optional[Comment]:
        # Simplificación: no se implementa GET individual de comentario en repo.
        # Se podría consultar por id si fuera necesario.
        return None
