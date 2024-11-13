import unittest
import base64
import os
import time
from cryptography.fernet import Fernet
from unittest.mock import patch, MagicMock
import io
from shiokorityAPI.app.auth.api_key_manager import (generate_encrypted_api_key, decrypt_and_verify_api_key)
from shiokorityAPI.app.auth.TOTP import (generate_secret, get_totp_token, generate_totp_uri, create_qr_code, encrypt_secret, decrypt_secret)
from shiokorityAPI.app.auth.encryption_utils import aes_encrypt, aes_decrypt
from shiokorityAPI.app.auth.CardTokenizer import CardTokenizer

class SecurityTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        # Encryption setup
        self.test_key = Fernet.generate_key()
        self.test_config = {'default': MagicMock(ENCRYPTION_KEY=self.test_key)}
        self.test_secret = "ABCDEFGHIJKLMNOP"
        self.test_username = "testuser@example.com"
        self.aes_key = os.urandom(32)  # 256-bit key for AES

        # Card Tokenizer setup
        self.tokenizer = CardTokenizer()
        self.valid_card = "4532015112830366"  # Valid number using Luhn algorithm
        self.valid_cvv = "123"
        self.valid_expiry = "12/25"

    # === ENCRYPTION AND TOTP TESTS ===

    def test_01_generate_secret(self):
        """Test secret generation."""
        secret = generate_secret()
        
        self.assertIsNotNone(secret)
        self.assertEqual(len(base64.b32decode(secret)), 10)
        # Verify it's base32 encoded
        self.assertTrue(all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567=' for c in secret))
        print("✓ Generate secret test passed")

    def test_02_get_totp_token(self):
        """Test TOTP token generation."""
        token = get_totp_token(self.test_secret)
        
        self.assertIsNotNone(token)
        self.assertEqual(len(token), 6)
        self.assertTrue(token.isdigit())
        print("✓ TOTP token generation test passed")

    def test_03_get_totp_token_invalid(self):
        """Test TOTP token generation with invalid secret."""
        token = get_totp_token(None)
        self.assertIsNone(token)
        
        token = get_totp_token("invalid_secret")
        self.assertIsNone(token)
        print("✓ Invalid TOTP token test passed")

    def test_04_generate_totp_uri(self):
        """Test TOTP URI generation."""
        uri = generate_totp_uri(self.test_username, self.test_secret)
        
        self.assertIsNotNone(uri)
        self.assertIn(self.test_username, uri)
        self.assertIn(self.test_secret, uri)
        self.assertIn("Shiokority", uri)
        self.assertTrue(uri.startswith("otpauth://totp/"))
        print("✓ TOTP URI generation test passed")

    def test_05_generate_totp_uri_invalid(self):
        """Test TOTP URI generation with invalid inputs."""
        uri = generate_totp_uri(None, self.test_secret)
        self.assertIsNone(uri)
        
        uri = generate_totp_uri(self.test_username, None)
        self.assertIsNone(uri)
        print("✓ Invalid TOTP URI test passed")

    def test_06_create_qr_code(self):
        """Test QR code generation."""
        uri = generate_totp_uri(self.test_username, self.test_secret)
        qr_code = create_qr_code(uri)
        
        self.assertIsNotNone(qr_code)
        self.assertTrue(isinstance(qr_code, io.BytesIO))
        qr_code.seek(0)
        self.assertTrue(qr_code.read().startswith(b'\x89PNG'))
        print("✓ QR code generation test passed")

    def test_07_encrypt_decrypt_secret(self):
        """Test secret encryption and decryption."""
        encrypted = encrypt_secret(self.test_secret)
        self.assertIsNotNone(encrypted)
        self.assertNotEqual(encrypted, self.test_secret)
        
        decrypted = decrypt_secret(encrypted)
        self.assertEqual(decrypted, self.test_secret)
        print("✓ Secret encryption/decryption test passed")

    def test_08_aes_encryption_decryption(self):
        """Test AES encryption and decryption."""
        test_data = "Test message for AES encryption"
        
        iv, ciphertext = aes_encrypt(test_data, self.aes_key)
        self.assertIsNotNone(iv)
        self.assertEqual(len(iv), 16)
        self.assertIsNotNone(ciphertext)
        
        decrypted = aes_decrypt(iv, ciphertext, self.aes_key)
        self.assertEqual(decrypted, test_data)
        print("✓ AES encryption/decryption test passed")

    def test_09_totp_time_window(self):
        """Test TOTP token time window."""
        token1 = get_totp_token(self.test_secret)
        time.sleep(1)
        token2 = get_totp_token(self.test_secret)
        
        self.assertEqual(token1, token2)
        print("✓ TOTP time window test passed")

    # === CARD TOKENIZER TESTS ===

    def test_10_card_number_validation(self):
        """Test credit card number validation."""
        valid_cards = [
            "4532015112830366",  # Visa
            "5425233430109903",  # Mastercard
            "374245455400126",   # American Express
            "6011000991300009"   # Discover
        ]
        for card in valid_cards:
            self.assertTrue(self.tokenizer._validate_card_number(card))
            
        invalid_cards = [
            "4532015112830367",  # Failed Luhn check
            "123",               # Too short
            "12345678901234567890",  # Too long
            "abcd4567890123456",     # Non-numeric
            ""                       # Empty
        ]
        for card in invalid_cards:
            self.assertFalse(self.tokenizer._validate_card_number(card))
        print("✓ Card number validation test passed")

    def test_11_cvv_validation(self):
        """Test CVV validation."""
        valid_cvvs = ["123", "1234"]
        for cvv in valid_cvvs:
            self.assertTrue(self.tokenizer._validate_cvv(cvv))
            
        invalid_cvvs = ["12", "12345", "abc", "", "12a"]
        for cvv in invalid_cvvs:
            self.assertFalse(self.tokenizer._validate_cvv(cvv))
        print("✓ CVV validation test passed")

    def test_12_expiry_validation(self):
        """Test expiry date validation."""
        valid_expiry = ["01/25", "12/99"]
        for expiry in valid_expiry:
            self.assertTrue(self.tokenizer._validate_expiry(expiry))
            
        invalid_expiry = [
            "13/25",  # Invalid month
            "00/25",  # Invalid month
            "1/25",   # Wrong format
            "01/2025",  # Wrong format
            "01-25",    # Wrong separator
            "ab/cd",    # Non-numeric
            ""          # Empty
        ]
        for expiry in invalid_expiry:
            self.assertFalse(self.tokenizer._validate_expiry(expiry))
        print("✓ Expiry date validation test passed")

    def test_13_token_generation_and_storage(self):
        """Test token generation and storage."""
        token = self.tokenizer.tokenize(
            self.valid_card,
            self.valid_cvv,
            self.valid_expiry
        )
        
        self.assertIsNotNone(token)
        self.assertTrue(token.startswith("TKN"))
        
        vault_data = self.tokenizer._token_vault[token]
        self.assertEqual(vault_data['card_number'], self.valid_card)
        self.assertEqual(vault_data['cvv'], self.valid_cvv)
        self.assertEqual(vault_data['expiry'], self.valid_expiry)
        print("✓ Token generation and storage test passed")

    def test_14_masked_info_retrieval(self):
        """Test retrieving masked card information."""
        token = self.tokenizer.tokenize(
            self.valid_card,
            self.valid_cvv,
            self.valid_expiry
        )
        
        masked_info = self.tokenizer.get_masked_info(token)
        
        self.assertEqual(masked_info['last_four'], self.valid_card[-4:])
        self.assertEqual(masked_info['expiry'], self.valid_expiry)
        self.assertTrue('created_at' in masked_info)
        self.assertFalse('card_number' in masked_info)
        self.assertFalse('cvv' in masked_info)
        print("✓ Masked info retrieval test passed")


    def test_15_token_security(self):
        """Test token security features."""
        # Test uniqueness
        tokens = set()
        for _ in range(10):
            token = self.tokenizer.tokenize(
                self.valid_card,
                self.valid_cvv,
                self.valid_expiry
            )
            self.assertNotIn(token, tokens)
            tokens.add(token)
            
        # Test invalid token access
        invalid_token = "TKN123456789"
        with self.assertRaises(KeyError):
            self.tokenizer.get_masked_info(invalid_token)
        with self.assertRaises(KeyError):
            self.tokenizer.bank_detokenize(invalid_token)
        print("✓ Token security test passed")

if __name__ == '__main__':
    unittest.main(verbosity=2)