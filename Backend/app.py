from flask import Flask, jsonify
from dotenv import load_dotenv
from extensions import init_db
from datetime import datetime
from routes.auth import auth_bp
from flask_jwt_extended import JWTManager
from routes.video import video_bp


load_dotenv()

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret-key"  # move to env later
jwt = JWTManager(app)

init_db()   # 👈 connect Mongo here

app.register_blueprint(auth_bp)
app.register_blueprint(video_bp)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/test-db", methods=["GET"])
def test_db():
    from extensions import db
    db.test.insert_one({"msg": "mongo is working"})
    return jsonify({"db": "connected"}), 200


@app.route("/test-user", methods=["GET"])
def test_user():
    from models.user import create_user, find_user_by_email
    from utils.password import hash_password

    email = "test@example.com"

    existing = find_user_by_email(email)
    if not existing:
        create_user(
            name="Test User",
            email=email,
            password_hash=hash_password("password123")
        )

    user = find_user_by_email(email)

    return {
        "name": user["name"],
        "email": user["email"],
        "password_hash_exists": bool(user["password_hash"])
    }


@app.route("/seed-videos")
def seed_videos():
    from extensions import db

    db.videos.insert_many([
        {
            "title": "How Startups Fail",
            "description": "Lessons from real founders",
            "youtube_id": "abc123xyz",
            "thumbnail_url": "https://img.youtube.com/vi/abc123xyz/0.jpg",
            "is_active": True
        },
        {
            "title": "Build Better APIs",
            "description": "API-first mindset",
            "youtube_id": "def456xyz",
            "thumbnail_url": "https://img.youtube.com/vi/def456xyz/0.jpg",
            "is_active": True
        }
    ])

    return {"status": "videos seeded"}



if __name__ == "__main__":
    app.run(debug=True)
