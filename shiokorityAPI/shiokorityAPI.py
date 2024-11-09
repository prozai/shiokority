from flask import Flask
from flask_cors import CORS
from config import config 
import os
from datetime import timedelta

#This is Root route for this application, so if needed just create a blueprint for your controller, do not create your own app route in your controller.
app = Flask(__name__)

from flask_cors import CORS

CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

config_name = os.getenv('FLASK_ENV', 'testing')
app.config.from_object(config[config_name])

# app.config.update(
#     SESSION_COOKIE_SECURE=True,  # For HTTPS
#     SESSION_COOKIE_HTTPONLY=True,  # Prevent XSS
#     SESSION_COOKIE_SAMESITE='Lax',  # CSRF protection
#     PERMANENT_SESSION_LIFETIME=timedelta(hours=24),  # Session duration
# )

#Registering blueprints
from app.view.merchantView import merchantBlueprint
app.register_blueprint(merchantBlueprint,  url_prefix='/merchant')

from app.view.adminView import adminBlueprint
app.register_blueprint(adminBlueprint, url_prefix='/admin')

from app.view.consumerView import consumerBlueprint
app.register_blueprint(consumerBlueprint, url_prefix='/consumer')

from app.view.developerView import developerBlueprint
app.register_blueprint(developerBlueprint, url_prefix='/developers')

from app.view.bankView import bankBlueprint
app.register_blueprint(bankBlueprint, url_prefix='/bank')

# Root route for testing
@app.route("/")
def hello():
    return "this is main page without anything"

if __name__ == "__main__":
    app.run(port=5001)
