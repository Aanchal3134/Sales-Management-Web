from database import db
from models import Sale, Product, User, Region, Team


from flask import Blueprint, jsonify, request
from models import db, Team, User

teams_bp = Blueprint('teams', __name__)

@teams_bp.route('/', methods=['GET'])
def get_teams():
    teams = Team.query.all()
    return jsonify([{'team_id': team.team_id, 'team_name': team.team_name, 'manager_name': team.manager.username} for team in teams])

@teams_bp.route('/', methods=['POST'])
def add_team():
    data = request.get_json()
    manager = User.query.get(data['manager_id'])
    if manager:
        new_team = Team(team_name=data['team_name'], manager_id=data['manager_id'])
        db.session.add(new_team)
        db.session.commit()
        return {"message": "Team added successfully!"}, 201

    return {"message": "Invalid manager ID."}, 400
