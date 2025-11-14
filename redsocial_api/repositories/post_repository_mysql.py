from typing import List, Optional
from db import Database
from models.post import Post

class PostRepositoryMySQL:
    def __init__(self, db: Database):
        self.db = db

    def list_all(self) -> List[Post]:
        conn = self.db.connect()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT id, id_usuario, titulo, contenido, imagen_base64, creado_en
            FROM publicaciones ORDER BY id DESC
        """)
        rows = cur.fetchall()
        cur.close(); conn.close()
        return [Post(**row) for row in rows]

    def get(self, post_id:int) -> Optional[Post]:
        conn = self.db.connect()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, id_usuario, titulo, contenido, imagen_base64, creado_en FROM publicaciones WHERE id=%s", (post_id,))
        row = cur.fetchone()
        cur.close(); conn.close()
        return Post(**row) if row else None

    def add(self, p:Post) -> int:
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO publicaciones (id_usuario, titulo, contenido, imagen_base64)
            VALUES (%s,%s,%s,%s)
        """, (p.id_usuario, p.titulo, p.contenido, p.imagen_base64))
        conn.commit()
        new_id = cur.lastrowid
        cur.close(); conn.close()
        return new_id

    def update(self, post_id:int, p:Post) -> int:
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute("""
            UPDATE publicaciones SET titulo=%s, contenido=%s, imagen_base64=%s WHERE id=%s
        """, (p.titulo, p.contenido, p.imagen_base64, post_id))
        conn.commit()
        count = cur.rowcount
        cur.close(); conn.close()
        return count

    def delete(self, post_id:int) -> int:
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM publicaciones WHERE id=%s", (post_id,))
        conn.commit()
        count = cur.rowcount
        cur.close(); conn.close()
        return count

    def like(self, post_id:int, user_id:int) -> None:
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute("INSERT IGNORE INTO publicaciones_likes (id_publicacion, id_usuario) VALUES (%s,%s)", (post_id, user_id))
        conn.commit()
        cur.close(); conn.close()

    def unlike(self, post_id:int, user_id:int) -> None:
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM publicaciones_likes WHERE id_publicacion=%s AND id_usuario=%s", (post_id, user_id))
        conn.commit()
        cur.close(); conn.close()
