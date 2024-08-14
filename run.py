from flask import Flask

from waitress import serve

app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello this is waitress"

mode = "development"

if __name__ == "__main__":
  
  #for debugging 
  if mode == "development":
    app.run(host="0.0.0.0", port=5000, debug=True)
  
  else:
    serve(app, host="0.0.0.0", port=5000, threads=1)
