from application.blueprints.mechanic import mechanics_bp
from application.blueprints.mechanic.mechanicSchema import mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from application.models import Mechanics, db
from sqlalchemy import select

@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    try: 
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_mechanic = Mechanics(
        name=mechanic_data['name'],
        phone_number=mechanic_data.get('phone_number'),
        skill_level=mechanic_data['skill_level'],
        hourly_rate=mechanic_data['hourly_rate']
    )
    
    db.session.add(new_mechanic)
    db.session.commit()

    return mechanic_schema.jsonify(new_mechanic), 201

@mechanics_bp.route('/', methods=['GET'])
def get_mechanics():
    query = select(Mechanics)
    result = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(result), 200 

@mechanics_bp.route('/<int:mechanic_id>', methods=['GET'])
def get_Mechanic(mechanic_id):
    query = select(Mechanics).where(Mechanics.id == mechanic_id)
    mechanic = db.session.execute(query).scalars().first()
    
    if mechanic == None:
        return jsonify({"message": "invalid Mechanic id"}), 400
    
    return mechanic_schema.jsonify(mechanic), 200

@mechanics_bp.route('/<int:mechanic_id>', methods=['PUT'])
def update_mechanic(mechanic_id):
    query = select(Mechanics).where(Mechanics.id == mechanic_id)
    mechanic = db.session.execute(query).scalars().first()

    if mechanic is None:
        return jsonify({"message": "Invalid mechanic ID"}), 400
    
    try:
        mechanic_data = mechanic_schema.load(request.json, partial=True) 
    except ValidationError as e:
        return jsonify(e.messages), 400

    if 'name' in mechanic_data:
        mechanic.name = mechanic_data['name']
    if 'phone_number' in mechanic_data:
        mechanic.phone_number = mechanic_data['phone_number']
    if 'skill_level' in mechanic_data:
        mechanic.skill_level = mechanic_data['skill_level']
    if 'hourly_rate' in mechanic_data:
        mechanic.hourly_rate = mechanic_data['hourly_rate']

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

@mechanics_bp.route('/<int:mechanic_id>', methods=['DELETE'])
def delete_mechanic(mechanic_id):
    query = select(Mechanics).where(Mechanics.id == mechanic_id)
    mechanic = db.session.execute(query).scalars().first()

    if mechanic is None:
        return jsonify({"message": "Invalid mechanic ID"}), 400

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": "Mechanic deleted successfully"}), 200
