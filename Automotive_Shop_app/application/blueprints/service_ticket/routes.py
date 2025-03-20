from application.blueprints.service_ticket import service_tickets_bp
from application.blueprints.service_ticket.service_ticketSchema import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from application.models import Service_Tickets, db
from sqlalchemy import select

service_tickets_bp.route("/servce_tickets", methods=['POST'])
def create_service_ticket():
    try: 
				# Deserialize and validate input data
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
		#use data to create an instance of service_ticket
    new_service_ticket = Service_Tickets(name=service_ticket_data['name'], email=service_ticket_data['email'], password=service_ticket_data['password'])
    
		#save new_service_ticket to the database
    db.session.add(new_service_ticket)
    db.session.commit()

		# Use schema to return the serialized data of the created service_ticket
    return service_ticket_schema.jsonify(new_service_ticket), 201

service_tickets_bp.route('/service_tickets', methods=['GET'])
def get_service_tickets():
    query = select(Service_Tickets)
    result = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(result), 200 

service_tickets_bp.route('/service_tickets/<int:Service_Ticket_id>', methods=['GET'])
def get_Service_Ticket(Service_Ticket_id):
    pass