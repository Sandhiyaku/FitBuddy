from app import app
from models import db, User

with app.app_context():
    users = User.query.all()
    if not users:
        print("No users found.")
    else:
        for user in users:
            print(f"Email: {user.email}, Role: {user.role}, Name: {user.name}")
