from flask import Blueprint

inventory_bp = Blueprint('inventory_bp', __name__)

from inventory import routes
