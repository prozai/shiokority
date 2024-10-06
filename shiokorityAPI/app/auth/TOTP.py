import os
import base64
import time
import struct
import hmac
import qrcode
import io
from cryptography.fernet import Fernet
import hashlib
from config import config

ENCRYPTION_KEY = config['default'].ENCRYPTION_KEY
cipher_suite = Fernet(ENCRYPTION_KEY) 

def generate_secret():
    return base64.b32encode(os.urandom(10)).decode('utf-8')

def get_totp_token(secret):
    x = int(time.time() // 30)
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", x)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[19] & 15
    h = struct.unpack('>I', h[o:o+4])[0] & 0x7fffffff
    return '{:06d}'.format(h % 1000000)

def generate_totp_uri(username, secret, issuer="YourApp"):
    return f"otpauth://totp/{issuer}:{username}?secret={secret}&issuer={issuer}"

def create_qr_code(uri):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io

def encrypt_secret(secret):
    return cipher_suite.encrypt(secret.encode()).decode()

def decrypt_secret(encrypted_secret):
    return cipher_suite.decrypt(encrypted_secret.encode()).decode()