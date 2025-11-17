import os
from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from models import db

from auth import auth_bp
from coach import coach_bp
from client import client_bp

# --------------------------
# Initialize Flask App
# --------------------------
app = Flask(
    __name__,
    static_folder="../frontend",      # Path to frontend folder
    template_folder="../frontend"     # Template folder for HTML
)

# --------------------------
# Serve HTML pages from /pages/
# --------------------------
PAGES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend/pages"))

@app.route("/pages/<path:filename>")
def serve_page(filename):
    """Serve HTML pages from frontend/pages folder"""
    return send_from_directory(PAGES_DIR, filename)

# --------------------------
# Config & Extensions
# --------------------------
app.config.from_object(Config)
CORS(app)
db.init_app(app)
jwt = JWTManager(app)

# Create uploads folder if not exists
if not os.path.exists(Config.UPLOAD_FOLDER):
    os.makedirs(Config.UPLOAD_FOLDER)

# --------------------------
# Register Blueprints (API)
# --------------------------
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(coach_bp, url_prefix='/coach')
app.register_blueprint(client_bp, url_prefix='/client')

# --------------------------
# Run the App
# --------------------------
# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()  # Create database tables if not exist
#     app.run(debug=True)
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables if not exist
    port = int(os.environ.get("PORT", 5000))  # Use Railway port or default 5000
    app.run(host="0.0.0.0", port=port)
