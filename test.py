import pyvirtualcam
import numpy as np
import cv2 as cv

# Classify face very X frames
CLASSEVERY = 10
# Send to virtual camera (1) or display using CV (0) 
DISPLAY = 1

# Set up webcam capture
vc = cv.VideoCapture(1)

# Load the cascade
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

# Counter
count = 0

# Initialise face variable
faces = []

with pyvirtualcam.Camera(width = 1920, height = 1080, fps = 30) as cam:
    print(f'Using virtual camera: {cam.device}')
    while True:
        # Read frame from webcam
        ret, frame = vc.read()
        if not ret:
            raise RunTimeError('Error fetching frame')

        # Update count
        count += 1

        # Run face classifier:
        if count == CLASSEVERY:
            # Reset count
            count = 0

            # Convert into greyscale 
            # for the face classifier
            frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            # Detect the faces
            faces = face_cascade.detectMultiScale(frame_gray, 1.1, 4)

        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        if DISPLAY == 1:
            # Use the virtual camera

            # Convert into RGB 
            # since OpenCV uses BRG 
            frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            # Send to virtual camera
            cam.send(frame_rgb)
            cam.sleep_until_next_frame()
        else:
            # Send to CV display
            cv.imshow('img', frame)

            # Stop if escape key is pressed
            k = cv.waitKey(30) & 0xff
            if k == 27:
                break

vc.release()