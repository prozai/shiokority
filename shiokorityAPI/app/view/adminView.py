from flask import Blueprint, request, session, jsonify
from werkzeug.exceptions import BadRequest
from ..controller.administratorController import AdminController

adminBlueprint = Blueprint('adminBlueprint', __name__)

admin_controller = AdminController()

@adminBlueprint.route("/login/admin", methods=['POST'])
def adminLogin():
    try:
        data = request.get_json()

        if not data:
            raise BadRequest("No input data provided")
        
        email = data.get('email', '')
        password = data.get('password', '')
        
        if not email or not password:
            raise BadRequest("Email and password are required")

        admin = admin_controller.validate_admin_login(email, password)
        
        if admin:
            session['loggedIn'] = True
            return jsonify(success=True), 200
        else:
            return jsonify(success=False), 401

    except BadRequest as e:
        return jsonify(success=False, message=str(e)), 400
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500

@adminBlueprint.route("/logout/admin", methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

@adminBlueprint.route("/create-merchant", methods=['POST'])
def createMerchant():
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("No input data provided")

        createdMerchant = admin_controller.create_merchant(data)

        if createdMerchant:
            return jsonify(success=True), 200
        else:
            return jsonify(success=False, message="Failed to create merchant"), 400

    except BadRequest as e:
        return jsonify(success=False, message=str(e)), 400
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500

@adminBlueprint.route('/admin/view-merchant', methods=['GET'])
def fetchMerchantList():
    try:
        merchants = admin_controller.get_merchant_data()
        if merchants:
            return jsonify(merchants), 200
        else:
            return jsonify(success=False, message="No merchants found"), 404
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500
        
@adminBlueprint.route('/admin/merchants/<merch_id>', methods=['GET'])
def getMerchant(merch_id):
    try:
        merchant = admin_controller.get_one_merchant(merch_id)
        
        if merchant:
            return jsonify(merchant), 200
        else:
            return jsonify(success=False, message="Merchant not found"), 404

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500

@adminBlueprint.route('/admin/merchants/<merch_id>', methods=['PUT'])
def submitMerchantUpdate(merch_id):
    try:
        data = request.json

        if not data:
            raise BadRequest("No input data provided")

        updateStatus = admin_controller.update_merchant_details(merch_id, data)
        
        if updateStatus:
            return jsonify(success=True), 200
        else:
            return jsonify(success=False, message="Failed to update merchant"), 400
        
    except BadRequest as e:
        return jsonify(success=False, message=str(e)), 400

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500
    
@adminBlueprint.route('/admin/suspend-merchants/<merch_id>', methods=['PUT'])
def updateMerchantStatus(merch_id):
    try:
        data = request.json
        if not data:
            raise BadRequest("No input data provided")

        status = data.get('status')
        
        updateStatus = admin_controller.update_merchant_status(merch_id, status)
        
        if updateStatus:
            return jsonify(success=True), 200
        else:
            return jsonify(success=False, message="Failed to update merchant status"), 400
        
    except BadRequest as e:
        return jsonify(success=False, message=str(e)), 400

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500


# My work of art
@adminBlueprint.route("/admin/add-user", methods=['POST'])
def addUser():
    if request.method == 'POST':
            data = request.get_json()  # Get the JSON data from the request

            # Extract the necessary fields
            email = data.get('email', '')
            password = data.get('password', '')
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')
            status = data.get('status', True)  # default to True if not provided

            createdUser = admin_controller.addUser(email, password, first_name, last_name, status)

            if createdUser:
                return jsonify(success=True), 200
            else:
                return jsonify(success=False), 400


@adminBlueprint.route('/admin/get-users', methods=['GET'])
def getAllUser():
    try:
        users = admin_controller.get_all_users()
        if users:
            return jsonify(users), 200
        else:
            return jsonify({"error": "No users found"}), 404

    except Exception as e:
        print(f"An error occurred: {e}")  # Log the error
        return jsonify({"error": "An unexpected error occurred"}), 500


@adminBlueprint.route('/admin/users/<int:user_id>/update', methods=['PUT'])
def submitUserUpdate(user_id):
    try:
        data = request.get_json()

        # Extract the necessary fields (similar to addUser)
        email = data.get('email', None)
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        status = data.get('status', None)

        # Update the user with the new details
        updateStatus = admin_controller.submit_user_update(user_id, email, first_name, last_name, status)

        if updateStatus:
            return jsonify(success=True), 200
        else:
            return jsonify(success=False), 400

    except Exception as e:
        print(f"Error updating user details: {e}")
        return jsonify({"error": "Failed to update user details"}), 500