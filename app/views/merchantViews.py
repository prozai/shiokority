# app/views/dashboard.py
from flask import Flask, request, render_template_string, session, redirect, url_for, flash
from app.controller.merchantController import authenticateMerchant, createAccount
from app.models.merchant import Merchant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///merchants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Needed for session management

from app.models.merchant import db
db.init_app(app)

@app.route('/login', methods=['GET', 'POST'])
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

    # Inline HTML template as a string for simplicity
    template = """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Merchant Login</title>
    </head>
    <body>
        <h2>Login</h2>
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
        <form method="POST">
            <input type="email" name="email" placeholder="Email" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Login</button>
        </form>
        <p>Don't have an account? <a href="{{ url_for('accountCreationPage') }}">Register here</a></p>
    </body>
    </html>
    """
    return render_template_string(template, error=error)

@app.route('/register', methods=['GET', 'POST'])
def accountCreationPage():
    result = None
    if request.method == 'POST':
        form_data = request.form
        result = createAccount(form_data)
    
    template = """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Register Merchant</title>
    </head>
    <body>
        <h2>Register</h2>
        {% if result %}
            <div class="{% if result.success %}success{% else %}error{% endif %}">
                {{ result.message }}
            </div>
        {% endif %}

        <form method="POST">
            <input type="text" name="name" placeholder="Name" required><br>
            <input type="email" name="email" placeholder="Email" required><br>
            <input type="text" name="business_name" placeholder="Business Name" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Create Account</button>
        </form>
        <p>Already have an account? <a href="{{ url_for('loginPage') }}">Login here</a></p>
    </body>
    </html>
    """
    return render_template_string(template, result=result)

@app.route('/merchantViews')
def dashboard():
    if 'merchantID' not in session:
        return redirect(url_for('loginPage'))  # Redirect to login if not logged in
    merchant = Merchant.query.get(session['merchantID'])  # Retrieve merchant from the database
    template = """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Profile</title>
    </head>
    <body>
        <h1>Welcome to your dashboard!<h1>
        <h2>Profile</h2>
        <p>Username: {{ merchant.name }}</p>
        <p>Email: {{ merchant.email }}</p>
        <form method="POST" action="{{ url_for('logout') }}">
            <button type="submit">Log-Out</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(template, merchant=merchant)
@app.route('/logout', methods=['POST'])
def logout():
    if 'merchantID' in session:
        session.pop('merchantID')  # Remove the merchant ID from the session
        flash('You have been logged out successfully.')
    return redirect(url_for('loginPage'))  # Redirect to login page after logout