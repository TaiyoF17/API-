from flask import Flask
from controllers.auth_controller import auth_bp
from controllers.users_controller import users_bp
from controllers.posts_controller import posts_bp
from controllers.comments_controller import comments_bp

app = Flask(__name__)

# Rutas (estilo ejemplo)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(users_bp, url_prefix="/usuarios")
app.register_blueprint(posts_bp, url_prefix="/publicaciones")
app.register_blueprint(comments_bp, url_prefix="")

if __name__ == "__main__":
    app.run(debug=True)
