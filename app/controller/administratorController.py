from flask import Blueprint, render_template, request, session, jsonify
from ..models.administrator import Administrator


adminBlueprint = Blueprint('adminBlueprint', __name__)

@adminBlueprint.route("/login/admin",methods=['GET', 'POST'])
def adminLogin():
    
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        admin = Administrator.validateLogin(username, password)
        
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
            print(1)
            return jsonify(success=False), 400
    


