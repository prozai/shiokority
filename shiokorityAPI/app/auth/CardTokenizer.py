import hashlib
import secrets
import re
from datetime import datetime
from typing import Dict, Optional, Tuple

class CardTokenizer:
    def __init__(self):
        # Simulate a secure token vault
        self._token_vault: Dict[str, Dict] = {}
        # Token prefix to identify our tokens
        self._token_prefix = "TKN"
        
    def _validate_card_number(self, card_number: str) -> bool:
        """Validate card number using Luhn algorithm"""
        if not re.match(r'^\d{13,19}$', card_number):
            return False
            
        digits = [int(d) for d in card_number]
        checksum = digits.pop()
        digits.reverse()
        
        doubled = [(d * 2) if i % 2 == 0 else d for i, d in enumerate(digits)]
        doubled = [sum(divmod(d, 10)) if d > 9 else d for d in doubled]
        total = sum(doubled) * 9
        
        return (total % 10) == checksum
    
    def _validate_cvv(self, cvv: str) -> bool:
        """Basic CVV validation"""
        return bool(re.match(r'^\d{3,4}$', cvv))
    
    def _validate_expiry(self, expiry: str) -> bool:
        """Basic expiry date validation (MM/YY format)"""
        if not re.match(r'^\d{2}/\d{2}$', expiry):
            return False
        
        try:
            month, year = map(int, expiry.split('/'))
            return 1 <= month <= 12
        except ValueError:
            return False
        
    def _generate_token(self) -> str:
        """Generate a unique token"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_suffix = secrets.token_hex(6)
        return f"{self._token_prefix}{timestamp}{random_suffix}"
        
    def tokenize(self, card_number: str, cvv: str, expiry: str) -> Optional[str]:
        """
        Tokenize card details including card number, CVV, and expiry date
        Returns None if validation fails
        """
        # Validate all inputs
        if not (self._validate_card_number(card_number) and 
                self._validate_cvv(cvv) and 
                self._validate_expiry(expiry)):
            return None
            
        # Generate token
        token = self._generate_token()
        
        # Store all card details
        self._token_vault[token] = {
            'card_number': card_number,  # In production, this would be encrypted
            'cvv': cvv,                  # In production, this would be encrypted
            'expiry': expiry,
            'last_four': card_number[-4:],
            'created_at': datetime.now().isoformat()
        }
        
        return token
    
    def get_masked_info(self, token: str) -> Optional[Dict]:
        """
        Get masked card information (for merchant/gateway use)
        Only returns last 4 digits and expiry
        """
            
        return {
            'last_four': self._token_vault[token]['last_four'],
            'expiry': self._token_vault[token]['expiry'],
            'created_at': self._token_vault[token]['created_at']
        }
    
    def bank_detokenize(self, token: str) -> Optional[Dict]:
        """
        Bank function to detokenize and get all original card details
        """
        vault_data = self._token_vault[token]
        return {
            'card_number': vault_data['card_number'],
            'cvv': vault_data['cvv'],
            'expiry_date': vault_data['expiry'],
            }