import base64
from flask import Blueprint, request, jsonify, session, send_file
from werkzeug.exceptions import BadRequest
from app.controller.developersController import DevelopersController
from ..models.developers import Developers
from ..auth.api_key_manager import generate_encrypted_api_key
from cryptography.hazmat.primitives import serialization
from ..auth.TOTP import generate_totp_uri, create_qr_code, generate_secret, encrypt_secret, decrypt_secret, get_totp_token

developerBlueprint = Blueprint('developerBlueprint', __name__)

@developerBlueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        raise BadRequest('No data provided')
    
    secret_key = encrypt_secret(generate_secret())

    ifRegister = DevelopersController().registerDevelopers(data, secret_key)
    
    return jsonify(success=ifRegister)

@developerBlueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        raise BadRequest('No data provided')
    
    ifLogin = DevelopersController().loginDeveloper(data)

    if not ifLogin.get('success'):
        return jsonify(ifLogin)
    
    
    session['email'] = data.get('email')
    session['dev_id'] = ifLogin.get('dev_id')  # Store dev_id for API key functions

    return jsonify(ifLogin)

@developerBlueprint.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

@developerBlueprint.route('/getQRcode', methods=['GET'])
def getQRcode():
    
    # need get secret key from database
    user = DevelopersController().getDeveloperByEmail(session['email'])
    
    totp_uri = generate_totp_uri(session['email'], decrypt_secret(user['dev_secret_key']))
    qr_code = create_qr_code(totp_uri)
    
    return send_file(qr_code, mimetype='image/png')

@developerBlueprint.route('/getSecretKey', methods=['GET'])
def getSecretKey():
    user = DevelopersController().getDeveloperByEmail(session['email'])

    de_secret_key = decrypt_secret(user['dev_secret_key'])

    return jsonify(secret_key=de_secret_key)
    
@developerBlueprint.route('/2fa/verify', methods=['POST'])
def verify2FA():
    data = request.get_json()

    if not data:
        raise BadRequest('No data provided')
    
    user = DevelopersController().getDeveloperByEmail(session['email'])

    server_token = get_totp_token(decrypt_secret(user['dev_secret_key']))

    if server_token == data['code']:
        update2FA = DevelopersController().update2FAbyEmail(session['email'])
        return jsonify(success=update2FA), 200
    else:
        return jsonify(success=False), 401
    
@developerBlueprint.route('/generate-api-key', methods=['POST'])
def generate_api_key():
    dev_id = session.get('dev_id') # Change to 'dev_id' when adjusting for login

    # Check if dev_id exists
    if not dev_id:
        return jsonify({'success': False, 'message': 'Developer ID is required'}), 400

    # Generate encrypted API key
    api_data = generate_encrypted_api_key()

    # Serialize and encode the public key into base64
    public_key_pem = api_data['public_key'].public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Encode ciphertext, IV, and signature in Base64 for storage
    encoded_ciphertext = base64.b64encode(api_data['ciphertext']).decode('utf-8')
    encoded_iv = base64.b64encode(api_data['iv']).decode('utf-8')
    encoded_signature = base64.b64encode(api_data['signature']).decode('utf-8')
    encoded_public_key = base64.b64encode(public_key_pem).decode('utf-8')

    # Save the Base64 encoded API key, iv, and signature in the Developer_API table
    developer = Developers()
    success = developer.save_api_key(dev_id, encoded_iv, encoded_ciphertext, encoded_signature, encoded_public_key)

    if success:
        return jsonify({'success': True, 'message': 'API key generated', 'api_key': encoded_ciphertext, 'iv': encoded_iv, 'signature':encoded_signature}), 200
    else:
        return jsonify({'success': False, 'message': 'Failed to generate API key'}), 500

@developerBlueprint.route('/api-keys', methods=['GET'])
def get_api_keys():
    dev_id = session.get('dev_id')

    if not dev_id:
        return jsonify({'success': False, 'message': 'Developer ID is required'}), 400

    # Fetch API keys for the given developer
    developer = Developers()
    api_keys = developer.get_api_keys(dev_id)

    if api_keys:
        return jsonify({'success': True, 'api_keys': api_keys}), 200
    else:
        return jsonify({'success': True, 'api_keys': []}), 200

@developerBlueprint.route('/api-keys/<api_id>', methods=['DELETE'])
def delete_api_key(api_id):
    success = Developers().delete_api_key(api_id)

    if success:
        return jsonify({'success': True, 'message': 'API key deleted successfully'}), 200
    else:
        return jsonify({'success': False, 'message': 'Failed to delete API key'}), 500