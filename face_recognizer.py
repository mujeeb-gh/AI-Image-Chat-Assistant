import sqlite3, database_manager, pickle

class FaceRecognizer:
  @staticmethod
  def load_known_face_encodings(database_manager):
    known_face_encodings = {}
    try:
        # Connect to the database
        database_manager.connect()

        # Load face encodings and other information from the database
        database_manager.cursor.execute('''
            SELECT name, face_encoding FROM face_data
        ''')

        rows = database_manager.cursor.fetchall()
        for name, face_encoding in rows:
            face_encoding = pickle.loads(face_encoding)
            known_face_encodings[name] = face_encoding

    except sqlite3.Error as e:
      print("Error while loading known face encodings:", e)
    
    finally:
      database_manager.disconnect()
      
    return known_face_encodings
  
  @staticmethod
  def recogni