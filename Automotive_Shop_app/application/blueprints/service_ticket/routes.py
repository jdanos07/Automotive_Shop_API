from application.blueprints.service_ticket import service_tickets_bp
from application.blueprints.service_ticket.service_ticketSchema import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from application.models import Service_Tickets, db
from sqlalchemy import select

@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_service_ticket = Service_Tickets(**service_ticket_data)
    
    db.session.add(new_service_ticket)
    db.session.commit()
    
    return jsonify(service_ticket_schema.dump(new_service_ticket)), 201

@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    query = select(Service_Tickets)
    result = db.session.execute(query).scalars().all()
    return jsonify(service_tickets_schema.dump(result)), 200 

@service_tickets_bp.route('/<int:service_ticket_id>', methods=['GET'])
def get_service_ticket(service_ticket_id):
    service_ticket = Service_Tickets.query.get_or_404(service_ticket_id)
    return jsonify(service_ticket_schema.dump(service_ticket)), 200

@service_tickets_bp.route('/<int:service_ticket_id>', methods=['PUT'])
def update_service_ticket(service_ticket_id):
    service_ticket = Service_Tickets.query.get_or_404(service_ticket_id)
    try:
        updated_data = service_ticket_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in updated_data.items():
        setattr(service_ticket, key, value)
    
    db.session.commit()
    return jsonify(service_ticket_schema.dump(service_ticket)), 200

@service_tickets_bp.route('/<int:service_ticket_id>', methods=['DELETE'])
def delete_service_ticket(service_ticket_id):
    service_ticket = Service_Tickets.query.get_or_404(service_ticket_id)
    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({"message": "Service ticket deleted"}), 200