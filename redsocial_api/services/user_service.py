from typing import Optional
from models.user import User
from repositories.user_repository_mysql import UserRepositoryMySQL
from services.auth_service import hash_password

class UserService:
    def __init__(self, repo: UserRepositoryMySQL):
        self.repo = repo

    def registrar(self, data:dict) -> User:
        u = User(
            id=None,
            nombre=data.get("nombre","").strip(),
            apellido=data.get("apellido","").strip(),
            correo=data.get("correo","").strip().lower(),
            alias=data.get("alias","").strip(),
            contrasena_hash=hash_password(data.get("contrasena","")),
            imagen_base64=data.get("imagen_base64")
        )
        if not u.nombre or not u.apellido or not u.correo or not u.alias or not data.get("contrasena"):
            raise ValueError("Faltan campos obligatorios")
        if "@" not in u.correo:
            raise ValueError("Correo inválido")
        if self.repo.find_by_email(u.correo):
            raise ValueError("Correo ya registrado")
        u.id = self.repo.create(u)
        return u

    def perfil(self, user_id:int) -> Optional[User]:
        return self.repo.find_by_id(user_id)

    def actualizar(self, user_id:int, fields:dict) -> int:
        return self.repo.update_profile(user_id, fields)
