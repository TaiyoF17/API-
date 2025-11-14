from flask import Blueprint, request, jsonify
from db import Database
from repositories.user_repository_mysql import UserRepositoryMySQL
from services.user_service import UserService
from services.auth_service import create_token, verify_token, hash_password

auth_bp = Blueprint("auth", __name__)

def user_service():
    return UserService(UserRepositoryMySQL(Database()))

@auth_bp.post("/registro")
def registro():
    data = request.get_json(silent=True) or {}
    try:
        u = user_service().registrar(data)
        return jsonify({"status":"success","data":{"id":u.id,"correo":u.correo,"alias":u.alias}}), 201
    except Exception as e:
        return jsonify({"status":"error","message":str(e)}), 400

@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    correo = (data.get("correo") or "").lower()
    contrasena = data.get("contrasena") or ""
    repo = UserRepositoryMySQL(Database())
    u = repo.find_by_email(correo)
    if not u: return jsonify({"status":"error","message":"credenciales inválidas"}), 401
    if u.contrasena_hash != hash_password(contrasena):
        return jsonify({"status":"error","message":"credenciales inválidas"}), 401
    token = create_token(u.id)
    return jsonify({"status":"success","access_token": token})

def require_token(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization","")
        if not auth.startswith("Bearer "):
            return jsonify({"status":"error","message":"token requerido"}), 401
        token = auth.split(" ",1)[1].strip()
        user_id = verify_token(token)
        if not user_id:
            return jsonify({"status":"error","message":"token inválido"}), 401
        # inyecta user_id en request context
        request.user_id = user_id
        return func(*args, **kwargs)
    return wrapper
