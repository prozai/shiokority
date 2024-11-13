import unittest
import requests
import json
from unittest.mock import patch

class MerchantAPITestCase(unittest.TestCase):
    def setUp(self):
        """Set up test configuration."""
        self.base_url = "https://api.shiokority.online/merchant"
        self.session = requests.Session()
        self.merchant_credentials = {
            "email": "merchtest2@example.com",
            "password": "123"
        }
        # Store JWT token
        self.access_token = None
        
    def login(self):
        """Helper method to log in and get JWT token."""
        response = self.session.post(
            f"{self.base_url}/login",
            json=self.merchant_credentials
        )
        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access_token']
            return True
        return False

    def test_01_merchant_registration(self):
        """Test merchant registration endpoint."""
        test_merchant = {
            "merch_email": "new_merchant@example.com",
            "merch_pass": "123",
            "merch_name": "Test",
            "merch_phone": "1234567890",
            "merch_address": "Test Address",
            "uen": "test23456"
        }
        
        response = self.session.post(
            f"{self.base_url}/register-merchant",
            json=test_merchant
        )
        
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertTrue(data['success'])
        print("✓ Merchant registration test passed")

    def test_02_merchant_registration_invalid(self):
        """Test merchant registration with repeated email."""
        invalid_merchant = {
            "merch_email": "new_merchant@example.com", # Same email as registration test
            "merch_pass": "123",
            "merch_name": "Test",
            "merch_phone": "1234567890",
            "merch_address": "Test Address",
            "uen": "1234567890"
        }
        
        response = self.session.post(
            f"{self.base_url}/register-merchant",
            json=invalid_merchant
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])
        print("✓ Invalid registration test passed")

    def test_03_merchant_login(self):
        """Test merchant login endpoint."""
        response = self.session.post(
            f"{self.base_url}/login",
            json=self.merchant_credentials
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('merchant', data)
        self.assertIn('merch_id', data['merchant'])
        self.assertIn('access_token', data)
        self.assertIn('refresh_token', data)
        print("✓ Merchant login test passed")

    def test_04_merchant_login_invalid(self):
        """Test merchant login with invalid credentials."""
        invalid_credentials = {
            "email": "wrong@merchant.com",
            "password": "wrongpass"
        }
        
        response = self.session.post(
            f"{self.base_url}/login",
            json=invalid_credentials
        )
        
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertFalse(data['success'])
        print("✓ Invalid login test passed")

    def test_05_get_merchant_profile(self):
        """Test getting merchant profile endpoint."""
        self.login()
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        response = self.session.get(
            f"{self.base_url}/profile",
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        merchant = response.json()
        self.assertIsInstance(merchant, dict)
        print("✓ Get merchant profile test passed")

    def test_06_get_profile_unauthorized(self):
        """Test getting profile without login."""
        response = self.session.get(f"{self.base_url}/profile")
        
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertEqual(data['msg'], 'Missing Authorization Header')
        print("✓ Unauthorized profile access test passed")

    def test_07_view_transaction_history(self):
        """Test viewing transaction history endpoint."""
        self.login()
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        response = self.session.get(
            f"{self.base_url}/viewTransactionHistory",
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        transactions = response.json()
        self.assertIsInstance(transactions, list)
        print("✓ View transaction history test passed")

    def test_08_view_transaction_history_unauthorized(self):
        """Test viewing transaction history without login."""
        response = self.session.get(f"{self.base_url}/viewTransactionHistory")
        
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertEqual(data['msg'], 'Missing Authorization Header')
        print("✓ Unauthorized transaction history access test passed")

    def test_09_merchant_logout(self):
        """Test merchant logout endpoint."""
        self.login()
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        response = self.session.post(
            f"{self.base_url}/logout",
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Logged out successfully')
        print("✓ Merchant logout test passed")

if __name__ == '__main__':
    unittest.main(verbosity=2)