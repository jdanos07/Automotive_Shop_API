from application import create_app
from application.models import db
import unittest

# run with - cd Automotive_Shop_app
#            python -m unittest discover tests

class TestServiceTickets(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()

        self.client = self.app.test_client()

    def test_create_service_ticket(self):
        service_ticket_payload = {'customer_phone': '1234567890', 'vin': '1234567890abcdefg', 'services': 'test'}

        post_response = self.client.post('/service_tickets/', json = service_ticket_payload)
        self.assertEqual(post_response.status_code, 201)
        self.assertEqual(post_response.json['customer_phone'], '1234567890')

    def test_invalid_creation(self):
        service_ticket_payload = {'services': 'test'}


        response = self.client.post('/service_tickets/', json=service_ticket_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['customer_phone'], ['Missing data for required field.'])

    def test_get_all_service_ticket(self):
        response = self.client.get('/service_tickets/')
        self.assertEqual(response.status_code, 200)

    def test_get_one_service_ticket(self):
        service_ticket_payload = {'customer_phone': '1234567890', 'vin': '1234567890abcdefg', 'services': 'test'}
        post_respsonse = self.client.post('/service_tickets/', json=service_ticket_payload)
        self.assertEqual(post_respsonse.status_code, 201)

        service_ticket = post_respsonse.get_json()
        service_ticket_id = service_ticket['ticket_id']       
        
        response = self.client.get(f'/service_tickets/{service_ticket_id}')
        self.assertEqual(response.status_code, 200)

    def test_update_service_ticket(self):
        service_ticket_payload = {'customer_phone': '1234567890', 'vin': '1234567890abcdefg', 'services': 'test'}
        post_respsonse = self.client.post('/service_tickets/', json=service_ticket_payload)
        self.assertEqual(post_respsonse.status_code, 201)

        service_ticket = post_respsonse.get_json()
        service_ticket_id = service_ticket['ticket_id']  

        updated_payload = {'customer_phone': '1234567890', 'vin': '1234567890abcdefg', 'services': 'toast'}
        
        response = self.client.put(f'/service_tickets/{service_ticket_id}', json=updated_payload)
        self.assertEqual(response.status_code, 200)
    
    def test_edit_service_ticket_mechanic(self):
        service_ticket_payload = {'customer_phone': '1234567890', 'vin': '1234567890abcdefg', 'services': 'test'}
        post_response = self.client.post('/service_tickets/', json=service_ticket_payload)
        self.assertEqual(post_response.status_code, 201)

        with self.app.app_context():
            from application.models import Mechanics
            mechanic = Mechanics(phone_number='1112223333', name='Test Mechanic', 
                                 skill_level='expert', hourly_rate=50, 
                                 email='mechanic@test.com', password='pass')
            db.session.add(mechanic)
            db.session.commit()

        service_ticket = post_response.get_json()
        service_ticket_id = service_ticket['ticket_id']

        edit_payload = {'mechanic_id': 1}

        response = self.client.put(f'/service_tickets/{service_ticket_id}/edit', json=edit_payload)
        self.assertEqual(response.status_code, 200)

    def test_delete_service_ticket(self):
        service_ticket_payload = {'customer_phone': '1234567890', 'vin': '1234567890abcdefg', 'services': 'test'}
        post_respsonse = self.client.post('/service_tickets/', json=service_ticket_payload)
        self.assertEqual(post_respsonse.status_code, 201)

        service_ticket = post_respsonse.get_json()
        service_ticket_id = service_ticket['ticket_id']       
        
        response = self.client.delete(f'/service_tickets/{service_ticket_id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()