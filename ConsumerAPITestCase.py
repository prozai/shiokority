import unittest
import requests
import json
from unittest.mock import patch

class ConsumerAPITestCase(unittest.TestCase):
    def setUp(self):
        """Set up test configuration."""
        self.base_url = "https://api.shiokority.online/consumer"
        self.session = requests.Session()
        self.consumer_credentials = {
            "email": "usertest@example.com",  # Replace with test consumer credentials
            "password": "123"
        }
        # Store session token after login
        self.session_token = None
        
    def login(self):
        """Helper method to log in and get session token."""
        response = self.session.post(
            f"{self.base_url}/login-consumer",
            json=self.consumer_credentials
        )
        if response.status_code == 200:
            # Store session cookies for subsequent requests
            self.session_token = self.session.cookies.get_dict()
            return True
        return False

    def test_01_register_consumer(self):
        """Test consumer registration endpoint."""
        test_consumer = {
            "cust_email": "newconsumer@example.com",
            "cust_pass": "test123",
            "cust_fname": "Test",
            "cust_lname": "Consumer",
            "cust_phone": "1234567890",
            "cust_address": "123 Test St"
        }
        
        response = self.session.post(
            f"{self.base_url}/register-consumer",
            json=test_consumer
        )
        
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertTrue(data['success'])
        print("✓ Consumer registration test passed")

    def test_02_register_consumer_duplicate_email(self):
        """Test consumer registration with duplicate email."""
        test_consumer = {
            "cust_email": "test@test.com",  # Existing email
            "cust_pass": "test123",
            "cust_fname": "Test",
            "cust_lname": "Consumer",
            "cust_phone": "1234567890",
            "cust_address": "123 Test St"
        }
        
        response = self.session.post(
            f"{self.base_url}/register-consumer",
            json=test_consumer
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])
        print("✓ Duplicate email registration test passed")

    def test_03_consumer_login_valid(self):
        """Test consumer login endpoint with valid credentials."""
        response = self.session.post(
            f"{self.base_url}/login-consumer",
            json=self.consumer_credentials
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        print("✓ Consumer login test passed")

    def test_04_consumer_login_invalid(self):
        """Test consumer login with invalid credentials."""
        invalid_credentials = {
            "email": "wrong@consumer.com",
            "password": "wrongpass"
        }
        
        response = self.session.post(
            f"{self.base_url}/login-consumer",
            json=invalid_credentials
        )
        
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertFalse(data['success'])
        print("✓ Invalid login test passed")

    def test_05_view_profile(self):
        """Test viewing consumer profile endpoint."""
        self.login()  # Ensure we're logged in
        
        response = self.session.get(f"{self.base_url}/profile-consumer")
        
        self.assertEqual(response.status_code, 200)
        profile = response.json()
        self.assertIsInstance(profile, dict)
        print("✓ View profile test passed")

    def test_06_view_profile_unauthorized(self):
        """Test viewing profile without login."""
        response = self.session.get(f"{self.base_url}/profile-consumer")
        
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertFalse(data['success'])
        print("✓ Unauthorized profile access test passed")

    def test_07_send_payment_valid(self):
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
        
        response = self.session.post(
            f"{self.base_url}/send-payment",
            json=payment_data
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        print("✓ Valid payment test passed")

    def test_08_send_payment_invalid_uen(self):
        """Test payment processing with invalid UEN."""
        self.login()
        
        payment_data = {
            "uen": "invalid-uen",
            "cardNumber": "4111111111111111",
            "cvv": "123",
            "expiryDate": "12/25",
            "amount": "100.00"
        }
        
        response = self.session.post(
            f"{self.base_url}/send-payment",
            json=payment_data
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])
        print("✓ Invalid UEN payment test passed")

    def test_09_send_payment_invalid_card_information(self):
        """Test payment processing with invalid card information."""
        self.login()
        
        payment_data = {
            "uen": "53339185K",
            "cardNumber": "1111111111111111",
            "cvv": "123",
            "expiryDate": "12/25",
            "amount": "100.00"
        }
        
        response = self.session.post(
            f"{self.base_url}/send-payment",
            json=payment_data
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])
        print("✓ Invalid UEN payment test passed")

    def test_09_view_merchants(self):
        """Test viewing merchant list endpoint."""
        self.login()
        
        response = self.session.get(f"{self.base_url}/view-merchant")
        
        self.assertEqual(response.status_code, 200)
        merchants = response.json()
        self.assertIsInstance(merchants, list)
        print("✓ View merchants test passed")

    def test_10_consumer_logout(self):
        """Test consumer logout endpoint."""
        self.login()
        
        response = self.session.post(f"{self.base_url}/logout-consumer")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Logout successful')
        print("✓ Consumer logout test passed")

if __name__ == '__main__':
    unittest.main(verbosity=2)