from flask import Flask, jsonify, render_template
from flask_cors import CORS
from config import config
import os

#This is Root route for this application, so if needed just create a blueprint for your controller, do not create your own app route in your controller.
app = Flask(__name__,template_folder=r"app\\templates")

# Enable CORS (Cross-Origin Resource Sharing)
CORS(app, supports_credentials=True)

#Load configuration
config_name = os.getenv('FLASK_ENV', 'testing')
app.config.from_object(config[config_name])

#Registering blueprints
from app.controller.merchantController import merchantBlueprint
app.register_blueprint(merchantBlueprint, url_prefix='/merchant')

from app.controller.administratorController import adminBlueprint
app.register_blueprint(adminBlueprint)

# Root route for testing
@app.route("/")
def hello():
    return "this is main page without anything"

if __name__ == "__main__":
    app.run(debug=True, port=5001)
    
