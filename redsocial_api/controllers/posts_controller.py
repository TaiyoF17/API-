from flask import Blueprint, request, jsonify
from db import Database
from repositories.post_repository_mysql import PostRepositoryMySQL
from services.post_service import PostService
from controllers.auth_controller import require_token

posts_bp = Blueprint("posts", __name__)

def service():
    return PostService(PostRepositoryMySQL(Database()))

@posts_bp.get("/")
def listar():
    posts = service().listar()
    return jsonify([vars(p) for p in posts])

@posts_bp.get("/<int:post_id>")
def obtener(post_id:int):
    p = service().obtener(post_id)
    if not p: return jsonify({"status":"error","message":"no encontrado"}), 404
    return jsonify(vars(p))

@posts_bp.post("/")
@require_token
def crear():
    from flask import request
    data = request.get_json(silent=True) or {}
    try:
        p = service().crear(request.user_id, data)
        return jsonify(vars(p)), 201
    except Exception as e:
        return jsonify({"status":"error","message":str(e)}), 400

@posts_bp.put("/<int:post_id>")
@require_token
def actualizar(post_id:int):
    from flask import request
    data = request.get_json(silent=True) or {}
    try:
        p = service().actualizar(request.user_id, post_id, data)
        if not p: return jsonify({"status":"error","message":"no encontrado"}), 404
        return jsonify(vars(p))
    except PermissionError as pe:
        return jsonify({"status":"error","message":str(pe)}), 403
    except Exception as e:
        return jsonify({"status":"error","message":str(e)}), 400

@posts_bp.delete("/<int:post_id>")
@require_token
def eliminar(post_id:int):
    from flask import request
    try:
        ok = service().eliminar(request.user_id, post_id)
        if not ok: return jsonify({"status":"error","message":"no encontrado"}), 404
        return jsonify({"status":"success","message":"eliminado"})
    except PermissionError as pe:
        return jsonify({"status":"error","message":str(pe)}), 403

@posts_bp.post("/<int:post_id>/like")
@require_token
def like(post_id:int):
    from flask import request
    service().like(request.user_id, post_id)
    return jsonify({"status":"success","message":"like"}), 201

@posts_bp.delete("/<int:post_id>/like")
@require_token
def unlike(post_id:int):
    from flask import request
    service().unlike(request.user_id, post_id)
    return jsonify({"status":"success","message":"unlike"})
