from flask import Blueprint, request, jsonify
from db import Database
from repositories.user_repository_mysql import UserRepositoryMySQL
from services.user_service import UserService
from controllers.auth_controller import require_token

users_bp = Blueprint("users", __name__)

def service():
    return UserService(UserRepositoryMySQL(Database()))

@users_bp.get("/perfil")
@require_token
def perfil():
    from flask import request
    u = service().perfil(request.user_id)
    if not u: 
        return jsonify({"status":"error","message":"no encontrado"}), 404
    data = {"id":u.id,"nombre":u.nombre,"apellido":u.apellido,"correo":u.correo,"alias":u.alias,"imagen_base64":u.imagen_base64}
    return jsonify({"status":"success","data":data})

@users_bp.put("/perfil")
@require_token
def actualizar():
    from flask import request
    fields = request.get_json(silent=True) or {}
    updated = service().actualizar(request.user_id, fields)
    if not updated:
        return jsonify({"status":"error","message":"nada para actualizar"}), 400
    return jsonify({"status":"success","message":"perfil actualizado"})
