from flask import Flask
from waitress import serve

# Import the app from the dashboard (which contains the main application logic)
from app.views.merchantViews import app

@app.route("/")
def hello():
    return "Hello, this is waitress"

mode = "development"

if __name__ == "__main__":
  
    # Ensure the database is created before starting the server
    with app.app_context():
        from app.models.merchant import db
        db.create_all()

    # for debugging
    if mode == "development":
        app.run(host="0.0.0.0", port=5000, debug=True)
    else:
        serve(app, host="0.0.0.0", port=5000, threads=1)
