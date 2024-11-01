from flask import Flask
from flask_cors import CORS
from config import config 
import os

#This is Root route for this application, so if needed just create a blueprint for your controller, do not create your own app route in your controller.
app = Flask(__name__)

CORS(app)

config_name = os.getenv('FLASK_ENV', 'testing')
app.config.from_object(config[config_name])

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
