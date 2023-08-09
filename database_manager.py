import sqlite3

class DatabaseManager:
  def __init__(self, database_name):
    self.database_name = database_name
    self.conn = None
    self.cursor= None
  
  def connect(self):
    self.conn = sqlite3.connect(self.database_name)
    self.cursor = self.conn.cursor()
    
  def create_table(self):
    self.cursor.execute('''
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
    self.conn.commit()
    
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
        
  def disconnect(self):
    if self.conn:
      self.conn.close()
      self.conn = None
      self.cursor = None