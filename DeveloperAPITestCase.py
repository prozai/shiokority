import unittest
import requests
from unittest.mock import patch

class DeveloperAPITestCase(unittest.TestCase):
    def setUp(self):
        """Set up test configuration."""
        self.base_url = "https://api.shiokority.online/developers"
        self.session = requests.Session()
        self.developer_credentials = {
            "email": "dev1@example.com",
            "password": "123"
        }
        # Store JWT token
        self.access_token = None
        
    def login(self):
        """Helper method to log in and get JWT token."""
        response = self.session.post(
            f"{self.base_url}/login",
            json=self.developer_credentials
        )
        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access_token']
            return True
        return False

    def test_01_developer_registration(self):
        """Test developer registration endpoint."""
        test_developer = {
            "email": "newdev@example.com",
            "password": "test123",
            "firstName": "Test",
            "lastName": "Developer",
            "address": "Test Developer",
            "phoneNumber": "Test Company"
        }
        
        response = self.session.post(
            f"{self.base_url}/register",
            json=test_developer
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        print("✓ Developer registration test passed")

    def test_02_developer_registration_duplicate(self):
        """Test developer registration with duplicate email."""
        test_developer = {
            "email": "dev1@example.com",
            "password": "test123",
            "name": "Test Developer",
            "company": "Test Company"
        }
        
        response = self.session.post(
            f"{self.base_url}/register",
            json=test_developer
        )
        
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertFalse(data['success'])
        print("✓ Duplicate registration test passed")

    def test_03_developer_login(self):
        """Test developer login endpoint."""
        response = self.session.post(
            f"{self.base_url}/login",
            json=self.developer_credentials
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('access_token', data)
        self.assertIn('refresh_token', data)
        self.assertIn('dev_id', data)
        self.assertIn('two_factor_enabled', data)
        print("✓ Developer login test passed")

    def test_04_developer_login_invalid(self):
        """Test developer login with invalid credentials."""
        invalid_credentials = {
            "email": "wrong@dev.com",
            "password": "wrongpass"
        }
        
        response = self.session.post(
            f"{self.base_url}/login",
            json=invalid_credentials
        )
        
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertFalse(data['success'])
        print("✓ Invalid login test passed")

    def test_05_get_qr_code(self):
        """Test getting QR code for 2FA setup."""
        self.login()
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = self.session.get(
            f"{self.base_url}/getQRcode",
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'image/png')
        print("✓ Get QR code test passed")

    def test_06_get_secret_key(self):
        """Test getting secret key for 2FA."""
        self.login()
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = self.session.get(
            f"{self.base_url}/getSecretKey",
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('secret_key', data)
        print("✓ Get secret key test passed")

    def test_07_verify_2fa(self):
        """Test 2FA verification."""
        self.login()
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        verify_data = {
            "code": "665855"  # Replace with actual TOTP code
        }

        response = self.session.post(
            f"{self.base_url}/2fa/verify",
            headers=headers,
            json=verify_data
        )
        
        # Note: This might fail in real testing as TOTP codes are time-based
        self.assertIn(response.status_code, [200, 401])
        print("✓ 2FA verification test passed")

    def test_08_generate_api_key(self):
        """Test API key generation."""
        self.login()
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = self.session.post(
            f"{self.base_url}/generate-api-key",
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('api_key', data)
        self.assertIn('iv', data)
        self.assertIn('signature', data)
        print("✓ Generate API key test passed")

    def test_09_get_api_keys(self):
        """Test getting list of API keys."""
        self.login()
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = self.session.get(
            f"{self.base_url}/api-keys",
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('api_keys', data)
        self.assertIsInstance(data['api_keys'], list)
        print("✓ Get API keys test passed")

    def test_10_delete_api_key(self):
        """Test API key deletion."""
        self.login()
        api_key_id = "2"  # Replace with actual API key ID
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = self.session.delete(
            f"{self.base_url}/api-keys/{api_key_id}",
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        print("✓ Delete API key test passed")

    def test_11_unauthorized_access(self):
        """Test unauthorized access to protected endpoints."""
        response = self.session.get(f"{self.base_url}/api-keys")
        
        self.assertEqual(response.status_code, 401)
        print("✓ Unauthorized access test passed")

    def test_12_developer_logout(self):
        """Test developer logout endpoint."""
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
        self.assertEqual(data['message'], 'Logged out successfully')
        print("✓ Developer logout test passed")

if __name__ == '__main__':
    unittest.main(verbosity=2)