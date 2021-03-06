import argparse
import pyvirtualcam
from spring import Spring
import numpy as np
import cv2 as cv

#############
# CONSTANTS #
#############

# Classify face very X frames
CLASSEVERY = 5
# Camera width
WIDTH, HEIGHT = 1920, 1080
# Vertical offset
VOFFSET = 60

#############
# ARGUMENTS #
#############
parser = argparse.ArgumentParser(
    description="Runs the Stagehand program to track facial position and crop the webcam."
)
parser.add_argument("--crop", type=float, default=1.2, help="Crop ratio (default: 1.2)")
parser.add_argument(
    "--display",
    choices=["virtual", "cv"],
    default="virtual",
    help="Output type (default: 'virtual')",
)
parser.add_argument(
    "-d", "--debug", action="store_true", help="Enable debugging ouput (default: false)"
)
parser.add_argument(
    "-a", "--auto", action="store_true", help="Auto adjust crop (default: false)"
)
parser.add_argument(
    "--k", type=float, default=0.5, help="Spring constant (default: 0.5)"
)
parser.add_argument(
    "--gamma", type=float, default=1, help="Damping coefficient (default: 1.0)"
)
args = parser.parse_args()

##############
# INITIALISE #
##############

# Set up webcam capture
vc = cv.VideoCapture(1)

# Load the cascade for face detection
face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")

# Counter for each frame loop
count = CLASSEVERY - 1

# Initialise face variable
face = [0, 0, 0, 0]

# Initialise spring to be at the centre of the screen
centre = np.array([WIDTH / 2, HEIGHT / 2])
sp = Spring(np.float64(centre), k=args.k, gamma=args.gamma)

# Initialise crop spring
csp = Spring(np.array([args.crop]), np.array([0.0]), k=args.k, gamma=args.gamma)


# Calculate initial cropped dimensions
def getWidthHeight(crop):
    """
    Calculate the width and height of the camera given a crop ratio.

    ARGUMENTS
    - crop: float64
    """
    c_width = int(round(0.5 * WIDTH / crop)) * 2
    c_height = int(round(0.5 * HEIGHT / crop)) * 2
    return (c_width, c_height)


c_width, c_height = getWidthHeight(args.crop)

##############
# FRAME LOOP #
##############
with pyvirtualcam.Camera(width=WIDTH, height=HEIGHT, fps=30) as cam:
    if args.debug:
        print(f"Using virtual camera: {cam.device}")
    while True:
        # Read frame from webcam
        ret, frame = vc.read()
        if not ret:
            raise RunTimeError("Error fetching frame")

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
                i = np.argmax(faces[:, 2])
                face = faces[i, :]

                # Convert to the desired crop ratio
                (x, y, w, h) = face
                centre = np.array([int(round(x + w / 2)), int(round(y + h / 2))])

                # Update the spring position
                sp.set_spring(np.float64(centre))

                # Update the crop factor
                if args.auto:
                    # factor = min([WIDTH / w, HEIGHT / h])
                    factor = WIDTH / (w * 3)
                    csp.set_spring(np.float64([factor]))

        # Recompute the ODE
        sp.update()

        # Get the smoothed position
        centre = sp.get_x()

        # Get crop ratio
        if args.auto:
            csp.update()
            crop = csp.get_x()
            c_width, c_height = getWidthHeight(crop[0])

        # Recalculate cropped boundaries, ensuring it doesn't exceed the edges of the video
        #   face = [x, y, w, h]
        face = [
            min(max(centre[0] - c_width // 2, 0), WIDTH - c_width),
            min(max(centre[1] - c_height // 2 - VOFFSET, 0), HEIGHT - c_height),
            c_width,
            c_height,
        ]

        # Crop to face if a face is detected
        (x, y, w, h) = face
        if w == 0:
            frame_crop = frame
        else:
            frame_crop = frame[y : (y + h), x : (x + w)]

        # Send to display
        if args.display == "virtual":
            # Use the virtual camera

            # Convert into RGB since OpenCV uses BRG
            # and resize to fit the virtual camera size
            frame_rgb = cv.resize(
                cv.cvtColor(frame_crop, cv.COLOR_BGR2RGB), (WIDTH, HEIGHT)
            )

            # Send to virtual camera
            cam.send(frame_rgb)
            cam.sleep_until_next_frame()
        else:
            # Send to CV display
            cv.imshow("Stagehand", frame_crop)

            # Stop if escape key is pressed
            k = cv.waitKey(30) & 0xFF
            if k == 27:
                break

# Release webcam
vc.release()
