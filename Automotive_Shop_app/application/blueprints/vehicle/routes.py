from application.blueprints.vehicle import vehicles_bp
from application.blueprints.vehicle.vehicleSchema import vehicle_schema, vehicles_schema
from flask import request, jsonify
from marshmallow import ValidationError
from application.models import Vehicles, db
from sqlalchemy import select

@vehicles_bp.route("/vehicles", methods=['POST'])
def create_vehicle():
    try: 
        vehicle_data = vehicle_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_vehicle = Vehicles(
        make=vehicle_data['make'], 
        model=vehicle_data['model'], 
        year=vehicle_data['year'],
        vin=vehicle_data['vin']
    )
    
    db.session.add(new_vehicle)
    db.session.commit()

    return vehicle_schema.jsonify(new_vehicle), 201


@vehicles_bp.route('/vehicles', methods=['GET'])
def get_vehicles():
    query = select(Vehicles)
    result = db.session.execute(query).scalars().all()
    return vehicles_schema.jsonify(result), 200 


@vehicles_bp.route('/vehicles/<int:Vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    query = select(Vehicles).where(Vehicles.id == vehicle_id)
    vehicle = db.session.execute(query).scalars().first()
    
    if vehicle == None:
        return jsonify({"message": "invalid Vehicle id"}), 400
    
    return vehicle_schema.jsonify(vehicle), 200

@vehicles_bp.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    query = select(Vehicles).where(Vehicles.id == vehicle_id)
    vehicle = db.session.execute(query).scalars().first()

    if vehicle is None:
        return jsonify({"message": "Invalid vehicle ID"}), 400
    
    try:
        vehicle_data = vehicle_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    if 'make' in vehicle_data:
        vehicle.make = vehicle_data['make']
    if 'model' in vehicle_data:
        vehicle.model = vehicle_data['model']
    if 'year' in vehicle_data:
        vehicle.year = vehicle_data['year']
    if 'vin' in vehicle_data:
        vehicle.vin = vehicle_data['vin']

    db.session.commit()
    return vehicle_schema.jsonify(vehicle), 200

@vehicles_bp.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    query = select(Vehicles).where(Vehicles.id == vehicle_id)
    vehicle = db.session.execute(query).scalars().first()

    if vehicle is None:
        return jsonify({"message": "Invalid vehicle ID"}), 400

    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({"message": "Vehicle deleted successfully"}), 200