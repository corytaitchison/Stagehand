import pyvirtualcam
import numpy as np
import cv2 as cv

# Classify face very X frames
CLASSEVERY = 2
# Send to virtual camera (1) or display using CV (0) 
DISPLAY = 1
# Camera width
WIDTH, HEIGHT = 1920, 1080
# Crop Ratio
CROP = 1.5

#################

# Set up webcam capture
vc = cv.VideoCapture(1)

# Load the cascade
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

# Counter
count = CLASSEVERY - 1

# Initialise face variable
face = [0, 0, 0, 0]

# Calculate cropped dimensions
c_width = int(round(0.5 * WIDTH / CROP)) * 2
c_height = int(round(0.5 * HEIGHT / CROP)) * 2

with pyvirtualcam.Camera(width = WIDTH, height = HEIGHT, fps = 30) as cam:
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
            faces = face_cascade.detectMultiScale(frame_gray, 2, 4)

            # Get the widest detected face
            if len(faces) != 0:
                i = np.argmax(faces[:,2])
                face = faces[i,:]

                # Convert to the desired crop ratio
                (x, y, w, h) = face
                centre = [int(round(x + w / 2)), int(round(y + h / 2))]
                face = [centre[0] - c_width//2, centre[1] - c_height//2, c_width, c_height]

        # # Draw the rectangle around each face
        # (x, y, w, h) = face
        # cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Crop to face
        (x, y, w, h) = face
        if w == 0:
            frame_crop = frame 
        else:
            frame_crop = frame[y:(y+h), x:(x+w)]

        # Send to display 
        if DISPLAY == 1:
            # Use the virtual camera

            # Convert into RGB since OpenCV uses BRG 
            # and resize to fit the virtual camera size
            frame_rgb = cv.resize(cv.cvtColor(frame_crop, cv.COLOR_BGR2RGB), (WIDTH, HEIGHT))

            # Send to virtual camera
            cam.send(frame_rgb)
            cam.sleep_until_next_frame()
        else:
            # Send to CV display
            cv.imshow('Stagehand', frame_crop)

            # Stop if escape key is pressed
            k = cv.waitKey(30) & 0xff
            if k == 27:
                break

vc.release()