from typing import List, Optional
from db import Database
from models.comment import Comment

class CommentRepositoryMySQL:
    def __init__(self, db: Database):
        self.db = db

    def list_by_post(self, post_id:int) -> List[Comment]:
        conn = self.db.connect()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT id, id_publicacion, id_usuario, contenido, creado_en
            FROM comentarios WHERE id_publicacion=%s ORDER BY id ASC
        """, (post_id,))
        rows = cur.fetchall()
        cur.close(); conn.close()
        return [Comment(**row) for row in rows]

    def add(self, c: Comment) -> int:
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO comentarios (id_publicacion, id_usuario, contenido)
            VALUES (%s,%s,%s)
        """, (c.id_publicacion, c.id_usuario, c.contenido))
        conn.commit()
        new_id = cur.lastrowid
        cur.close(); conn.close()
        return new_id

    def update(self, comment_id:int, contenido:str) -> int:
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute("UPDATE comentarios SET contenido=%s WHERE id=%s", (contenido, comment_id))
        conn.commit()
        count = cur.rowcount
        cur.close(); conn.close()
        return count

    def delete(self, comment_id:int) -> int:
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM comentarios WHERE id=%s", (comment_id,))
        conn.commit()
        count = cur.rowcount
        cur.close(); conn.close()
        return count
