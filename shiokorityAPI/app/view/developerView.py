import base64
from flask import Blueprint, request, jsonify, session, send_file
from werkzeug.exceptions import BadRequest
from app.controller.developersController import DevelopersController
from ..auth.api_key_manager import generate_encrypted_api_key
from cryptography.hazmat.primitives import serialization
from ..auth.TOTP import generate_totp_uri, create_qr_code, generate_secret, encrypt_secret, decrypt_secret, get_totp_token
from ..controller.auditTrailController import AuditTrailController  # Import AuditTrailController
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required, get_jwt_identity, get_jwt

developerBlueprint = Blueprint('developerBlueprint', __name__)
audit_trail_controller = AuditTrailController()

@developerBlueprint.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            audit_trail_controller.log_action('POST', '/developers/register', "No data provided")
            raise BadRequest('No data provided')
        
        secret_key = encrypt_secret(generate_secret())
        ifRegister = DevelopersController().registerDevelopers(data, secret_key)
        
        audit_trail_controller.log_action('POST', '/developers/register', f"Developer registration {'successful' if ifRegister else 'failed'}")
        return jsonify(success=ifRegister)
    except Exception as e:
        audit_trail_controller.log_action('POST', '/developers/register', f"Unexpected error: {e}")
        print(f"Error registering developer: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred during registration'}), 500

@developerBlueprint.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            audit_trail_controller.log_action('POST', '/developers/login', "No data provided")
            raise BadRequest('No data provided')
        
        ifLogin = DevelopersController().loginDeveloper(data)

        if not ifLogin.get('success'):
            audit_trail_controller.log_action('POST', '/developers/login', f"Failed login attempt for email: {data.get('email')}")
            return jsonify(ifLogin)
        
        access_token = create_access_token(
                identity=data.get('email'),
                additional_claims={'dev_id':ifLogin['dev_id']})

        audit_trail_controller.log_action('POST', '/developers/login', f"Developer {data.get('email')} logged in successfully")
        return jsonify({
            'success': ifLogin['success'],
            "dev_id": ifLogin["dev_id"],
            "two_factor_enabled" : ifLogin['two_factor_enabled'],
            'access_token': access_token,
            'refresh_token': create_refresh_token(identity=data.get('email'))            
        }), 200

    except Exception as e:
        audit_trail_controller.log_action('POST', '/developers/login', f"Unexpected error: {e}")
        print(f"Error logging in developer: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred during login'}), 500


@developerBlueprint.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        current_user = get_jwt_identity()
        validateUser = DevelopersController().validateTokenEmail(current_user)

        if not validateUser:
            audit_trail_controller.log_action('POST', '/developers/logout', "Unauthorized access attempt")
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 401
        
        session.clear()
        audit_trail_controller.log_action('POST', '/developers/logout', f"Developer {current_user} logged out")
        return jsonify({"message": "Logged out successfully"}), 200
    except Exception as e:
        audit_trail_controller.log_action('POST', '/developers/logout', f"Unexpected error: {e}")
        print(f"Error logging out developer: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred during logout'}), 500

@developerBlueprint.route('/getQRcode', methods=['GET'])
@jwt_required()
def getQRcode():
    try:
        current_user = get_jwt_identity()
        validateUser = DevelopersController().validateTokenEmail(current_user)

        if not validateUser:    
            audit_trail_controller.log_action('GET', '/developers/getQRcode', "Unauthorized access attempt")
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 401

        user = DevelopersController().getDeveloperByEmail(current_user)
        totp_uri = generate_totp_uri(current_user, decrypt_secret(user['dev_secret_key']))
        qr_code = create_qr_code(totp_uri)
        audit_trail_controller.log_action('GET', '/developers/getQRcode', f"QR code generated for developer {current_user}")
        return send_file(qr_code, mimetype='image/png')
    except Exception as e:
        audit_trail_controller.log_action('GET', '/developers/getQRcode', f"Unexpected error: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred while generating QR code'}), 500

@developerBlueprint.route('/getSecretKey', methods=['GET'])
@jwt_required()
def getSecretKey():
    try:

        current_user = get_jwt_identity()
        validateUser = DevelopersController().validateTokenEmail(current_user)

        if not validateUser:
            audit_trail_controller.log_action('GET', '/developers/getSecretKey', "Unauthorized access attempt")
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 401

        user = DevelopersController().getDeveloperByEmail(current_user)
        de_secret_key = decrypt_secret(user['dev_secret_key'])
        audit_trail_controller.log_action('GET', '/developers/getSecretKey', f"Retrieved secret key for developer {current_user}")
        return jsonify(secret_key=de_secret_key)
    except Exception as e:
        audit_trail_controller.log_action('GET', '/developers/getSecretKey', f"Unexpected error: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred while retrieving secret key'}), 500

@developerBlueprint.route('/2fa/verify', methods=['POST'])
@jwt_required()
def verify2FA():
    try:
        current_user = get_jwt_identity()
        validateUser = DevelopersController().validateTokenEmail(current_user)

        if not validateUser:
            audit_trail_controller.log_action('POST', '/developers/2fa/verify', "Unauthorized access attempt")
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 401

        data = request.get_json()
        if not data:
            audit_trail_controller.log_action('POST', '/developers/2fa/verify', "No data provided")
            raise BadRequest('No data provided')
        
        user = DevelopersController().getDeveloperByEmail(current_user)
        server_token = get_totp_token(decrypt_secret(user['dev_secret_key']))
        
        if server_token == data['code']:
            update2FA = DevelopersController().update2FAbyEmail(current_user)
            audit_trail_controller.log_action('POST', '/developers/2fa/verify', f"2FA verified for developer {current_user}")
            return jsonify(success=update2FA), 200
        else:
            audit_trail_controller.log_action('POST', '/developers/2fa/verify', f"2FA verification failed for developer {current_user}")
            return jsonify(success=False), 401
    except Exception as e:
        audit_trail_controller.log_action('POST', '/developers/2fa/verify', f"Unexpected error: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred during 2FA verification'}), 500

@developerBlueprint.route('/generate-api-key', methods=['POST'])
@jwt_required()
def generate_api_key():
    try:
        current_user = get_jwt_identity()
        validateUser = DevelopersController().validateTokenEmail(current_user)

        if not validateUser:
            audit_trail_controller.log_action('POST', '/developers/generate-api-key', "Unauthorized access attempt")
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 401
        
        dev_id = get_jwt()['dev_id']

        if not dev_id:
            audit_trail_controller.log_action('POST', '/developers/generate-api-key', "Developer ID is required")
            return jsonify({'success': False, 'message': 'Developer ID is required'}), 400

        api_data = generate_encrypted_api_key()
        public_key_pem = api_data['public_key'].public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        encoded_ciphertext = base64.b64encode(api_data['ciphertext']).decode('utf-8')
        encoded_iv = base64.b64encode(api_data['iv']).decode('utf-8')
        encoded_signature = base64.b64encode(api_data['signature']).decode('utf-8')
        encoded_public_key = base64.b64encode(public_key_pem).decode('utf-8')

        success = DevelopersController().saveApiKey(dev_id, encoded_iv, encoded_ciphertext, encoded_signature, encoded_public_key)
        audit_trail_controller.log_action('POST', '/developers/generate-api-key', f"API key generation {'successful' if success else 'failed'} for developer ID {dev_id}")

        if success:
            return jsonify({'success': True, 'message': 'API key generated', 'api_key': encoded_ciphertext, 'iv': encoded_iv, 'signature': encoded_signature}), 200
        else:
            return jsonify({'success': False, 'message': 'Failed to generate API key'}), 500
    except Exception as e:
        audit_trail_controller.log_action('POST', '/generate-api-key', f"Unexpected error: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred during API key generation'}), 500

@developerBlueprint.route('/api-keys', methods=['GET'])
@jwt_required()
def get_api_keys():
    try:
        current_user = get_jwt_identity()
        validateUser = DevelopersController().validateTokenEmail(current_user)

        if not validateUser:
            audit_trail_controller.log_action('GET', '/developers/api-keys', "Unauthorized access attempt")
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 401

        dev_id = get_jwt()['dev_id']

        if not dev_id:
            audit_trail_controller.log_action('GET', '/developers/api-keys', "Developer ID is required")
            return jsonify({'success': False, 'message': 'Developer ID is required'}), 400

        api_keys = DevelopersController().getApiKeys(dev_id)
        audit_trail_controller.log_action('GET', '/developers/api-keys', f"Retrieved API keys for developer ID {dev_id}")
        return jsonify({'success': True, 'api_keys': api_keys}), 200
    except Exception as e:
        audit_trail_controller.log_action('GET', '/developers/api-keys', f"Unexpected error: {e}")
        print(f"Error fetching API keys: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred while fetching API keys'}), 500

@developerBlueprint.route('/api-keys/<api_id>', methods=['DELETE'])
@jwt_required()
def delete_api_key(api_id):
    try:
        current_user = get_jwt_identity()
        validateUser = DevelopersController().validateTokenEmail(current_user)

        if not validateUser:
            audit_trail_controller.log_action('DELETE', f'/developers/api-keys/{api_id}', "Unauthorized access attempt")
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 401

        success = DevelopersController().deleteApiKey(api_id)
        
        if success:
            audit_trail_controller.log_action('DELETE', f'/developers/api-keys/{api_id}', f"API key deletion {'successful' if success else 'failed'} for API ID {api_id}")
            return jsonify({'success': True, 'message': 'API key deleted successfully'}), 200
        else:
            audit_trail_controller.log_action('DELETE', f'/developers/api-keys/{api_id}', "Failed to delete API key")
            return jsonify({'success': False, 'message': 'Failed to delete API key'}), 400
    except Exception as e:
        audit_trail_controller.log_action('DELETE', f'/developers/api-keys/{api_id}', f"Unexpected error: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred while deleting API key'}), 500
