import unittest
import requests
import json
from unittest.mock import patch

class AdminAPITestCase(unittest.TestCase):
    def setUp(self):
        """Set up test configuration."""
        self.base_url = "https://api.shiokority.online/admin"
        self.session = requests.Session()
        self.admin_credentials = {
            "email": "admin1@example.com",  # Replace with test admin credentials
            "password": "123"
        }
        # Store session token after login
        self.session_token = None
        
    def login(self):
        """Helper method to log in and get session token."""
        response = self.session.post(
            f"{self.base_url}/auth/login",
            json=self.admin_credentials
        )
        if response.status_code == 200:
            # Store session cookies for subsequent requests
            self.session_token = self.session.cookies.get_dict()
            return True
        return False

    def test_01_admin_login(self):
        """Test admin login endpoint."""
        response = self.session.post(
            f"{self.base_url}/auth/login",
            json=self.admin_credentials
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        print("✓ Admin login test passed")

    def test_02_admin_login_invalid(self):
        """Test admin login with invalid credentials."""
        invalid_credentials = {
            "email": "wrong@admin.com",
            "password": "wrongpass"
        }
        
        response = self.session.post(
            f"{self.base_url}/auth/login",
            json=invalid_credentials
        )
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertFalse(data['success'])
        print("✓ Invalid login test passed")


    def test_03_create_merchant_valid_email(self):
        """Test merchant creation with valid email endpoint."""
        self.login()  # Ensure we're logged in
        
        test_merchant = {
            "name": "Test Merchant",
            "email": "test_merchant@example.com",
            "address": "Test Address",
            "phone": "1234567890",
            "uen": "test-uen-123"
            # Add other required merchant fields
        }

        response = self.session.post(
            f"{self.base_url}/create-merchant",
            json=test_merchant
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        print("✓ Create merchant test passed")

    def test_04_create_merchant_repeated_email(self):
        """Test merchant creation not valid email endpoint."""
        self.login()  # Ensure we're logged in
        
        test_merchant = {
            "name": "Test Merchant",
            "email": "test1@test.com",
            "address": "Test Address",
            "phone": "1234567890",
            "uen": "test-uen-123"
            # Add other required merchant fields
        }

        response = self.session.post(
            f"{self.base_url}/create-merchant",
            json=test_merchant
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])
        print("✓  test passed") 

    def test_05_view_merchants(self):
        """Test viewing merchant list endpoint."""
        self.login()  # Ensure we're logged in
        
        response = self.session.get(f"{self.base_url}/view-merchant")
        
        self.assertEqual(response.status_code, 200)
        merchants = response.json()
        self.assertIsInstance(merchants, list)
        print("✓ View merchants test passed")

    def test_06_get_specific_merchant(self):
        """Test getting specific merchant endpoint."""
        self.login()
        merchant_id = "1"  # Replace with valid merchant ID
        
        response = self.session.get(f"{self.base_url}/merchants/{merchant_id}")
        
        self.assertEqual(response.status_code, 200)
        merchant = response.json()
        self.assertIsInstance(merchant, dict)
        print("✓ Get specific merchant test passed")

    def test_07_update_merchant(self):
        """Test merchant update endpoint."""
        self.login()
        merchant_id = "1"  # Replace with valid merchant ID
        
        update_data = {
            "merch_name": "Updated Merchant Name",
            "merch_email": "updated@example.com",
            "merch_address": "Updated Address",
            "merch_phone": "9876543210",
            "uen": "test-uen-123"
        }
        
        response = self.session.put(
            f"{self.base_url}/merchants/{merchant_id}",
            json=update_data
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        print("✓ Update merchant test passed")

    def test_08_fail_update_merchant(self):
        """Test merchant update endpoint."""
        self.login()
        merchant_id = "1"

        update_data = {
            "name": "Updated Merchant Name",
            "email": "merchant1@example.com", # existing email address
            "address": "Updated Address",
            "phone": "9876543210",
            "uen": "test-uen-123"
        }

        response = self.session.put(
            f"{self.base_url}/merchants/{merchant_id}",
            json=update_data
        )

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])


    def test_09_suspend_merchant(self):
        """Test merchant suspension endpoint."""
        self.login()
        merchant_id = "1"  # Replace with valid merchant ID
        
        suspend_data = {
            "status": "0"
        }
        
        response = self.session.put(
            f"{self.base_url}/suspend-merchants/{merchant_id}",
            json=suspend_data
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        print("✓ Suspend merchant test passed")

    def test_10_get_audit_trail_logs(self):
        """Test audit trail logs endpoint."""
        self.login()
        
        response = self.session.get(f"{self.base_url}/getAllAuditTrailLogs")
        
        self.assertEqual(response.status_code, 200)
        logs = response.json()
        self.assertIsInstance(logs, list)
        print("✓ Get audit trail logs test passed")

    def test_11_get_specific_audit_log(self):
        """Test getting specific audit log endpoint."""
        self.login()
        audit_id = "1"  # Replace with valid audit ID
        
        response = self.session.get(f"{self.base_url}/getAuditTrailById/{audit_id}")
        
        self.assertEqual(response.status_code, 200)
        log = response.json()
        self.assertIsInstance(log, dict)
        print("✓ Get specific audit log test passed")

    def test_10_unauthorized_access(self):
        """Test unauthorized access to protected endpoints."""
        # Try accessing protected endpoint without login
        response = self.session.get(f"{self.base_url}/view-merchant")
        
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertFalse(data['success'])
        print("✓ Unauthorized access test passed")

    def test_11_admin_logout(self):
        """Test admin logout endpoint."""
        self.login()
        
        response = self.session.post(f"{self.base_url}/auth/logout")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['message'], 'Logout successful')
        print("✓ Admin logout test passed")

if __name__ == '__main__':
    unittest.main(verbosity=2)