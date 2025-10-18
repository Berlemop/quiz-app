import sqlite3

DATABASE_PATH = 'base_de_donnees.db'


class Participation:
    
    def __init__(self, playerName: str, score: int, answers: list = None):
        self.id = None
        self.playerName = playerName
        self.score = score
        self.answers = answers if answers is not None else []
    
    
    @staticmethod
    def delete_all():
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM participations')
            conn.commit()
        finally:
            conn.close()
    
    
    @staticmethod
    def get_all():
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, playerName, score, date 
                FROM participations 
                ORDER BY score DESC, date DESC
            ''')
            participations_rows = cursor.fetchall()
            
            participations = []
            for row in participations_rows:
                participation = {
                    'id': row[0],
                    'playerName': row[1],
                    'score': row[2],
                    'date': row[3]
                }
                participations.append(participation)
            
            return participations
            
        finally:
            conn.close()