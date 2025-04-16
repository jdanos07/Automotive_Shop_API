from flask import Blueprint

mechanics_bp = Blueprint('mechanics_bp', __name__)

from blueprints.mechanic import routes
