from flask import Blueprint, render_template, request, session, jsonify
from ..models.administrator import Administrator


adminBlueprint = Blueprint('adminBlueprint', __name__)

@adminBlueprint.route("/login/admin",methods=['GET', 'POST'])
def adminLogin():
    
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        admin = Administrator(username,password).validateLogin()
        
        if admin is not False:
            session['id'] = admin['admin_id']
            session['user_email'] = admin['admin_username']
            session['loggedIn'] = True
            print("success")
            return jsonify(success=True), 200
        else:
            return jsonify(success=False), 200

@adminBlueprint.route("/logout/admin",methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200


