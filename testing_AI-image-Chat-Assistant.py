import cv2
import face_recognition

def get_face_embeddings(image_path):
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)

    if len(face_encodings) > 0:
        return face_encodings[0]  # Return the first face encoding (assumes one face per image)
    else:
        return None

def compare_faces(known_face_encoding, unknown_face_encoding):
    # Compute the Euclidean distance between the two face embeddings
    similarity_score = face_recognition.face_distance([known_face_encoding], unknown_face_encoding)[0]

    # Normalize the similarity score to a range between 0.3 and 0.8
    normalized_confidence = 0.3 + (similarity_score - 0) * (0.8 - 0.3) / (1 - 0)

    return normalized_confidence

def main():
    # Load known face embedding
    known_image_path = "Known_Faces/Tolu2.jpg"
    known_face_encoding = get_face_embeddings(known_image_path)
    if known_face_encoding is None:
        print("No face detected in the known image.")
        return

    # Start webcam capture
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame.")
            break

        # Get face encoding of the current frame
        face_locations = face_recognition.face_locations(frame)
        if len(face_locations) > 0:
            face_encoding = face_recognition.face_encodings(frame, face_locations)[0]

            # Compare faces
            confidence = compare_faces(known_face_encoding, face_encoding)
            print(f"Confidence: {confidence:.2f}")

            # Draw rectangle and confidence level on the frame
            top, right, bottom, left = face_locations[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, f"Confidence: {confidence:.2f}", (left, bottom + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Show the frame
        cv2.imshow("Webcam", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()







# import cv2 as cv
# import face_recognition

# face_classifier = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

# def get_face_embeddings(image_path):
#     image = face_recognition.load_image_file(image_path)
#     face_encodings = face_recognition.face_encodings(image)

#     if len(face_encodings) > 0:
#         return face_encodings[0]  # Return the first face encoding (assumes one face per image)
#     else:
#         return None

# def compare_faces(known_face_encoding, unknown_face_encoding):
#     # Compute the Euclidean distance between the two face embeddings
#     return face_recognition.face_distance([known_face_encoding], unknown_face_encoding)[0]
  
# def similarity_to_percentage(similarity_score):
#   return (1 - similarity_score)* 100

# def face_extractor(img) :
#   # Function detects face and returns the cropped face
#   # if no face is found, it returns the input image
#     gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
#     faces = face_classifier.detectMultiScale(gray, 1.3, 5)
#     if len(faces) == 0 :
#         return None
#     #crop all faces found
#     for (x,y,w,h) in faces :
#         cropped_face = img[y : y + h, x : x + w]
#     return cropped_face



# def main():
#     known_image_path = "Known_Faces/Tolu2.jpg"
#     known = cv.imread(known_image_path)
    
#     #Get second image with 
#     # global frame
#     cap = cv.VideoCapture(0)
  
#     while True:
#         ret, frame = cap.read()
#         # if not ret:
#         #     print("Failed to grab frame")
#         #     break
        
        
#         if face_extractor(frame) is not None :
#             face = cv.resize(face_extractor(frame), (200, 200))
#             face = cv.cvtColor(face, cv.COLOR_BGR2GRAY)
#             unknown_image_path = f"Unknown_Faces/face.jpg"
#             cv.imwrite(unknown_image_path, face) 
#         else:
#             print("\n Face not found \n")
#             break
        
        
#         # Load known and unknown face embeddings
#         known_face_encoding = get_face_embeddings(known_image_path)
#         if known_face_encoding is None:
#             print("No face detected in the known image.")
#             return

#         unknown_face_encoding = get_face_embeddings(unknown_image_path)
#         if unknown_face_encoding is None:
#             print("No face detected in the unknown image.")
#             return

#         # Compare faces
#         similarity_score = compare_faces(known_face_encoding, unknown_face_encoding)
#         similarity_percentage = similarity_to_percentage(similarity_score= similarity_score)
#         print(f"Similarity percentage: {similarity_percentage:.2f}%")

#         # Define a threshold to consider faces similar or not
#         similarity_threshold = 60
#         if similarity_percentage >= similarity_threshold:
#             print("The faces are similar.")
#         else:
#             print("The faces are not similar.")
        
#         cv.imshow("Known_Faces", known)
#         cv.putText(frame, f"Similarity Percentage: {similarity_percentage:.2f}%", (50,50), cv.FONT_HERSHEY_COMPLEX, 1.0, (255,0,255), 2)
#         cv.imshow("Unknown Face", frame)
#         break
    
    
    
#     cv.waitKey(0)
#     cap.release()
#     cv.destroyAllWindows() 
    
# # # display = cv.imread(frame)
# # cv.imshow("Testing Face", frame) 

# if __name__ == "__main__":
#   main()

