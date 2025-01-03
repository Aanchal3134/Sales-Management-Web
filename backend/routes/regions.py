from database import db
from models import Sale, Product, User, Region, Team


from flask import Blueprint, jsonify, request
from models import db, Region

regions_bp = Blueprint('regions', __name__)

@regions_bp.route('/', methods=['GET'])
def get_regions():
    regions = Region.query.all()
    return jsonify([{'region_id': region.region_id, 'region_name': region.region_name} for region in regions])

@regions_bp.route('/', methods=['POST'])
def add_region():
    data = request.get_json()
    new_region = Region(region_name=data['region_name'])
    db.session.add(new_region)
    db.session.commit()
    return {"message": "Region added successfully!"}, 201
