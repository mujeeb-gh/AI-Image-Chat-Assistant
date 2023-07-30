import cv2 as cv
import numpy as np

# Load HHAR face classifier
face_classifier = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

def calculate_hog(image):
    # Create HOG descriptor
    hog = cv.HOGDescriptor()
    # Compute HOG features
    hog_features = hog.compute(image)
    return hog_features.flatten()

def calculate_similarity(feature1, feature2):
    # Calculate Euclidean distance between feature vectors
    distance = np.linalg.norm(feature1 - feature2)
    return distance


# Get Image 1 -- selfie to be uploaded
image1 = cv.imread("Faces\image1.jpg", cv.IMREAD_GRAYSCALE)



name = str(input("Enter your name: "))
def face_extractor(img) :
  # Function detects face and returns the cropped face
  # if no face is found, it returns the input image
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 0 :
        return None
    #crop all faces found
    for (x,y,w,h) in faces :
        cropped_face = img[y : y + h, x : x + w]
    return cropped_face


# Get Image 2
cap = cv.VideoCapture(0)

ret, frame = cap.read()
if face_extractor(frame) is not None :
    face = cv.resize(face_extractor(frame), (200, 200))
    face = cv.cvtColor(face, cv.COLOR_BGR2GRAY)
    file_name_path = f"Faces\\{name}2.jpg"
    cv.imwrite(file_name_path, face)  
    image2 = cv.imread(f"Faces\\{name}.jpg", cv.IMREAD_GRAYSCALE)

    # image1 = cv.resize(image1, (64, 128),  interpolation=cv.INTER_CUBIC)
    # image2 = cv.resize(image2, (64, 128),  interpolation=cv.INTER_CUBIC)
else :
    print("\n Face not found \n")
    pass
      
cv.waitKey(1) == 13
cap.release()
cv.destroyAllWindows()  

# Load and preprocess two images
cv.imshow(name, image2)


# Calculate HOG features for both images
hog_features1 = calculate_hog(image1)
hog_features2 = calculate_hog(image2)








cv.waitKey(0)

