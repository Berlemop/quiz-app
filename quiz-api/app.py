from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime
import jwt_utils
import db_setup
from Question import Question
from Participation import Participation 


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

@app.route('/questions', methods=['POST', 'GET'])
def question():
	if request.method == 'POST':
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
			question = Question.from_dict(question_data)
			question_id = question.save()
			return jsonify({"id": question_id}), 200
			
		except Exception as e:
			return jsonify({"error": str(e)}), 500
	else: #GET
		position = request.args.get('position')
		if position:
			try:
				position_int = int(position)
				question = Question.get_by_position(position_int)
				if question is None:
					return jsonify({"error": "Question not found"}), 404
                
				return jsonify(question.to_dict()), 200
			except ValueError:
			    return jsonify({"error": "Invalid position"}), 400
		else:
		    questions_list = Question.get_all()
		    return jsonify([q.to_dict() for q in questions_list]), 200

@app.route('/questions/all', methods=['DELETE'])
def delete_all_questions():
    """
    Supprime toutes les questions
    Nécessite une authentification
    """
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
    try:
        Question.delete_all()
        return '', 204  # 
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/questions/<int:question_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_question_by_id(question_id):
    if request.method == 'PUT':
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
        
        question = Question.get_by_id(question_id)
        if question is None:
            return jsonify({"error": "Question not found"}), 404
        
        question_data = request.get_json()
        if not question_data:
            return 'Bad Request', 400
        
        try:
            Question.update_by_id(question_id, question_data)
            return '', 204
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    elif request.method == 'DELETE':
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
        
        question = Question.get_by_id(question_id)
        if question is None:
            return jsonify({"error": "Question not found"}), 404
        
        try:
            Question.delete_by_id(question_id)
            return '', 204
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    else:
        question = Question.get_by_id(question_id)
        
        if question is None:
            return jsonify({"error": "Question not found"}), 404
        
        return jsonify(question.to_dict()), 200


@app.route('/rebuild-db', methods=['POST'])
def rebuild_db():
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
	
	try:
		db_setup.rebuild_database()
		return "Ok", 200
	except Exception as e:
		return jsonify({"error": str(e)}), 500

@app.route('/participations/all', methods=['DELETE'])
def delete_all_participations():
    """
    Supprime toutes les participations
    Nécessite une authentification
    """
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
    
    try:
        Participation.delete_all()
        return '', 204  
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()