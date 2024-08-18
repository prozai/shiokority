from flask import Flask, Blueprint, render_template
from app.models.merchant import db, Merchant

#This is Root route for this application, so if needed just create a blueprint for your controller, do not create your own app route in your controller.
app = Flask(__name__, template_folder=r'C:\Users\jiyuan\Desktop\shiokority\app\templates')

#here is the blueprint 
from app.controller.merchantController import merchantController
app.register_blueprint(merchantController)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///merchants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Needed for session management

db.init_app(app)

@app.route("/")
def hello():
    return "this is main page without anything"


if __name__ == "__main__":
  
    # Ensure the database is created before starting the server
    with app.app_context():
        from app.models.merchant import db
        db.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True)
