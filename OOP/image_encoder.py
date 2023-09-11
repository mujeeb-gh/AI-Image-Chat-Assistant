import face_recognition

class ImageEncoder:
  @staticmethod
  def encode_image(image_path):
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)

    if len(face_encodings) > 0:
        return face_encodings[0]  # Only encode the first face found in the image
    else:
        return None