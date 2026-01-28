from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models.video import get_dashboard_videos

video_bp = Blueprint("video", __name__)

@video_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    videos = get_dashboard_videos()
    return jsonify(videos), 200
