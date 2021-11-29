import pyvirtualcam
import numpy as np
import cv2 as cv

# Set up webcam capture
vc = cv.VideoCapture(1)

with pyvirtualcam.Camera(width = 1920, height = 1080, fps = 30) as cam:
	print(f'Using virtual camera: {cam.device}')
	while True:
		# Read frame from webcam
		ret, frame = vc.read()
		if not ret:
			raise RunTimeError('Error fetching frame')

		# Convert into RGB 
		# since OpenCV uses BRG 
		frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

		# Send the frame to the virtual camera and wait until the next frame
		cam.send(frame_rgb)
		cam.sleep_until_next_frame()

vc.release()