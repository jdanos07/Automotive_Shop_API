from application.blueprints.inventory import inventory_bp
from application.blueprints.inventory.inventorySchema import consumable_schema, consumables_schema
from application.extensions import cache
from flask import request, jsonify
from marshmallow import ValidationError
from application.models import Inventory, db
from sqlalchemy import select

@inventory_bp.route('/', methods=['POST'])
def create_consumable():
    try: 
        consumable_data = consumable_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_consumable = Inventory(
        name = consumable_data['name'], 
        price = consumable_data['price'], 
        )
    
    db.session.add(new_consumable)
    db.session.commit()

    return consumable_schema.jsonify(new_consumable), 201

@inventory_bp.route('/', methods=['GET'])
@cache.cached(timeout=60)
def get_consumable():
    query = select(Inventory)
    result = db.session.execute(query).scalars().all()
    return consumables_schema.jsonify(result), 200 

@inventory_bp.route('/<id>', methods=['GET'])
def get_Consumable(id):
    query = select(Inventory).where(Inventory.id == id)
    consumable = db.session.execute(query).scalars().first()
    
    if consumable == None:
        return jsonify({"message": "invalid Consumable id"}), 400
    else:
        return consumable_schema.jsonify(consumable), 200
    
@inventory_bp.route('/<id>', methods=['PUT'])
@cache.cached(timeout=120)
def update_consumable(id):
    query = select(Inventory).where(Inventory.id == id)
    consumable = db.session.execute(query).scalars().first()

    if consumable is None:
        return jsonify({"message": "Invalid Consumable ID"}), 400
    
    try:
        consumable_data = consumable_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    if 'name' in consumable_data:
        consumable.name = consumable_data['name']
    if 'price' in consumable_data:
        consumable.price = consumable_data['price']
   

    db.session.commit()
    return consumable_schema.jsonify(consumable), 200

@inventory_bp.route('/<id>', methods=['DELETE'])
def delete_consumable(id):
    query = select(Inventory).where(Inventory.id == id)
    consumable = db.session.execute(query).scalars().first()

    if consumable is None:
        return jsonify({"message": "Invalid Consumable ID"}), 400

    db.session.delete(consumable)
    db.session.commit()
    return jsonify({"message": "Consumable deleted successfully"}), 200
    
