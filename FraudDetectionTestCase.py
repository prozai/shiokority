import unittest
from decimal import Decimal
from datetime import datetime, timedelta
import pymysql
from shiokorityAPI.app.models.fraudDetection import FraudDetection
from shiokorityAPI.app.auth.databaseConnection import getDBConnection
from shiokorityAPI.shiokorityAPI import app

class FraudDetectionTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test configuration."""
        self.fraud_detection = FraudDetection()
        # Test user ID - make sure this exists in your test database
        self.test_user_id = 1  
        self.timestamp = datetime.now()

        # Test credentials
        self.consumer_credentials = {
            "email": "testconsumer@example.com",
            "password": "test123"
        }
        
        # Test transaction data
        self.test_transaction = {
            "amount": "500.00",
            "user_id": self.test_user_id,
            "timestamp": self.timestamp
        }

    def test_01_check_amount_within_limit(self):
        """Test transaction amount within threshold."""
        amount = 500  # Below threshold of 1000
        is_safe, message = self.fraud_detection._check_amount(amount)
        
        self.assertTrue(is_safe)
        self.assertEqual(message, "")
        print("✓ Valid amount test passed")

    def test_02_check_amount_exceeds_limit(self):
        """Test transaction amount exceeding threshold."""
        amount = 1500  # Above threshold of 1000
        is_safe, message = self.fraud_detection._check_amount(amount)
        
        self.assertFalse(is_safe)
        self.assertIn("exceeds the limit", message)
        print("✓ Amount limit exceeded test passed")

    def test_03_check_daily_total_within_limit(self):
        """Test daily total spending within threshold."""
        amount = 500  # This amount plus existing daily total should be under 3000
        is_safe, message = self.fraud_detection._check_daily_total(self.test_user_id, amount)
        
        self.assertTrue(is_safe)
        self.assertEqual(message, "")
        print("✓ Valid daily total test passed")

    def test_04_check_daily_total_exceeds_limit(self):
        """Test daily total spending exceeding threshold."""
        amount = 3500  # This amount should exceed daily limit
        is_safe, message = self.fraud_detection._check_daily_total(self.test_user_id, amount)
        
        self.assertFalse(is_safe)
        self.assertIn("Daily spending limit", message)
        print("✓ Daily total limit exceeded test passed")

    def test_05_check_transaction_frequency_within_limit(self):
        """Test transaction frequency within thresholds."""
        is_safe, message = self.fraud_detection._check_transaction_frequency(self.test_user_id)
        
        self.assertTrue(is_safe)
        self.assertEqual(message, "")
        print("✓ Valid transaction frequency test passed")

    def test_06_check_transaction_frequency_exceeds_hourly(self):
        """Test transaction frequency exceeding hourly threshold."""
        # First, create multiple transactions to exceed hourly limit
        for _ in range(6):  # Create 6 transactions (above 5 limit)
            self._create_test_transaction()
            
        is_safe, message = self.fraud_detection._check_transaction_frequency(self.test_user_id)
        
        self.assertFalse(is_safe)
        self.assertIn("Maximum transactions per hour", message)
        print("✓ Hourly frequency exceeded test passed")

    def test_07_check_sudden_pattern_change_normal(self):
        """Test transaction amount within normal pattern."""
        amount = 500  # Amount close to usual pattern
        is_safe, message = self.fraud_detection._check_sudden_pattern_change(self.test_user_id, amount)
        
        self.assertTrue(is_safe)
        self.assertEqual(message, "")
        print("✓ Normal pattern change test passed")

    def test_08_check_sudden_pattern_change_unusual(self):
        """Test unusual transaction amount pattern."""
        amount = 2000  # Unusual amount compared to pattern
        is_safe, message = self.fraud_detection._check_sudden_pattern_change(self.test_user_id, amount)
        
        self.assertFalse(is_safe)
        self.assertIn("Unusual transaction amount", message)
        print("✓ Unusual pattern change test passed")

    def test_09_check_rapid_transactions_normal(self):
        """Test normal transaction timing."""
        is_safe, message = self.fraud_detection._check_rapid_transactions(
            self.test_user_id, 
            self.timestamp
        )
        
        self.assertTrue(is_safe)
        self.assertEqual(message, "")
        print("✓ Normal transaction timing test passed")

    def test_10_check_rapid_transactions_suspicious(self):
        """Test suspicious rapid transactions."""
        # Create multiple transactions within 5 minutes
        for _ in range(4):  # Create 4 transactions (above 3 limit)
            self._create_test_transaction()
            
        is_safe, message = self.fraud_detection._check_rapid_transactions(
            self.test_user_id, 
            self.timestamp
        )
        
        self.assertFalse(is_safe)
        self.assertIn("Multiple rapid transactions", message)
        print("✓ Rapid transactions test passed")

    def test_11_detect_transaction_fraud_safe(self):
        """Test complete fraud detection with safe transaction."""
        is_safe, message = self.fraud_detection.detect_transaction_fraud(
            self.test_user_id,
            "500.00",
            self.timestamp
        )
        
        self.assertTrue(is_safe)
        self.assertEqual(message, "Transaction authorized")
        print("✓ Safe transaction detection test passed")

    def test_12_admin_fraud_detection_success(self):
        """Test admin fraud detection system with successful login."""
        is_locked, message = self.fraud_detection.adminFraudDetection(
            "admin@test.com",  # Use a valid admin email
            True  # Successful login
        )
        
        self.assertFalse(is_locked)
        self.assertEqual(message, "Authentication successful")
        print("✓ Admin successful login test passed")

    def test_13_admin_fraud_detection_failure(self):
        """Test admin fraud detection system with failed login attempts."""
        admin_email = "admin@test.com"  # Use a valid admin email
        
        # Simulate multiple failed login attempts
        for _ in range(5):
            self.fraud_detection.adminFraudDetection(admin_email, False)
            
        is_locked, message = self.fraud_detection.adminFraudDetection(admin_email, False)
        
        self.assertTrue(is_locked)
        self.assertIn("Account locked", message)
        print("✓ Admin account lockout test passed")


if __name__ == '__main__':
    unittest.main(verbosity=2)