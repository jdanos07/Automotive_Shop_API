@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    query = select(Vehicle)
    result = db.session.execute(query).scalars().all()
    return vehicles_schema.jsonify(result), 200 


@app.route('/vehicles/<int:Vehicle_id>', methods=['GET'])
def get_Vehicle(Vehicle_id):
    query = select(Vehicle).where(Vehicle.id == Vehicle_id)
    Vehicle = db.session.execute(query).scalars().first()
    
    if Vehicle == None:
        return jsonify({"message": "invalid Vehicle id"}), 400
    
    return vehicles_schema.jsonify(result), 200
