from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime
import jwt_utils

import Question


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

@app.route('/questions', methods=['POST'])
def post_question():
	auth_header = request.headers.get('Authorization')
	if not auth_header:
		return 'Unauthorized', 401

	try:
		token = auth_header.replace('Bearer ', '')
		
		jwt_utils.decode_token(token)
		
	except jwt_utils.JwtError:
		return 'Unauthorized', 401
	except Exception:
		return 'Unauthorized', 401
	
	question_data = request.get_json()
	
	if not question_data:
		return 'Bad Request', 400
	
	required_fields = ['title', 'text', 'position', 'possibleAnswers']
	for field in required_fields:
		if field not in question_data:
			return jsonify({"error": f"Missing field: {field}"}), 400
	
	try:
		question_id = question_manager.add_question(question_data)
		
		return jsonify({"id": question_id}), 200
		
	except Exception as e:
		return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()