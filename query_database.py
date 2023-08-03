import face_recognition
import cv2
import sqlite3
import numpy as np
import os

DATABASE_NAME = "face_data.db"
KNOWN_FACES_DIR = "known_faces"

known_face_encodings = []

def create_database():
    # Connect to the database or create it if it doesn't exist
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Create a table to store face data if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS face_data (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE,
            name TEXT UNIQUE,
            age INTEGER,
            occupation TEXT,
            face_encoding TEXT,
            image_path TEXT
        )
    ''')

    # Save the changes and close the connection
    conn.commit()
    conn.close()

def encode_image(image_path):
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)

    if len(face_encodings) > 0:
        return face_encodings[0]  # Only encode the first face found in the image
    else:
        return None
    
def str_to_float_tuple(face_encoding_str):
    face_encoding_str = face_encoding_str.replace('\n', '').strip('[]')
    face_encoding_list = [float(val) for val in face_encoding_str.split()]
    face_encoding = tuple(face_encoding_list)
    return face_encoding

def load_known_face_encodings():
    try:
        # Connect to the database
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Load all the face encodings from the database
        cursor.execute('SELECT face_encoding FROM face_data')
        rows = cursor.fetchall()
        for row in rows:
            face_encoding_str = row[0]
            face_encoding = str_to_float_tuple(face_encoding_str)
            known_face_encodings.append(face_encoding)

        # Close the connection
        conn.close()

    except sqlite3.Error as e:
        print("Error while loading known face encodings:", e)

def check_existing_data(email, name, face_encoding, image_path):
    try:
        # Connect to the database
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Check if the email, name, face encoding, or image path already exists in the database
        cursor.execute('''
            SELECT * FROM face_data WHERE email=? OR name=? OR face_encoding=? OR image_path=?
        ''', (email, name, face_encoding, image_path))

        existing_data = cursor.fetchone()

        # Close the connection
        conn.close()

        return existing_data

    except sqlite3.Error as e:
        print("Error while checking existing data:", e)
        return None


def insert_data(email, name, age, occupation, face_encoding, image_path):
    try:
        # Check if the data already exists
        existing_data = check_existing_data(email, name, face_encoding, image_path)
        if existing_data:
            print("Data already exists in the database. Skipping insertion.")
            return

        # Connect to the database
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Insert data into the table
        cursor.execute('''
            INSERT INTO face_data (email, name, age, occupation, face_encoding, image_path)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (email, name, age, occupation, face_encoding, image_path))

        # Save the changes and close the connection
        conn.commit()
        conn.close()

        print("Data inserted successfully!")

    except sqlite3.Error as e:
        print("Error while inserting data:", e)

def main():
    create_database()
    load_known_face_encodings()

    # Sample data to insert (replace this with actual data and image paths)
    data = [
        {
            "email": "toluwaniojof@gmail.com",
            "name": "Ojo Toluwani",
            "age": 20,
            "occupation": "Engineer",
            "image_paths": ["Known_Faces/Tolu2.jpg", "Known_Faces/tolu_3.jpeg"]
        },
        {
            "email": "john.doe@yahoo.com",
            "name": "Balogs Olamlams",
            "age": 25,
            "occupation": "Software Engineer",
            "image_paths": ["Known_Faces/Ola.jpg", "Known_Faces/Ola2.jpg"]
        },
        {
            "email": "adisadavid@gmail.com",
            "name": "Adisa David",
            "age": 6,
            "occupation": "Data Analyst",
            "image_paths": ["Known_Faces/david_1.jpeg", "Known_Faces/david_2.jpeg", "Known_Faces/david_3.jpeg"]
        },
        {
            "email": "somthingif@gmail.com",
            "name": "Something Oluwaife",
            "age": 15,
            "occupation": "Programmer",
            "image_paths": ["Known_Faces/ife_1.jpeg", "Known_Faces/ife_2.jpeg"]
        },
        {
            "email": "mujeebbalogun24@gmail.com",
            "name": "Gbolahan Kayode",
            "age": 188,
            "occupation": "Billionaire",
            
            "image_paths": ["Known_Faces/Olamide.jpg", "Known_Faces/ife_2.jpeg"]
        }
    ]
 

    for item in data:
        email = item["email"]
        name = item["name"]
        age = item["age"]
        occupation = item["occupation"]
        image_paths = item["image_paths"]

        for image_path in image_paths:
            face_encoding = encode_image(image_path)
            if face_encoding is not None:
                # Check if the face encoding is already in the database
                face_encoding_np = np.array(face_encoding)
                if not any(np.array_equal(face_encoding_np, known_encoding) for known_encoding in known_face_encodings):
                    insert_data(email, name, age, occupation, str(face_encoding), image_path)
                    known_face_encodings.append(face_encoding_np)
                else:
                    print(f"Face encoding already exists in the database for image: {image_path}")
            else:
                print(f"Error: No face found in the image: {image_path}")


if __name__ == "__main__":
    main()





