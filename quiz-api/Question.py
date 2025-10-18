import sqlite3

DATABASE_PATH = 'base_de_donnees.db'


class Question:
    
    def __init__(self, title: str, text: str, position: int, image: str = "", possibleAnswers: list = None):
        self.id = None  # L'ID sera défini après insertion en BDD
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
        Génère une requête SQL INSERT à partir de l'objet Python
        """
        conn = sqlite3.connect(DATABASE_PATH)
        conn.isolation_level = None  
        cursor = conn.cursor()
        
        try:
            cursor.execute("begin")
            
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
        Récupère une question depuis la BDD par son ID (SELECT)
        Génère un objet Python à partir du retour d'une requête SQL SELECT
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
                
                cursor.execute('SELECT text, isCorrect FROM answers WHERE question_id = ?', (question_id,))
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
        """
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM questions WHERE id = ?', (question_id,))
            conn.commit()
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
            # Les réponses sont supprimées automatiquement grâce à ON DELETE CASCADE
            cursor.execute('DELETE FROM questions')
            conn.commit()
        finally:
            conn.close()
    
    @staticmethod
    def update_by_id(question_id: int, data: dict):
        """
        Met à jour une question et ses réponses
        Gère les conflits de position
        """
        conn = sqlite3.connect(DATABASE_PATH)
        conn.isolation_level = None
        cursor = conn.cursor()
        
        try:
            cursor.execute("begin")
            
            # Vérifier si la nouvelle position est déjà utilisée par une autre question
            new_position = data.get('position')
            cursor.execute('''
                SELECT id FROM questions 
                WHERE position = ? AND id != ?
            ''', (new_position, question_id))
            
            conflicting_question = cursor.fetchone()
            
            if conflicting_question:
                # Déplacer temporairement la question en conflit vers une position très haute
                cursor.execute('''
                    UPDATE questions
                    SET position = (SELECT MAX(position) + 1 FROM questions)
                    WHERE id = ?
                ''', (conflicting_question[0],))
            
            # Mettre à jour la question
            cursor.execute('''
                UPDATE questions
                SET title = ?, text = ?, image = ?, position = ?
                WHERE id = ?
            ''', (
                data.get('title'),
                data.get('text'),
                data.get('image', ''),
                new_position,
                question_id
            ))
            
            # Supprimer les anciennes réponses
            cursor.execute('DELETE FROM answers WHERE question_id = ?', (question_id,))
            
            # Ajouter les nouvelles réponses
            if 'possibleAnswers' in data:
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



