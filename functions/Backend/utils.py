from flask import Blueprint, jsonify, request
from uuid import UUID

def is_valid_uuid(val):
    try:
        UUID(str(val))
        return True
    except ValueError:
        return False
validate_bp = Blueprint('validate', __name__)

@validate_bp.route('/validate_uuid', methods=['POST'])
def validate_uuid():
    data = request.get_json()
    uuid_val = data.get("uuid")

    if not uuid_val or not is_valid_uuid(uuid_val):
        return jsonify({"message": "Invalid UUID"}), 400

    return jsonify({"message": "UUID is valid"}), 200