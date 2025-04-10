from application import create_app
from application.models import db, Mechanics
from application.utils.util import encode_token

import unittest

class TestMechanics(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.mechanic = Mechanics(name='test_mechanic', phone_number='1234567895', password='test', email= 'test@test.com', skill_level= 'test', hourly_rate = 50)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
            mechanic_id = self.mechanic.phone_number       
        self.token = encode_token(mechanic_id)
        self.client = self.app.test_client()

    def test_create_mechanic(self):
        mechanic_payload = {'phone_number': '1234567890','name': 'test', 'password': 'tests', 'email': 'test5@test.com', 'skill_level': 'test', 'hourly_rate': 50}

        post_response = self.client.post('/mechanics/', json = mechanic_payload)
        self.assertEqual(post_response.status_code, 201)
        self.assertEqual(post_response.json['name'], 'test')
        self.assertEqual(post_response.json['phone_number'], '1234567890')

    def test_invalid_creation(self):
        mechanic_payload = {'name': 'test', 'password': 'tests', 'email': 'test@test.com', 'skill_level': 'test', 'hourly_rate': 50}

        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['phone_number'], ['Missing data for required field.'])

    def test_get_all_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)

    def test_get_one_mechanic(self):
        mechanic_payload = {'phone_number': '1234567890','name': 'test', 'password': 'tests', 'email': 'test1@test.com', 'skill_level': 'test', 'hourly_rate': 50}
        post_response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(post_response.status_code, 201)

        mechanic = post_response.get_json()
        mechanic_id = mechanic['id']       
        
        response = self.client.get(f'/mechanics/{mechanic_id}')
        self.assertEqual(response.status_code, 200)

    def test_update_mechanic(self):
        updated_payload = {'phone_number': '1234567897','name': 'test', 'password': 'toast', 'email': 'test3@test.com', 'skill_level': 'test', 'hourly_rate': 50}

        headers = {'Authorization': "Bearer " + self.test_mechanic_login()}

        response = self.client.put(f'/mechanics/', json=updated_payload, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_mechanic_login(self):
        credentials = {"email": "test@test.com", "password": "test"}

        response = self.client.post('/mechanics/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        return response.json['auth_token']

    def test_delete_mechanic(self):
        headers = {'Authorization': "Bearer " + self.test_mechanic_login()}
  
        response = self.client.delete(f'/mechanics/', headers=headers)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()