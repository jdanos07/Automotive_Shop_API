from flask import Blueprint

customers_bp = Blueprint('customers_bp', __name__)

from blueprints.customer import routes
