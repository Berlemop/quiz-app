import sqlite3

DATABASE_PATH = 'base_de_donnees.db'


class Question:
    
    def __init__(self, title: str, text: str, position: int, image: str = "", possibleAnswers: list = None):
        self.id = None
        self.title = title
        self.text = text
        self.image = image
        self.position = position
        self.possibleAnswers = possibleAnswers if possibleAnswers is not None else []
    
    
    def to_dict(self):
        """
        Question en dictionnaire pour JSONification
        """
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'image': self.image,
            'position': self.position,
            'possibleAnswers': self.possibleAnswers
        }
    
    
    @staticmethod
    def from_dict(data: dict):
        """
        Crée un objet Question à partir d'un dictionnaire
        """
        question = Question(
            title=data.get('title'),
            text=data.get('text'),
            position=data.get('position'),
            image=data.get('image', ''),
            possibleAnswers=data.get('possibleAnswers', [])
        )
        if 'id' in data:
            question.id = data['id']
        return question
    
    
    def save(self):
        """
        Sauvegarde la question dans la BDD 
        Gère automatiquement le réordonnancement des positions
        """
        conn = sqlite3.connect(DATABASE_PATH)
        conn.isolation_level = None  
        cursor = conn.cursor()
        
        try:
            cursor.execute("begin")
            
            cursor.execute('SELECT id FROM questions WHERE position = ?', (self.position,))
            existing = cursor.fetchone()
            
            if existing:
                cursor.execute('SELECT MAX(position) FROM questions')
                max_pos = cursor.fetchone()[0]
                
                cursor.execute('''
                    UPDATE questions
                    SET position = position + ? + 1
                    WHERE position >= ?
                ''', (max_pos, self.position))
                
                cursor.execute('''
                    UPDATE questions
                    SET position = position - ?
                    WHERE position > ?
                ''', (max_pos, max_pos))
            
            cursor.execute('''
                INSERT INTO questions (title, text, image, position)
                VALUES (?, ?, ?, ?)
            ''', (self.title, self.text, self.image, self.position))
            
            self.id = cursor.lastrowid
            
            for answer in self.possibleAnswers:
                cursor.execute('''
                    INSERT INTO answers (question_id, text, isCorrect)
                    VALUES (?, ?, ?)
                ''', (self.id, answer['text'], answer['isCorrect']))
            
            cursor.execute("commit")
            return self.id
            
        except Exception as e:
            cursor.execute('rollback')
            raise e
        finally:
            conn.close()
    
    
    @staticmethod
    def get_by_id(question_id: int):
        """
        Récupère une question depuis la BDD par son ID
        """
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, title, text, image, position
                FROM questions
                WHERE id = ?
            ''', (question_id,))
            
            row = cursor.fetchone()
            
            if not row:
                return None
            
            cursor.execute('''
                SELECT text, isCorrect
                FROM answers
                WHERE question_id = ?
                ORDER BY id
            ''', (question_id,))
            
            answers_rows = cursor.fetchall()
            
            question = Question(
                title=row[1],
                text=row[2],
                image=row[3],
                position=row[4],
                possibleAnswers=[
                    {'text': ans[0], 'isCorrect': bool(ans[1])}
                    for ans in answers_rows
                ]
            )
            question.id = row[0]
            
            return question
            
        finally:
            conn.close()
    
    
    @staticmethod
    def get_by_position(position: int):
        """
        Récupère une question depuis la BDD par sa position
        """
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, title, text, image, position
                FROM questions
                WHERE position = ?
            ''', (position,))
            
            row = cursor.fetchone()
            
            if not row:
                return None
            
            cursor.execute('''
                SELECT text, isCorrect
                FROM answers
                WHERE question_id = ?
                ORDER BY id
            ''', (row[0],))
            
            answers_rows = cursor.fetchall()
            
            question = Question(
                title=row[1],
                text=row[2],
                image=row[3],
                position=row[4],
                possibleAnswers=[
                    {'text': ans[0], 'isCorrect': bool(ans[1])}
                    for ans in answers_rows
                ]
            )
            question.id = row[0]
            
            return question
            
        finally:
            conn.close()
    
    
    @staticmethod
    def get_all():
        """
        Récupère toutes les questions depuis la BDD
        """
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT id, title, text, image, position FROM questions ORDER BY position')
            questions_rows = cursor.fetchall()
            
            questions = []
            for row in questions_rows:
                question_id = row[0]
                
                cursor.execute('SELECT text, isCorrect FROM answers WHERE question_id = ? ORDER BY id', (question_id,))
                answers_rows = cursor.fetchall()
                
                question = Question(
                    title=row[1],
                    text=row[2],
                    image=row[3],
                    position=row[4],
                    possibleAnswers=[
                        {'text': ans[0], 'isCorrect': bool(ans[1])}
                        for ans in answers_rows
                    ]
                )
                question.id = question_id
                questions.append(question)
            
            return questions
            
        finally:
            conn.close()
    
    
    @staticmethod
    def delete_by_id(question_id: int):
        """
        Supprime une question et ses réponses associées
        Décale automatiquement les questions suivantes
        """
        conn = sqlite3.connect(DATABASE_PATH)
        conn.isolation_level = None
        cursor = conn.cursor()
        
        try:
            cursor.execute("begin")
            
            cursor.execute('SELECT position FROM questions WHERE id = ?', (question_id,))
            result = cursor.fetchone()
            
            if result:
                position = result[0]
                
                cursor.execute('DELETE FROM questions WHERE id = ?', (question_id,))
                
                cursor.execute('''
                    UPDATE questions
                    SET position = position - 1
                    WHERE position > ?
                ''', (position,))
            else:
                cursor.execute('DELETE FROM questions WHERE id = ?', (question_id,))
            
            cursor.execute("commit")
            
        except Exception as e:
            cursor.execute('rollback')
            raise e
        finally:
            conn.close()
    
    
    @staticmethod
    def delete_all():
        """
        Supprime toutes les questions et leurs réponses associées
        """
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM questions')
            conn.commit()
        finally:
            conn.close()
    
    
    @staticmethod
    def delete_by_position(position: int):
        """
        Supprime une question à une position donnée
        et décale toutes les questions suivantes vers le haut
        """
        conn = sqlite3.connect(DATABASE_PATH)
        conn.isolation_level = None
        cursor = conn.cursor()
        
        try:
            cursor.execute("begin")
            
            cursor.execute('SELECT id FROM questions WHERE position = ?', (position,))
            result = cursor.fetchone()
            
            if not result:
                raise Exception("Question not found at this position")
            
            question_id = result[0]
            
            cursor.execute('DELETE FROM questions WHERE id = ?', (question_id,))
            
            cursor.execute('''
                UPDATE questions
                SET position = position - 1
                WHERE position > ?
            ''', (position,))
            
            cursor.execute("commit")
            
        except Exception as e:
            cursor.execute('rollback')
            raise e
        finally:
            conn.close()
    
    
    @staticmethod
    def update_by_id(question_id: int, data: dict):
        """
        Met à jour une question et gère le réordonnancement complet des positions
        """
        conn = sqlite3.connect(DATABASE_PATH)
        conn.isolation_level = None
        cursor = conn.cursor()
        
        try:
            cursor.execute("begin")
            
            cursor.execute('''
                SELECT title, text, image, position 
                FROM questions 
                WHERE id = ?
            ''', (question_id,))
            result = cursor.fetchone()
            
            if not result:
                raise Exception("Question not found")
            
            current_title, current_text, current_image, old_position = result
            
            new_title = data.get('title', current_title)
            new_text = data.get('text', current_text)
            new_image = data.get('image', current_image)
            new_position = data.get('position', old_position)
            
            if old_position != new_position:
                cursor.execute('''
                    UPDATE questions
                    SET position = -1
                    WHERE id = ?
                ''', (question_id,))
                
                if new_position < old_position:
                    cursor.execute('''
                        UPDATE questions
                        SET position = position + 1
                        WHERE position >= ? AND position < ?
                    ''', (new_position, old_position))
                else:
                    cursor.execute('''
                        UPDATE questions
                        SET position = position - 1
                        WHERE position > ? AND position <= ?
                    ''', (old_position, new_position))
                
                cursor.execute('''
                    UPDATE questions
                    SET position = ?
                    WHERE id = ?
                ''', (new_position, question_id))
            
            cursor.execute('''
                UPDATE questions
                SET title = ?, text = ?, image = ?
                WHERE id = ?
            ''', (new_title, new_text, new_image, question_id))
            
            if 'possibleAnswers' in data:
                cursor.execute('DELETE FROM answers WHERE question_id = ?', (question_id,))
                
                for answer in data['possibleAnswers']:
                    cursor.execute('''
                        INSERT INTO answers (question_id, text, isCorrect)
                        VALUES (?, ?, ?)
                    ''', (question_id, answer['text'], answer['isCorrect']))
            
            cursor.execute("commit")
            
        except Exception as e:
            cursor.execute('rollback')
            raise e
        finally:
            conn.close()