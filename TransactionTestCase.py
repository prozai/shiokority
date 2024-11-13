import unittest
import requests
import json
from unittest.mock import patch

class TransactionTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test configuration."""
        self.base_url = "https://api.shiokority.online/consumer"
        self.session = requests.Session()
        self.consumer_credentials = {
            "email": "usertest@example.com",
            "password": "123"
        }
        # Store JWT token
        self.access_token = None

    def login(self):
        """Helper method to log in and get JWT token."""
        response = self.session.post(
            f"{self.base_url}/login-consumer",
            json=self.consumer_credentials
        )
        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access_token']
            return True
        return False
    
    def test_01_send_payment_valid(self):
        """Test payment processing with valid data."""
        self.login()
        
        payment_data = {
            "cust_email":"usertest@example.com",
            "amount":"10",
            "cardNumber":"7285185555042423",
            "expiryDate":"12/25",
            "cvv":"111",
            "uen":"53339185K"
        }
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = self.session.post(
            f"{self.base_url}/send-payment",
            headers=headers,
            json=payment_data
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        print("✓ Valid payment test passed")

    def test_02_send_payment_invalid_uen(self):
        """Test payment processing with invalid UEN."""
        self.login()
        
        payment_data = {
            "uen": "invalid-uen",
            "cardNumber": "4111111111111111",
            "cvv": "123",
            "expiryDate": "12/25",
            "amount": "100.00"
        }
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = self.session.post(
            f"{self.base_url}/send-payment",
            headers=headers,
            json=payment_data
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])
        print("✓ Invalid UEN payment test passed")

    def test_03_send_payment_invalid_card_information(self):
        """Test payment processing with invalid card information."""
        self.login()
        
        payment_data = {
            "uen": "53339185K",
            "cardNumber": "1111111111111111",
            "cvv": "123",
            "expiryDate": "12/25",
            "amount": "100.00"
        }
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = self.session.post(
            f"{self.base_url}/send-payment",
            headers=headers,
            json=payment_data
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])
        print("✓ Invalid card information test passed")

    def test_04_send_payment_invalid_amount(self):
        """Test payment processing with invalid amount."""
        self.login()
        
        payment_data = {
            "uen": "53339185K",
            "cardNumber": "4111111111111111",
            "cvv": "123",
            "expiryDate": "12/25",
            "amount": "0"
        }
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = self.session.post(
            f"{self.base_url}/send-payment",
            headers=headers,
            json=payment_data
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])
        print("✓ Invalid amount test passed")
    
    def test_05_send_payment_no_data(self):
        """Test payment processing with no data."""
        self.login()
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = self.session.post(
            f"{self.base_url}/send-payment",
            headers=headers
        )

        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertFalse(data['success'])
        print("✓ No data test passed")

    def test_06_send_payment_unauthorized(self):
        """Test payment processing with unauthorized access."""

        payment_data = {
            "uen": "53339185K",
            "cardNumber": "4111111111111111",
            "cvv": "123",
            "expiryDate": "12/25",
            "amount": "100.00"
        }
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = self.session.post(
            f"{self.base_url}/send-payment",
            headers=headers,
            json=payment_data
        )
        
        self.assertEqual(response.status_code, 422)
        data = response.json()
        self.assertEqual(data['msg'], 'Not enough segments')
        print("✓ Unauthorized access test passed")

    def test_07_send_payment_user_not_enough_money(self):
        """Test payment processing with user not enough money."""
        self.login()
        
        payment_data = {
            "cust_email":self.consumer_credentials['email'],
            "uen": "53339185K",
            "cardNumber": "7708402154134496",
            "cvv": "222",
            "expiryDate": "12/25",
            "amount": "500.00"
        }
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = self.session.post(
            f"{self.base_url}/send-payment",
            headers=headers,
            json=payment_data
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])
        print("✓ User not enough money test passed")

if __name__ == '__main__':
    unittest.main(verbosity=2)