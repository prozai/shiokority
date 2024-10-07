from flask import Blueprint, request, jsonify, session, send_file
from werkzeug.exceptions import BadRequest
from app.controller.developersController import DevelopersController
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

    if not ifLogin:
        return jsonify(ifLogin)
        
    session['email'] = data.get('email')
    return jsonify(ifLogin)

@developerBlueprint.route('/auth/2FA', methods=['POST'])
def auth2FA():
    data = request.get_json()

    if not data:
        raise BadRequest('No data provided')
    
    user = DevelopersController().getDeveloperByEmail(session['email'])

    if user.verify_totp(data['token']):
        return jsonify(success=True), 200
    else:
        return jsonify(success=False), 401

@developerBlueprint.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

@developerBlueprint.route('/getQRcode', methods=['GET'])
def getQRcode():
    
    # need get secret key from database
    user = DevelopersController().getDeveloperByEmail(session['email'])
    
    totp_uri = generate_totp_uri(session['email'], decrypt_secret(user['secret_key']))
    qr_code = create_qr_code(totp_uri)
    
    return send_file(qr_code, mimetype='image/png')

@developerBlueprint.route('/getSecretKey', methods=['GET'])
def getSecretKey():
    user = DevelopersController().getDeveloperByEmail(session['email'])

    de_secret_key = decrypt_secret(user['secret_key'])

    return jsonify(secret_key=de_secret_key)
    
@developerBlueprint.route('/2fa/verify', methods=['POST'])
def verify2FA():
    data = request.get_json()

    if not data:
        raise BadRequest('No data provided')
    
    user = DevelopersController().getDeveloperByEmail(session['email'])

    server_token = get_totp_token(decrypt_secret(user['secret_key']))

    if server_token == data['code']:
        update2FA = DevelopersController().update2FAbyEmail(session['email'])
        return jsonify(success=update2FA), 200
    else:
        return jsonify(success=False), 401