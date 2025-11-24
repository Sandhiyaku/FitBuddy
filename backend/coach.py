from flask import Blueprint, request, jsonify
from models import db, Client, Plan
from flask_jwt_extended import jwt_required, get_jwt_identity

import json

coach_bp = Blueprint('coach', __name__, url_prefix='/coach')

# ---------------------------
# GET ALL CLIENTS
# ---------------------------
@coach_bp.route("/clients", methods=["GET"])
def get_clients():
    try:
        clients = Client.query.all()
        clients_list = [
            {
                "id": c.id,
                "name": c.name,
                "email": c.email,
                "age": c.age,
                "weight": c.weight,
                "height": c.height
            } for c in clients
        ]
        return jsonify({"success": True, "clients": clients_list})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ---------------------------
# ADD NEW CLIENT
# ---------------------------

@coach_bp.route('/add_client', methods=['POST'])
@jwt_required()
def add_client():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    age = data.get("age")
    weight = data.get("weight")
    height = data.get("height")

    # Get logged-in coach
    coach_id = int(get_jwt_identity())

    if Client.query.filter_by(email=email).first():
        return jsonify({"message": "Client already exists!"}), 409

    new_client = Client(
        name=name,
        email=email,
        age=age,
        weight=weight,
        height=height,
        coach_id=coach_id   # <-- IMPORTANT
    )

    db.session.add(new_client)
    db.session.commit()

    return jsonify({"message": "Client added successfully!"}), 201

# ---------------------------
# ADD WORKOUT PLAN
# ---------------------------
@coach_bp.route('/add_workout_plan', methods=['POST'])
def add_workout_plan():
    data = request.json
    client_id = data.get("client_id")
    warmup = data.get("warmup")
    workout = data.get("workout")
    cooldown = data.get("cooldown")

    client = Client.query.get(client_id)
    if not client:
        return jsonify({"message": "Client not found"}), 404

    # Check if plan already exists
    plan = Plan.query.filter_by(client_id=client_id).order_by(Plan.id.desc()).first()

    workout_data = {
        "warmup": warmup,
        "workout": workout,
        "cooldown": cooldown
    }

    if plan:
        # Update workout_plan only
        plan.workout_plan = json.dumps(workout_data)
    else:
        # Create new plan with empty nutrition section
        plan = Plan(
            client_id=client_id,
            workout_plan=json.dumps(workout_data),
            nutrition_plan=""
        )
        db.session.add(plan)

    db.session.commit()
    return jsonify({"message": "Workout plan saved successfully!"}), 201

# ---------------------------
# VIEW ALL WORKOUT + NUTRITION PLANS
# ---------------------------
@coach_bp.route("/view_workout_plans", methods=["GET"])
def view_workout_plans():
    try:
        plans = Plan.query.order_by(Plan.id.desc()).all()
        plans_list = []
        for p in plans:
            client = Client.query.get(p.client_id)
            plans_list.append({
                "plan_id": p.id,
                "client_id": p.client_id,
                "client_name": client.name if client else "Unknown",
                "workout_plan": json.loads(p.workout_plan) if p.workout_plan else {},
                "nutrition_plan": json.loads(p.nutrition_plan) if p.nutrition_plan else {}
            })
        return jsonify({"success": True, "plans": plans_list})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
