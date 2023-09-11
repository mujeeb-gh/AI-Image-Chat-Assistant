import sqlite3, pickle

# DatabaseManager is being implemented as a Singleton. A Singleton is a design pattern that ensures a class has only one instance and provides a global point of access to that instance
class DatabaseManager:
  _instance = None
  
  def __new__(cls, db_name):
    if cls._instance is None:
      cls._instance = super(DatabaseManager, cls).__new__(cls)
    return cls._instance
  
  def __init__(self, db_name):
    if not hasattr(self, 'initialized'):
      self.initialized = True
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