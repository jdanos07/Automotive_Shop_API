from flask import Flask
from .models import db
from .extensions import ma, limiter, cache
from .blueprints.customer import customers_bp
from .blueprints.mechanic import mechanics_bp
from .blueprints.service_ticket import service_tickets_bp
from .blueprints.vehicle import vehicles_bp
from .blueprints.inventory import inventory_bp
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
    'app_name': "Automotive Shop App"
    }
)

def create_app(config_name = 'DevelopmentConfig'):

    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    app.register_blueprint(customers_bp, url_prefix = '/customers')
    app.register_blueprint(mechanics_bp, url_prefix = '/mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix = '/service_tickets')
    app.register_blueprint(vehicles_bp, url_prefix = '/vehicles')
    app.register_blueprint(inventory_bp, url_prefix = '/inventory')
    app.register_blueprint(swaggerui_blueprint, url_prefix = SWAGGER_URL)
    
    return app