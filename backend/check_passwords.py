from app import app
from models import db, User
from werkzeug.security import check_password_hash

common_passwords = ['password', '123456', '12345678', 'admin', 'secret', 'coach', 'client']

with app.app_context():
    users = User.query.all()
    found = False
    for user in users:
        for pwd in common_passwords:
            if check_password_hash(user.password, pwd):
                print(f"MATCH FOUND -> Email: {user.email}, Password: {pwd}, Role: {user.role}")
                found = True
                break
    if not found:
        print("No common passwords matched.")
