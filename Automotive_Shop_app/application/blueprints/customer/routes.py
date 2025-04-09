from application.blueprints.customer import customers_bp
from application.blueprints.customer.customerSchema import customer_schema, customers_schema, login_schema
from application.extensions import cache
from application.utils.util import encode_token, token_required
from flask import request, jsonify
from marshmallow import ValidationError
from application.models import Customers, Service_Tickets, db
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from application.blueprints.service_ticket.service_ticketSchema import service_tickets_schema

@customers_bp.route('/', methods=['POST'])
def create_customer():
    try: 
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_customer = Customers(
        name = customer_data['name'], 
        phone_number = customer_data['phone_number'], 
        password = customer_data['password'],
        email = customer_data['email']
        )
    
    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 201

@customers_bp.route('/login', methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']

    except ValidationError as e:
        return jsonify({'messages':'Invalid payload, expecting username and password'}), 400
    
    query = select(Customers).where(Customers.email == email)
    customer = db.session.execute(query).scalar_one_or_none()

    if customer and customer.password == password:
        auth_token = encode_token(customer.phone_number)

        response = {
            'status': 'success',
            'message': 'Succesfully logged in',
            'auth_token':auth_token
        }
        return jsonify(response), 200
    else:
        return jsonify({'messages': 'Invalid Username or Password'}), 401
    
@customers_bp.route('/', methods=['GET'])
@cache.cached(timeout=60)
def get_customers():
    query = select(Customers)
    result = db.session.execute(query).scalars().all()
    return customers_schema.jsonify(result), 200 

@customers_bp.route('/<int:phone_number>', methods=['GET'])
def get_Customer(phone_number):
    query = select(Customers).where(Customers.phone_number == phone_number)
    customer = db.session.execute(query).scalars().first()
    
    if customer == None:
        return jsonify({"messages": "invalid Customer id"}), 400
    else:
        return customer_schema.jsonify(customer), 200
    
@customers_bp.route('/', methods=['PUT'])
@token_required
@cache.cached(timeout=120)
def update_customer(phone_number):
    query = select(Customers).where(Customers.phone_number == phone_number)
    customer = db.session.execute(query).scalars().first()

    if customer is None:
        return jsonify({"messages": "Invalid customer ID"}), 400
    
    try:
        customer_data = customer_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    if 'name' in customer_data:
        customer.name = customer_data['name']
    if 'phone_number' in customer_data:
        customer.phone_number = customer_data['phone_number']
   

    db.session.commit()
    return customer_schema.jsonify(customer), 200

@customers_bp.route('/', methods=['DELETE'])
@token_required
def delete_customer(phone_number):
    query = select(Customers).where(Customers.phone_number == phone_number)
    customer = db.session.execute(query).scalars().first()

    if customer is None:
        return jsonify({"messages": "Invalid customer ID"}), 400

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"messages": "Customer deleted successfully"}), 200
    
@customers_bp.route('/my_tickets', methods=['GET'])
@token_required
def get_customerTickets(phone_number):

    query = select(Customers).where(Customers.phone_number == phone_number)
    customer = db.session.execute(query).scalar_one_or_none()


    if customer is None:
        return jsonify({"messages": "invalid Customer id"}), 400
    else:
        return service_tickets_schema.jsonify(customer.service_tickets), 200
