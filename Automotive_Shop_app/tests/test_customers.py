from application import create_app
from application.models import db
import unittest

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    def test_create_customer(self):
        customer_payload = {'name': 'oil','price': 2.50}

        post_response = self.client.post('/customers/', json = customer_payload)
        self.assertEqual(post_response.status_code, 201)
        self.assertEqual(post_response.json['name'], 'oil')

    def test_invalid_creation(self):
        customer_payload ={'name': 'oil'}

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['name'], ['Missing data for required field.'])

    def test_get_all_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)

    def test_get_one_customer(self):
        customer_payload = {'name': 'test', 'price': 2.50}
        post_respsonse = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(post_respsonse.status_code, 201)

        customer = post_respsonse.get_json()
        customer_id = customer['id']       
        
        response = self.client.get(f'/customers/{customer_id}')
        self.assertEqual(response.status_code, 200)

    def test_update_customer(self):
        customer_payload = {'name': 'test', 'price': 2.50}
        post_respsonse = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(post_respsonse.status_code, 201)

        customer = post_respsonse.get_json()
        customer_id = customer['id']  

        updated_payload = {'name': 'best', 'price': 3.01}     
        
        response = self.client.put(f'/customers/{customer_id}', json=updated_payload)
        self.assertEqual(response.status_code, 200)

    def test_delete_customer(self):
        customer_payload = {'name': 'test', 'price': 2.50}
        post_respsonse = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(post_respsonse.status_code, 201)

        customer = post_respsonse.get_json()
        customer_id = customer['id']       
        
        response = self.client.delete(f'/customers/{customer_id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()