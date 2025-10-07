from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime
import jwt_utils


app = Flask(__name__)
CORS(app)

ADMIN_PASSWORD = "mdp" 

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def login():

	payload = request.get_json() 

	if not payload or 'password' not in payload:
		return 'Unauthorized', 401
	    
	password = payload['password']

	if password == ADMIN_PASSWORD:
		token = jwt_utils.build_token()
		return jsonify({"token": token}), 200
	else:
		return 'Unauthorized', 401 

if __name__ == "__main__":
    app.run()