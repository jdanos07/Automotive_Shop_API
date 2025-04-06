from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify
import jwt
import jose

SECRET_KEY = "sugar plum"

def encode_token(user_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0,hours=1),
        'iat': datetime.now(timezone.utc), 
        'sub':  str(user_id)
        }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        
            if not token:
                return jsonify({'message': 'Token is missing!'}), 400

            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                user_id = data['sub']  
                
            except jose.exceptions.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired!'}), 400
            except jose.exceptions.JWTError:
                return jsonify({'message': 'Invalid token!'}), 400

            return f(user_id, *args, **kwargs)
        
        else:
            return jsonify({'message': 'Login in first!'}), 400

    return decorated