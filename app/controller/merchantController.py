# controllers/merchantController.py
from flask import Flask, request, render_template, session, redirect, url_for, flash, Blueprint
from app.models.merchant import Merchant
from app.models.merchant import db, Merchant
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

merchantController = Blueprint('merchantController', __name__)

@merchantController.route('/login', methods=['GET', 'POST'])
def loginPage():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        merchant = authenticateMerchant(email, password)
        if merchant:
            session['merchantID'] = merchant.id  # Store the merchant ID in session
            return redirect(url_for('dashboard'))  # Redirect to dashboard after login
        else:
            error = 'Invalid email or password. Please try again.'
    return render_template("login.html",error=error)

@merchantController.route('/register', methods=['GET', 'POST'])
def accountCreationPage():
    result = None
    if request.method == 'POST':
        form_data = request.form
        result = createAccount(form_data)

    return render_template('register.html', result=result)

@merchantController.route('/merchantViews')
def dashboard():
    if 'merchantID' not in session:
        return redirect(url_for('loginPage'))  # Redirect to login if not logged in
    merchant = Merchant.query.get(session['merchantID'])  # Retrieve merchant from the database

    return render_template('dashboard.html', merchant=merchant)


@merchantController.route('/logout', methods=['GET, POST'])
def logout():
    if 'merchantID' in session:
        session.pop('merchantID')  # Remove the merchant ID from the session
        flash('You have been logged out successfully.')
    return redirect(url_for('merchantController.loginPage'))  # Redirect to login page after logout

def createAccount(form_data):
    email = form_data.get('email')
    if Merchant.query.filter_by(email=email).first():
        return {'success': False, 'message': 'Email is already in use'}

    try:
        merchant = Merchant(
            name=form_data.get('name'),
            email=email,
            business_name=form_data.get('business_name'),
            password=generate_password_hash(form_data.get('password'))
        )
        db.session.add(merchant)
        db.session.commit()
        return {'success': True, 'message': 'Account created successfully'}
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': str(e)}
    
def authenticateMerchant(email, password):
    merchant = Merchant.query.filter_by(email=email).first()
    if merchant and check_password_hash(merchant.password, password):
        return merchant
    return None
