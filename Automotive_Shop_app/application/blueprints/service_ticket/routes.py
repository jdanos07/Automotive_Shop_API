from application.blueprints.service_ticket import service_tickets_bp
from application.blueprints.service_ticket.service_ticketSchema import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from application.models import Mechanics, Service_Tickets, db
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_service_ticket = Service_Tickets(**service_ticket_data)
    db.session.add(new_service_ticket)
    try:
        db.session.commit()
    except IntegrityError as err:
        db.session.rollback()
        error_str = str(err.orig)
        if 'customer' in error_str.lower():
            return jsonify({'message': 'Customer information must be input before a ticket can be created. '}), 400
        elif 'vin' in error_str.lower():
            return jsonify({'message': 'Vehicle information must be input before a ticket can be created.'}), 400
        elif 'mechanic' in error_str.lower():
            return jsonify({'message': 'Current Mechanic ID must be provided.'}), 400
        else:
            return jsonify({'message': 'A foreign key constraint failed.', 'details': error_str}), 400

    return jsonify(service_ticket_schema.dump(new_service_ticket)), 201

@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    query = select(Service_Tickets)
    result = db.session.execute(query).scalars().all()
    return jsonify(service_tickets_schema.dump(result)), 200 

@service_tickets_bp.route('/<int:ticket_id>', methods=['GET'])
def get_service_ticket(ticket_id):
    query = select(Service_Tickets).where(Service_Tickets.ticket_id == ticket_id)
    service_ticket = db.session.execute(query).scalars().first()

    if service_ticket == None:
        return jsonify({'message': 'invalid Service Ticket id'}), 400
    
    return service_ticket_schema.jsonify(service_ticket), 200


@service_tickets_bp.route('/<int:ticket_id>', methods=['PUT'])
def update_service_ticket(ticket_id):
    query = select(Service_Tickets).where(Service_Tickets.ticket_id == ticket_id)
    service_ticket = db.session.execute(query).scalars().first()

    if service_ticket is None:
        return jsonify({'message': 'Invalid Service Ticket ID'}), 400
    
    try:
        ticket_data = service_ticket_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    if 'customer_phone' in ticket_data:
        service_ticket.customer_phone = ticket_data['customer_phone']
    if 'services' in ticket_data:
        service_ticket.services = ticket_data['services']
    if 'vin' in ticket_data:
        service_ticket.vin = ticket_data['vin']
    if 'consumables' in ticket_data:
        service_ticket.consumables = ticket_data['consumables']

    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200

@service_tickets_bp.route('/<int:ticket_id>/edit', methods=['PUT'])
def update_service_ticket_mechanic(ticket_id):
    query = select(Service_Tickets).where(Service_Tickets.ticket_id == ticket_id)
    service_ticket = db.session.execute(query).scalars().first()

    if service_ticket is None:
        return jsonify({'message': 'Invalid Service Ticket ID'}), 400
    
    try:
        ticket_data = service_ticket_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    if 'mechanic_id' in ticket_data:
        mechanic_id = ticket_data['mechanic_id']
        mechanic = Mechanics.query.get(mechanic_id)
        if mechanic is None:
            return jsonify({'message': 'Invalid Mechanic ID'}), 400
        
        if mechanic in service_ticket.mechanics:
            service_ticket.mechanics.remove(mechanic)
        else:
            service_ticket.mechanics.append(mechanic)

    else:
        return jsonify({'message': 'No Mechanic ID provided.'}), 400
    db.session.commit()

    return service_ticket_schema.dump(service_ticket), 200

@service_tickets_bp.route('/<int:ticket_id>', methods=['DELETE'])
def delete_service_ticket(ticket_id):
    query = select(Service_Tickets).where(Service_Tickets.ticket_id == ticket_id)
    service_ticket = db.session.execute(query).scalars().first()

    if service_ticket is None:
        return jsonify({'message': 'Invalid Service Ticket ID'}), 400

    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({'message': 'Service Ticket deleted successfully'}), 200
