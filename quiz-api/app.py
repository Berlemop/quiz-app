from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime


app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def login():
    

    return jsonify({"token": token}), 200


if __name__ == "__main__":
    app.run()