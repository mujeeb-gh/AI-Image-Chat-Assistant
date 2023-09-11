import cv2 as cv
import numpy as np

# Our sketch generating function
def sketch(image):
  # Convert image to grayscale
  img_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
  
  # Clean up image using Gaussian Blur
  img_gray_blur = cv.GaussianBlur(img_gray, (3, 3), 0)
  
  # Extract edges
  canny = cv.Canny(img_gray_blur, 10, 70)
  #Do an invert binarize the image
  ret, mask = cv.threshold(canny, 70, 255, cv.THRESH_BINARY_INV)
  return mask

capture = cv.VideoCapture(0)

while True:
  ret, frame = capture.read()
  cv.imshow("Live Sketcher", sketch(frame))
  if cv.waitKey(1) == 13: #13 is the enter key
    break
  
capture.release()
cv.destroyAllWindows()

