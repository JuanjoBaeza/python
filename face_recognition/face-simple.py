# https://realpython.com/traditional-face-detection-python/

import cv2
import sys

# Read image from your local file system
original_image = cv2.imread('known_people/tonto2.webp')

# Convert color image to grayscale for Viola-Jones
grayscale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

# Load the classifier and create a cascade object for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

detected_faces = face_cascade.detectMultiScale(grayscale_image)
name = 'Una cara'

for (column, row, width, height) in detected_faces:
    cv2.rectangle(
        original_image,
        (column, row),
        (column + width, row + height),
        (0, 255, 0),
        2
    )
    cv2.putText(original_image, name, (column, row-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

cv2.imshow('Image', original_image)
cv2.waitKey(0)
cv2.destroyAllWindows()