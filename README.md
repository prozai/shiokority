# shiokority


Window User
#clone our repo
1. git clone https://github.com/prozai/shiokority.git
2. --> python -m venv env
3. --> env\Scripts\activate.bat
4. --> pip install -r requirements.txt
5. you can start develop your features!

Mac User
#clone our repo
1. git clone https://github.com/prozai/shiokority.git
2. --> python3 -m venv env
3. --> source env/bin/activate
4. --> pip install -r requirements.txt
5. you can start develop your features!

Deactivating the Virtual Environment

Windows: --> env\Scripts\deactivate.bat

macOS/Linux: --> deactivate


Frontend Setup (React)

Ensure you have Node.js installed.

Navigate to the frontend directory:
1. --> cd frontend

Install the required Node.js dependencies:

2. --> npm install

Update the React proxy (if necessary):

If you changed the port in config.py, update the proxy setting in frontend/package.json:

  "proxy": "http://localhost:5001"

Start the React application:

npm start


