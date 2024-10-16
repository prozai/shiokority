import os
from shiokorityAPI.app.auth.encryption_utils import aes_encrypt, aes_decrypt
from shiokorityAPI.app.auth.rsa_utils import generate_rsa_keys, sign_data, verify_signature

# Encrypt data, sign AES key, verify and decrypt workflow
def generate_encrypted_api_key():
    # Example: data is the API key you want to encrypt
    api_key = os.urandom(16).hex()  # Random 16-byte API key, converted to hex for readability

    # Generate RSA key pair
    private_key, public_key = generate_rsa_keys()

    # Step 1: AES encryption
    aes_key = os.urandom(32)  # AES-256 key
    iv, ciphertext = aes_encrypt(api_key, aes_key)

    # Step 2: RSA signature of AES key
    signature = sign_data(private_key, aes_key)

    # Return encrypted API key and the signature (along with iv)
    return {
        'iv': iv,
        'ciphertext': ciphertext,
        'signature': signature,
        'public_key': public_key
    }

# Decrypt and verify
def decrypt_and_verify_api_key(iv, ciphertext, aes_key, signature, public_key):
    # Step 3: Verify the signature
    try:
        verify_signature(public_key, aes_key, signature)
    except:
        raise ValueError("Invalid signature")

    # Step 4: Decrypt the API key
    decrypted_key = aes_decrypt(iv, ciphertext, aes_key)
    return decrypted_key