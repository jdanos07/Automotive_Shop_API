from blueprints.service_ticket.service_ticketSchema import service_tickets_schema
from blueprints.mechanic import mechanics_bp
from blueprints.mechanic.mechanicSchema import mechanic_schema, mechanics_schema, login_schema
from utils.util import encode_token, token_required
from flask import request, jsonify
from marshmallow import ValidationError
from models import Mechanics, db
from sqlalchemy import select
from extensions import limiter


@mechanics_bp.route('/login', methods=['POST'])
def login():  
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
        
    except ValidationError as e:
        return jsonify({'messages':'Invalid payload, expecting username and password'}), 400
    
    query = select(Mechanics).where(Mechanics.email == email)
    mechanic = db.session.execute(query).scalar_one_or_none()

    if mechanic and mechanic.password == password:
        auth_token = encode_token(mechanic.id)

        response = {
            'status': 'success',
            'message': 'Succesfully logged in',
            'auth_token':auth_token
        }
        return jsonify(response), 200
    else:
        return jsonify({'messages': 'Invalid Username or Password'}), 401
    
@mechanics_bp.route('/', methods=['POST'])
@limiter.limit("2 per hour")
def create_mechanic():
    try: 
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_mechanic = Mechanics(
        **mechanic_data
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
    else:
        return mechanic_schema.jsonify(mechanic), 200

@mechanics_bp.route('/', methods=['PUT'])
@token_required
def update_mechanic(id):
    query = select(Mechanics).where(Mechanics.id == id)
    mechanic = db.session.execute(query).scalars().first()

    if mechanic is None:
        return jsonify({"message": "Invalid Mechanic ID"}), 400
    
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

@mechanics_bp.route('/', methods=['DELETE'])
@token_required
def delete_mechanic(mechanic_id):
    query = select(Mechanics).where(Mechanics.id == mechanic_id)
    mechanic = db.session.execute(query).scalars().first()

    if mechanic is None:
        return jsonify({"message": "Invalid mechanic ID"}), 400

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": "Mechanic deleted successfully"}), 200

@mechanics_bp.route('/tickets', methods=['GET'])
@token_required
def get_mechanic_tix(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)

    if mechanic:
    
        service_tix = mechanic.service_tickets

        return jsonify(service_tickets_schema.dump(service_tix)), 200

    else:
        return jsonify({"message": "Mechnanic is not in the system, or has no tickets."}), 400
