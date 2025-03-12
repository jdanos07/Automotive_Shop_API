@app.route("/mechanics", methods=['POST'])
def create_mechanic():
    try: 
				# Deserialize and validate input data
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
		#use data to create an instance of mechanic
    new_mechanic = mechanic(name=mechanic_data['name'], email=mechanic_data['email'], password=mechanic_data['password'])
    
		#save new_mechanic to the database
    db.session.add(new_mechanic)
    db.session.commit()

		# Use schema to return the serialized data of the created mechanic
    return mechanic_schema.jsonify(new_mechanic), 201

@app.route('/mechanics', methods=['GET'])
def get_mechanics():
    query = select(Mechanic)
    result = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(result), 200 

@app.route('/mechanics/<int:Mechanic_id>', methods=['GET'])
def get_Mechanic(Mechanic_id):
    query = select(Mechanic).where(Mechanic.id == Mechanic_id)
    Mechanic = db.session.execute(query).scalars().first()
    
    if Mechanic == None:
        return jsonify({"message": "invalid Mechanic id"}), 400
    
    return mechanics_schema.jsonify(result), 200
#--------------VEHICLES-------------