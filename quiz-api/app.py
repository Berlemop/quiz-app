from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime
import jwt_utils
import db_setup
import sqlite3
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
    try:
        questions = Question.get_all()
        size = len(questions)
        
        participations = Participation.get_all()
        
        scores = [
            {
                "playerName": participation.playerName,
                "score": participation.score
            }
            for participation in participations
        ]
        
        return jsonify({
            "size": size,
            "scores": scores
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

@app.route('/questions', methods=['GET', 'POST', 'DELETE'])
def question():
    if request.method == 'POST':
        # POST : Ajouter une question
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
    
    elif request.method == 'DELETE':
        # DELETE par position : DELETE /questions?position=X
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
        
        position = request.args.get('position')
        if not position:
            return jsonify({"error": "Position parameter required"}), 400
        
        try:
            position_int = int(position)
            question = Question.get_by_position(position_int)
            
            if question is None:
                return jsonify({"error": "Question not found"}), 404
            
            # Supprimer la question et réordonner
            Question.delete_by_position(position_int)
            return '', 204
            
        except ValueError:
            return jsonify({"error": "Invalid position"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    else:
        # GET : Récupérer les questions
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

@app.route('/participations', methods=['POST'])
def participate():
    participation_data = request.get_json()
    
    if not participation_data:
        return 'Bad Request', 400
    
    required_fields = ['playerName', 'answers']
    for field in required_fields:
        if field not in participation_data:
            return jsonify({"error": f"Missing field: {field}"}), 400
    
    playerName = participation_data.get('playerName')
    answers = participation_data.get('answers')
    
    if not playerName or not isinstance(playerName, str) or playerName.strip() == '':
        return jsonify({"error": "Invalid playerName"}), 400
    
    if not isinstance(answers, list):
        return jsonify({"error": "answers must be a list"}), 400
    
    try:
        
        questions = Question.get_all()
        
        if len(answers) != len(questions):
            return jsonify({"error": "Number of answers doesn't match number of questions"}), 400
        
       
        score = 0
        for i, answer in enumerate(answers):
            question = questions[i]
            if answer is not None and 0 <= answer < len(question.possibleAnswers):
                if question.possibleAnswers[answer]['isCorrect']:
                    score += 1
        conn = sqlite3.connect('base_de_donnees.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO participations (playerName, score, date)
            VALUES (?, ?, datetime('now'))
        ''', (playerName, score))
        
        participation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            "id": participation_id,
            "playerName": playerName,
            "score": score
        }), 200
        
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

@app.route('/debug/questions', methods=['GET'])
def debug_questions():
    """Route de debug pour voir les bonnes réponses"""
    questions = Question.get_all()
    debug_info = []
    for i, q in enumerate(questions):
        correct_indices = [idx for idx, ans in enumerate(q.possibleAnswers) if ans['isCorrect']]
        debug_info.append({
            'position': q.position,
            'title': q.title,
            'correct_answer_indices': correct_indices
        })
    return jsonify(debug_info), 200


if __name__ == "__main__":
    app.run()