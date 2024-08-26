from flask import Blueprint, render_template, request, session, jsonify
from ..models.administrator import Administrator


adminBlueprint = Blueprint('adminBlueprint', __name__)

@adminBlueprint.route("/login/admin",methods=['GET', 'POST'])
def adminLogin():
    
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        print(email, password)
        admin = Administrator.validateLogin(email, password)
        
        if admin is not False:
            session['id'] = admin['admin_id']
            session['user_email'] = admin['admin_username']
            session['loggedIn'] = True
            print("success")
            return jsonify(success=True), 200
        else:
            return jsonify(success=False), 400

@adminBlueprint.route("/logout/admin",methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

@adminBlueprint.route("/create-merchant",methods=['POST'])
def createMerchant():
    
    if request.method == 'POST':
        data = request.get_json()  # Get the JSON data from the request

        # Extract the necessary fields
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')

        # Validate the input
        if not name or not email or not phone:
            return jsonify({"error": "Name, address, and phone are required"}), 400
        
        createdMerchant = Administrator.createMerchant(name, email, phone)
        
        if createdMerchant:
            return jsonify(success=True), 200
        else:
            return jsonify(success=False), 400
    

@adminBlueprint.route('/admin/view-merchant', methods=['GET'])
def fetchMerchantList():
    
    if request.method == 'GET':
        
        merchants = Administrator().getMerchantData()
        
        if merchants is not False:
            return jsonify(merchants), 200
        else:
            return jsonify({"error": "Could not fetch merchant data"}), 500
        
@adminBlueprint.route('/admin/merchants/<int:merch_id>', methods=['GET'])
def getMerchant(merch_id):
    
    if request.method == 'GET':
        
        merchants = Administrator().getOneMerchant(merch_id)
        
        if merchants is not False:
            return jsonify(merchants), 200
        else:
            return jsonify({"error": "Could not fetch merchant data"}), 500
    
    pass

@adminBlueprint.route('/admin/merchants/<int:merch_id>', methods=['PUT'])
def submitMerchantUpdate(merch_id):
    
    if request.method == 'PUT':
        data = request.json
        
        updateStatus = Administrator().updateMerchantDetails(merch_id, data)
        
        if updateStatus:
            return jsonify({'message': 'Merchant updated successfully'}), 200
        else:
            return jsonify({'message': 'Merchant updated fail'}), 400
        
    else:
        return jsonify({'message': 'Bad Request!'}), 500
    
    
@adminBlueprint.route('/admin/suspend-merchants/<int:merch_id>', methods=['PUT'])
def updateMerchantStatus(merch_id):
    
    if request.method == 'PUT':
        
        updateStatus = Administrator().updateMerchantStatus(merch_id)
        
        if updateStatus:
            return jsonify({'message': 'Merchant updated successfully'}), 200
        else:
            return jsonify({'message': 'Merchant updated fail'}), 400
        
    else:
        return jsonify({'message': 'Bad Request!'}), 500