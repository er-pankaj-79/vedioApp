import extensions
from datetime import datetime

def create_user(name, email, password_hash):
    return extensions.db.users.insert_one({
        "name": name,
        "email": email,
        "password_hash": password_hash,
        "created_at": datetime.utcnow()
    })

def find_user_by_email(email):
    return extensions.db.users.find_one({"email": email})
