import extensions

def serialize_video(video):
    video["_id"] = str(video["_id"])
    return video

def get_dashboard_videos(limit=2):
    videos = extensions.db.videos.find(
        {"is_active": True},
        {"youtube_id": 0}   # hide youtube_id
    ).limit(limit)

    return [serialize_video(v) for v in videos]
