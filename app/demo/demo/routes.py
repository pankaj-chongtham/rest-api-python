from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

demo_bp = Blueprint('demo', __name__)

@demo_bp.route('/ping')
@jwt_required()
def ping():
    return jsonify({'message': f'You are reaching demo Application.'})
