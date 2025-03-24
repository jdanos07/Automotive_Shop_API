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
    Each service ticket links to a customer (by phone number), a vehicle (by VIN), and a mechanic.
  
  Vehicle Management:
    Track vehicles using VINs and associate them with customers.
  
  Modular Design:
    Organized using Flask Blueprints for clean separation between different areas of functionality.

2) Project Structure

![image](https://github.com/user-attachments/assets/0ed00294-5852-4cc9-bde6-acb8c8cab713)


3) Installation

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
    

4) API Endpoints
   
  Customers
  
    GET /customers – List all customers.
    
    POST /customers – Create a new customer.
    
    GET /customers/<phone_number> – Retrieve a customer by phone number.
    
    PUT /customers/<phone_number> – Update a customer's information.
    
    DELETE /customers/<phone_number> – Delete a customer.
    
  Mechanics
  
    GET /mechanics – List all mechanics.
    
    POST /mechanics – Create a new mechanic.
    
    GET /mechanics/<employee_id> – Retrieve a mechanic by employee ID.
    
    PUT /mechanics/<employee_id> – Update mechanic details.
    
    DELETE /mechanics/<employee_id> – Delete a mechanic.
    
  Service Tickets
  
    GET /service_tickets – List all service tickets.
    
    POST /service_tickets – Create a new service ticket.
    
    GET /service_tickets/<ticket_id> – Retrieve a service ticket by ID.
    
    PUT /service_tickets/<ticket_id> – Update a service ticket.
    
    DELETE /service_tickets/<ticket_id> – Delete a service ticket.

  Vehicles

    GET /vehicles – List all vehicles.
    
    POST /vehicles – Create a new vehicles.
    
    GET /vehicles/<vin> – Retrieve a vehicles by VIN.
    
    PUT /vehicles/<vin> – Update a vehicles.
    
    DELETE /vehicles/<vin> – Delete a vehicle.
