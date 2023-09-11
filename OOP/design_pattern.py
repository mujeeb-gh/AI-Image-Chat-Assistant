import sqlite3, pickle, face_recognition, cv2


      
      

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


class FaceDetection:
  @staticmethod
  def detect_faces(frame):
    # Load Haar Cascade Classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        # Convert the frame to grayscale for face detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces
  

class ImageEncoder:
  @staticmethod
  def encode_image(image_path):
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)

    if len(face_encodings) > 0:
        return face_encodings[0]  # Only encode the first face found in the image
    else:
        return None