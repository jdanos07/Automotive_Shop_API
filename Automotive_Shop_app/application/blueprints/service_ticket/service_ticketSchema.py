from application.models import Service_Tickets
from application.extensions import ma
from marshmallow import fields

class Service_TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_Tickets
        include_fk = True
        include_relationships = True
        exclude = ('customer', 'vehicle', 'consumables')

class Edit_Ticket_MechanicSchema(ma.Schema):
    mechanic_id = fields.Int(required = True)
    
    
service_ticket_schema = Service_TicketSchema()
service_tickets_schema = Service_TicketSchema(many=True)
edit_ticket_mechanics_schema = Edit_Ticket_MechanicSchema()
