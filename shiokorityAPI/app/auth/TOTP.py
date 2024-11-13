import os
import base64
import time
import struct
import hmac
import qrcode
import io
from cryptography.fernet import Fernet, InvalidToken
import hashlib
from config import config

ENCRYPTION_KEY = config['default'].ENCRYPTION_KEY
cipher_suite = Fernet(ENCRYPTION_KEY) 

def generate_secret():
    try:
        return base64.b32encode(os.urandom(10)).decode('utf-8')
    except Exception as e:
        print(f"Error generating secret: {str(e)}")
        return None

def get_totp_token(secret):
    try:
        if not secret:
            raise ValueError("Invalid secret key")
            
        x = int(time.time() // 30)
        key = base64.b32decode(secret, True)
        msg = struct.pack(">Q", x)
        h = hmac.new(key, msg, hashlib.sha1).digest()
        o = h[19] & 15
        h = struct.unpack('>I', h[o:o+4])[0] & 0x7fffffff
        return '{:06d}'.format(h % 1000000)
    except Exception as e:
        print(f"Error generating TOTP token: {str(e)}")
        return None

def generate_totp_uri(username, secret, issuer="Shiokority"):
    try:
        if not username or not secret:
            raise ValueError("Username and secret are required")
        return f"otpauth://totp/{issuer}:{username}?secret={secret}&issuer={issuer}"
    except Exception as e:
        print(f"Error generating TOTP URI: {str(e)}")
        return None

def create_qr_code(uri):
    try:
        if not uri:
            raise ValueError("Invalid URI")
            
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uri)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        return img_io
    except Exception as e:
        print(f"Error creating QR code: {str(e)}")
        return None

def encrypt_secret(secret):
    try:
        if not isinstance(secret, str):
            raise ValueError("Secret must be a string")
        return cipher_suite.encrypt(secret.encode()).decode()
    except Exception as e:
        print(f"Encryption error: {str(e)}")
        return None

def decrypt_secret(encrypted_secret):
    try:
        if not encrypted_secret:
            raise ValueError("No encrypted secret provided")
        return cipher_suite.decrypt(encrypted_secret.encode()).decode()
    except InvalidToken:
        print("Invalid token - encryption key might have changed")
        return None
    except Exception as e:
        print(f"Decryption error: {str(e)}")
        return None