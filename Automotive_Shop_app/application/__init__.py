from flask import Flask
from application.models import db
from application.extensions import ma
from application.blueprints.customer import customers_bp
from application.blueprints.mechanic import mechanics_bp
from application.blueprints.service_ticket import service_tickets_bp

def create_app(config_name = 'DevelopmentConfig'):

    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(customers_bp, url_prefix = '/customers')
    app.register_blueprint(mechanics_bp, url_prefix = '/mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix = '/service_tickets')

    return app