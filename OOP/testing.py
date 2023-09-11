import sqlite3, pickle, cv2, face_recognition

class DatabaseManager:
  def __init__(self, db_name):
        self.db_name = db_name
        self.conn= sqlite3.connect(self.db_name)
        self.cursor= self.conn.cursor()

  def create_table(self):
      conn = sqlite3.connect(self.db_name)
      cursor = conn.cursor()
      # Create the table if it doesn't exist
      cursor.execute('''
          CREATE TABLE IF NOT EXISTS face_data (
              id INTEGER PRIMARY KEY,
              email TEXT UNIQUE,
              name TEXT UNIQUE,
              age INTEGER,
              occupation TEXT,
              face_encoding BLOB,
              image_folder TEXT
          )
      ''')
      conn.commit()
      conn.close()
    
  def check_existing_data(self, email, name, face_encoding, image_folder):
    try:
        # Check if the email, name, face encoding, or image path already exists in the database
        self.cursor.execute('''
            SELECT * FROM face_data WHERE email=? OR name=? OR face_encoding=? OR image_folder=?
        ''', (email, name, face_encoding, image_folder))

        existing_data = self.cursor.fetchone()

        return existing_data

    except sqlite3.Error as e:
        print("Error while checking existing data:", e)
        return None
      
  def insert_data(self, email, name, age, occupation, face_encoding, image_folder):
    try:
      # Check if the data already exists
        existing_data = self.check_existing_data(email, name, face_encoding, image_folder)
        if existing_data:
            print("Data already exists in the database")
            return

        # Insert data into the table
        self.cursor.execute('''
            INSERT INTO face_data (email, name, age, occupation, face_encoding, image_folder)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (email, name, age, occupation, face_encoding, image_folder))

        # Save the changes and close the connection
        self.conn.commit()

        print("Data inserted successfully!")

    except sqlite3.Error as e:
        print("Error while inserting data:", e)
        
  def load_known_face_encodings(self):
        known_face_encodings = {}
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT name, face_encoding FROM face_data
            ''')

            rows = cursor.fetchall()
            for name, face_encoding in rows:
                face_encoding = pickle.loads(face_encoding)
                known_face_encodings[name] = face_encoding

            conn.close()

        except sqlite3.Error as e:
            print("Error while loading known face encodings:", e)

        return known_face_encodings

        
  def disconnect(self):
    if self.conn:
      self.conn.close()
      self.conn = None
      self.cursor = None
      


class FaceRecognitionModel:
    def __init__(self):
        self.known_face_encodings = {}

    def load_known_face_encodings(self, database_manager):
        self.known_face_encodings = database_manager.load_known_face_encodings()
        return self.known_face_encodings

    def recognize_person(self, face_encoding):
        for name, known_encodings in self.known_face_encodings.items():
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.3)
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