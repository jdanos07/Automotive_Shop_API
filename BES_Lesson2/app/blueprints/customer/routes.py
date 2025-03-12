from app.blueprints.customer import customers_bp
from app.blueprints.customer.customerSchema import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Customers, db
from sqlalchemy import select, delete

customers_bp.route("/customers", methods=['POST'])
def create_customer():
    try: 
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_customer = Customers(name=customer_data['name'], email=customer_data['email'], password=customer_data['password'])
    
    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 201

customers_bp.route('/customers', methods=['GET'])
def get_customers():
    query = select(Customers)
    result = db.session.execute(query).scalars().all()
    return customers_schema.jsonify(result), 200 

customers_bp.route('/customers/<int:Customer_id>', methods=['GET'])
def get_Customer(Customer_id):
    query = select(Customer).where(Customer.id == Customer_id)
    Customer = db.session.execute(query).scalars().first()
    
    if Customer == None:
        return jsonify({"message": "invalid Customer id"}), 400
    else:
        return customers_schema.jsonify(result), 200
    
