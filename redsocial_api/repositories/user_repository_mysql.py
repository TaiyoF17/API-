from typing import Optional, Dict
from db import Database
from models.user import User

class UserRepositoryMySQL:
    def __init__(self, db: Database):
        self.db = db

    def find_by_email(self, correo:str) -> Optional[User]:
        conn = self.db.connect()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, nombre, apellido, correo, alias, contrasena_hash, imagen_base64 FROM usuarios WHERE correo=%s", (correo,))
        row = cur.fetchone()
        cur.close(); conn.close()
        return User(**row) if row else None

    def find_by_id(self, user_id:int) -> Optional[User]:
        conn = self.db.connect()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, nombre, apellido, correo, alias, contrasena_hash, imagen_base64 FROM usuarios WHERE id=%s", (user_id,))
        row = cur.fetchone()
        cur.close(); conn.close()
        return User(**row) if row else None

    def create(self, u:User) -> int:
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO usuarios (nombre, apellido, correo, alias, contrasena_hash, imagen_base64)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (u.nombre, u.apellido, u.correo, u.alias, u.contrasena_hash, u.imagen_base64))
        conn.commit()
        new_id = cur.lastrowid
        cur.close(); conn.close()
        return new_id

    def update_profile(self, user_id:int, fields:Dict) -> int:
        allowed = ["nombre","apellido","alias","imagen_base64"]
        sets = []
        vals = []
        for k,v in fields.items():
            if k in allowed:
                sets.append(f"{k}=%s")
                vals.append(v)
        if not sets:
            return 0
        vals.append(user_id)
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute(f"UPDATE usuarios SET {', '.join(sets)} WHERE id=%s", tuple(vals))
        conn.commit()
        count = cur.rowcount
        cur.close(); conn.close()
        return count
