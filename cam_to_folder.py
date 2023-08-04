import cv2
import os
import uuid

def capture_and_save_image(name):
    # Open the default camera (usually the webcam)
    cap = cv2.VideoCapture(0)

    # Set the camera resolution to 250x250
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 250)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 250)

    # Loop until the user presses the 'b' key
    while True:
        ret, frame = cap.read()
        frame = frame[120:120+250,200:200+250, :]

        # Display the video stream in a window
        cv2.imshow('Capture Image', frame)

        # Wait for the user to press a key (maximum delay of 10 milliseconds)
        key = cv2.waitKey(10)

        # If the user presses the 'b' key (ASCII value 98), save the image and exit the loop
        if key == 98:
            # Convert the image to greyscale
            grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Save the greyscale image to the "Known_Faces" folder with the provided name
            filename = os.path.join('Known_Faces', f'{name}', f'{uuid.uuid1()}.jpg')
            cv2.imwrite(filename, grey_frame)

            print(f"Image saved as {filename}")
        elif key == 113:
            break

    # Release the camera and close the OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

def main():
    # Prompt the user for their name
    name = input("Enter your name: ")

    # Create the "Known_Faces" folder if it doesn't exist
    if not os.path.exists(f'Known_Faces/{name}'):
        os.mkdir(f'Known_Faces/{name}')

    # Capture and save the image
    capture_and_save_image(name)

if __name__ == "__main__":
    main()
