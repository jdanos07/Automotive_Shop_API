from application import create_app
from application.models import db, Customers
from application.utils.util import encode_token
import unittest

# run with - python -m unittest discover tests


class TestCustomers(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.customer = Customers(name='test_customer', phone_number='1234567895', password='test', email= 'test@test.com')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
            customer_id = self.customer.phone_number       
        self.token = encode_token(customer_id)
        self.client = self.app.test_client()

    def test_create_customer(self):
        customer_payload = {'phone_number': '1234567890','name': 'test', 'password': 'tests', 'email': 'test5@test.com'}

        post_response = self.client.post('/customers/', json = customer_payload)
        self.assertEqual(post_response.status_code, 201)
        self.assertEqual(post_response.json['name'], 'test')
        self.assertEqual(post_response.json['phone_number'], '1234567890')

    def test_invalid_creation(self):
        customer_payload = {'name': 'test', 'password': 'tests', 'email': 'test@test.com'}

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['phone_number'], ['Missing data for required field.'])

    def test_get_all_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)

    def test_get_one_customer(self):
        customer_payload = {'phone_number': '1234567890','name': 'test', 'password': 'tests', 'email': 'test1@test.com'}
        post_response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(post_response.status_code, 201)

        customer = post_response.get_json()
        customer_id = customer['phone_number']       
        
        response = self.client.get(f'/customers/{customer_id}')
        self.assertEqual(response.status_code, 200)

    def test_update_customer(self):
        updated_payload = {'phone_number': '1234567897','name': 'test', 'password': 'toast', 'email': 'test3@test.com'}

        headers = {'Authorization': "Bearer " + self.test_customer_login()}

        response = self.client.put(f'/customers/', json=updated_payload, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_customer_login(self):
        credentials = {"email": "test@test.com", "password": "test"}

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        return response.json['auth_token']

    def test_delete_customer(self):
        headers = {'Authorization': "Bearer " + self.test_customer_login()}
  
        response = self.client.delete(f'/customers/', headers=headers)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()