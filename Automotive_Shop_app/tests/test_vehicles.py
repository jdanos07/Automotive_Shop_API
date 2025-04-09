from application import create_app
from application.models import db
import unittest

class TestVehicles(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    def test_create_vehicle(self):
        vehicle_payload = {'vin': '1234567890abcdefg', 'customer_phone': '1234567890'}

        post_response = self.client.post('/vehicles/', json = vehicle_payload)
        self.assertEqual(post_response.status_code, 201)
        self.assertEqual(post_response.json['vin'], '1234567890abcdefg')

    def test_invalid_creation(self):
        vehicle_payload = {
            'customer_phone': '1234567890'
        }

        response = self.client.post('/vehicles/', json=vehicle_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['vin'], ['Missing data for required field.'])

    def test_get_all_vehicle(self):
        response = self.client.get('/vehicles/')
        self.assertEqual(response.status_code, 200)

    def test_get_one_consumalbe(self):
        vehicle_payload = {'vin': '1234567890abcdefg', 'customer_phone': '1234567890'}
        post_respsonse = self.client.post('/vehicles/', json=vehicle_payload)
        self.assertEqual(post_respsonse.status_code, 201)

        vehicle = post_respsonse.get_json()
        vehicle_id = vehicle['id']       
        
        response = self.client.get(f'/vehicles/{vehicle_id}')
        self.assertEqual(response.status_code, 200)

    def test_update_vehicle(self):
        vehicle_payload = {'vin': '1234567890abcdefg', 'customer_phone': '1234567890'}
        post_respsonse = self.client.post('/vehicles/', json=vehicle_payload)
        self.assertEqual(post_respsonse.status_code, 201)

        vehicle = post_respsonse.get_json()
        vehicle_id = vehicle['id']  

        updated_payload = {'vin': '1234567890abcdefh', 'customer_phone': '0987654321'}
        
        response = self.client.put(f'/vehicles/{vehicle_id}', json=updated_payload)
        self.assertEqual(response.status_code, 200)

    def test_delete_vehicle(self):
        vehicle_payload = {'vin': '1234567890abcdefg', 'customer_phone': '1234567890'}
        post_respsonse = self.client.post('/vehicles/', json=vehicle_payload)
        self.assertEqual(post_respsonse.status_code, 201)

        vehicle = post_respsonse.get_json()
        vehicle_id = vehicle['id']       
        
        response = self.client.delete(f'/vehicles/{vehicle_id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()