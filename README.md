Automotive Shop Management Application

This is a Flask-based web application designed to streamline operations for an automotive shop. The application provides a RESTful API to manage customers, mechanics, vehicles, and service tickets. It leverages SQLAlchemy for ORM, Marshmallow for serialization/validation, and Blueprints for modular organization.

1) Features

  Customer Management:
    Create, view, update, and delete customer records.
    Customers are identified by their phone number, which serves as a primary key.
  
  Mechanic Management:
    Manage mechanic profiles, including contact details, skill level, and hourly rates.
  
  Service Ticket Management:
    Create, view, update, and delete service tickets.
    Each service ticket links to a customer (by phone number), a vehicle (by VIN), and any mechanic that has been assigned to that ticket.
  
  Vehicle Management:
    Track vehicles using VINs and associate them with customers.
  
  Modular Design:
    Organized using Flask Blueprints for clean separation between different areas of functionality.

2) Installation

Clone the Repository:

    bash
    
    git clone https://github.com/yourusername/automotive-shop-app.git
    cd automotive-shop-app

Create a Virtual Environment:

    bash
    
    python -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    
Install Dependencies:

    bash
    
    pip install -r requirements.txt
    
3) Run Flask_app

4) Navigate to Swagger Documentaion:

    localhost/api/docs

    Here the user can find information concerning the end routes, app structure, as well as test the endpoints for expected results