from application.blueprints.customer import customers_bp
from application.blueprints.customer.customerSchema import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from application.models import Customers, db
from sqlalchemy import select

@customers_bp.route("/customers", methods=['POST'])
def create_customer():
    try: 
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_customer = Customers(name = customer_data['name'], email =customer_data['email'], password = customer_data['password'])
    
    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 201

@customers_bp.route('/customers', methods=['GET'])
def get_customers():
    query = select(Customers)
    result = db.session.execute(query).scalars().all()
    return customers_schema.jsonify(result), 200 

@customers_bp.route('/customers/<int:Customer_id>', methods=['GET'])
def get_Customer(customer_id):
    query = select(Customers).where(Customers.id == customer_id)
    customer = db.session.execute(query).scalars().first()
    
    if customer == None:
        return jsonify({"message": "invalid Customer id"}), 400
    else:
        return customers_schema.jsonify(customer), 200
    
@customers_bp.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    query = select(Customers).where(Customers.id == customer_id)
    customer = db.session.execute(query).scalars().first()

    if customer is None:
        return jsonify({"message": "Invalid customer ID"}), 400
    
    try:
        customer_data = customer_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    if 'name' in customer_data:
        customer.name = customer_data['name']
    if 'email' in customer_data:
        customer.email = customer_data['email']
    if 'password' in customer_data:
        customer.password = customer_data['password']

    db.session.commit()
    return customer_schema.jsonify(customer), 200

@customers_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    query = select(Customers).where(Customers.id == customer_id)
    customer = db.session.execute(query).scalars().first()

    if customer is None:
        return jsonify({"message": "Invalid customer ID"}), 400

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted successfully"}), 200
    
