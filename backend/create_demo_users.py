from app import app
from models import db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Create a Coach
    coach_email = "demo_coach@example.com"
    if not User.query.filter_by(email=coach_email).first():
        coach = User(
            name="Demo Coach",
            email=coach_email,
            password=generate_password_hash("password123"),
            role="coach"
        )
        db.session.add(coach)
        print(f"Created Coach: {coach_email} / password123")
    else:
        print(f"Coach {coach_email} already exists.")

    # Create a Client
    client_email = "demo_client@example.com"
    if not User.query.filter_by(email=client_email).first():
        client = User(
            name="Demo Client",
            email=client_email,
            password=generate_password_hash("password123"),
            role="client"
        )
        db.session.add(client)
        print(f"Created Client: {client_email} / password123")
    else:
        print(f"Client {client_email} already exists.")

    db.session.commit()
