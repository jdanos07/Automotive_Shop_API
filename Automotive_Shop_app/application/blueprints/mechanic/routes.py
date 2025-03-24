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
    
    new_mechanic = Mechanics(name=mechanic_data['name'], email=mechanic_data['email'], password=mechanic_data['password'])
    
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
    if 'email' in mechanic_data:
        mechanic.email = mechanic_data['email']
    if 'password' in mechanic_data:
        mechanic.password = mechanic_data['password']

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
