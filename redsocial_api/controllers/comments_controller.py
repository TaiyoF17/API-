from flask import Blueprint, request, jsonify
from db import Database
from repositories.comment_repository_mysql import CommentRepositoryMySQL
from services.comment_service import CommentService
from controllers.auth_controller import require_token

comments_bp = Blueprint("comments", __name__)

def service():
    return CommentService(CommentRepositoryMySQL(Database()))

@comments_bp.get("/publicaciones/<int:post_id>/comentarios")
def listar(post_id:int):
    cs = service().listar_por_publicacion(post_id)
    return jsonify([vars(c) for c in cs])

@comments_bp.post("/publicaciones/<int:post_id>/comentarios")
@require_token
def crear(post_id:int):
    from flask import request
    data = request.get_json(silent=True) or {}
    try:
        c = service().crear(request.user_id, post_id, data)
        return jsonify(vars(c)), 201
    except Exception as e:
        return jsonify({"status":"error","message":str(e)}), 400

@comments_bp.put("/comentarios/<int:comment_id>")
@require_token
def actualizar(comment_id:int):
    data = request.get_json(silent=True) or {}
    try:
        c = service().actualizar(comment_id, data)
        if not c: return jsonify({"status":"error","message":"no encontrado"}), 404
        return jsonify(vars(c))
    except Exception as e:
        return jsonify({"status":"error","message":str(e)}), 400

@comments_bp.delete("/comentarios/<int:comment_id>")
@require_token
def eliminar(comment_id:int):
    ok = service().eliminar(comment_id)
    if not ok: return jsonify({"status":"error","message":"no encontrado"}), 404
    return jsonify({"status":"success","message":"eliminado"})
