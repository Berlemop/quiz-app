import sqlite3
import os

DATABASE_PATH = 'base_de_donnees.db'


def rebuild_database():
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
        print(f"Base de données existante supprimée : {DATABASE_PATH}")
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        # Table des questions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                text TEXT NOT NULL,
                image TEXT,
                position INTEGER NOT NULL 
            )
        ''')
        
        # Table des réponses possibles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                isCorrect INTEGER NOT NULL,
                FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
            )
        ''')
        
        # Table des participations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS participations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                playerName TEXT NOT NULL,
                score INTEGER NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des réponses données lors des participations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS participation_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                participation_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                answer_text TEXT NOT NULL,
                FOREIGN KEY (participation_id) REFERENCES participations(id) ON DELETE CASCADE,
                FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        
    except Exception as e:
        print(f" Erreur : {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()


if __name__ == "__main__":
    rebuild_database()