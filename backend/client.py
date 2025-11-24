from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Client, Plan, User, db
import json

client_bp = Blueprint('client', __name__, url_prefix='/client')

@client_bp.route('/view_my_plans', methods=['GET'])
@jwt_required()
def view_my_plans():
    try:
        # JWT identity is now a STRING user_id
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"success": False, "message": "Invalid token identity"}), 422

        user_id = int(user_id)

        # Get user from User table
        user = User.query.get(user_id)
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        # Each client uses same email as the user
        client = Client.query.filter_by(email=user.email).first()
        if not client:
            return jsonify({"success": False, "message": "Client profile not found"}), 404

        # Get latest plan for this client
        plan = Plan.query.filter_by(client_id=client.id).order_by(Plan.id.desc()).first()
        if not plan:
            return jsonify({"success": True, "plans": []})

        # Find coach name
        coach_name = "Unknown"
        if client.coach_id:
            coach = User.query.get(client.coach_id)
            if coach:
                coach_name = coach.name

        # Parse workout and nutrition safely
        try:
            workout_plan = json.loads(plan.workout_plan) if plan.workout_plan else {}
        except:
            workout_plan = {}

        try:
            nutrition_plan = json.loads(plan.nutrition_plan) if plan.nutrition_plan else {}
        except:
            nutrition_plan = {}

        return jsonify({
            "success": True,
            "plans": [{
                "plan_id": plan.id,
                "coach_name": coach_name,
                "workout_plan": workout_plan,
                "nutrition_plan": nutrition_plan
            }]
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
# ---------------------------
# LOG DAILY PROGRESS
# ---------------------------
@client_bp.route('/log_progress', methods=['POST'])
@jwt_required()
def log_progress():
    try:
        data = request.json
        workout = data.get("workout", "")
        measurements = data.get("measurements", "")
        photos = data.get("photos", "")

        user_id = get_jwt_identity()
        client = Client.query.filter_by(id=int(user_id)).first()
        if not client:
            # fallback: match by email
            user = User.query.get(user_id)
            client = Client.query.filter_by(email=user.email).first()
        if not client:
            return jsonify({"success": False, "message": "Client not found"}), 404

        new_log = Log(
            client_id=client.id,
            date=date.today(),
            workout=workout,
            measurements=measurements,
            photo=photos
        )
        db.session.add(new_log)
        db.session.commit()

        return jsonify({"success": True, "message": "Progress logged successfully!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
# ---------------------------
# VIEW PROGRESS HISTORY
# ---------------------------

@client_bp.route('/progress_history', methods=['GET'])
@jwt_required()
def progress_history():
    try:
        identity = get_jwt_identity()  # returns {"id": ..., "role": ...}
        client_id = identity['id']

        # Fetch client using user_id
        client = Client.query.filter_by(id=client_id).first()
        if not client:
            return jsonify({"success": False, "message": "Client not found"}), 404

        logs = Log.query.filter_by(client_id=client.id).order_by(Log.date.desc()).all()
        history = [
            {
                "date": l.date.strftime("%Y-%m-%d"),
                "workout": l.workout,
                "measurements": l.measurements,
                "photos": l.photo
            } for l in logs
        ]
        return jsonify({"success": True, "history": history})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

