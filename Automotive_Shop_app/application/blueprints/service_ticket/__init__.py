from flask import Blueprint

service_tickets_bp = Blueprint('service_tickets_bp', __name__)

from blueprints.service_ticket import routes
