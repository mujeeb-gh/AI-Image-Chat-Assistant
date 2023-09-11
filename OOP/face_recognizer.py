import sqlite3, database_manager, pickle, face_recognition

class FaceRecognitionModel:
    def __init__(self):
        self.known_face_encodings = {}

    def load_known_face_encodings(self, database_manager):
        self.known_face_encodings = database_manager.load_known_face_encodings()
        return self.known_face_encodings

    def recognize_person(self, face_encoding):
        for name, known_encodings in self.known_face_encodings.items():
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.4)
            if any(matches):
                return name
        return None
      
    def calculate_similarity(self, face_encoding, name):
        known_face_encoding_arr = self.known_face_encodings[name]
        similarity_scores = face_recognition.face_distance(known_face_encoding_arr, face_encoding)
        similarity_percentage = (1 - similarity_scores[0]) * 100
        return similarity_percentage

  