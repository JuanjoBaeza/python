import cv2
import face_recognition
import os
import numpy as np
import sys
from tkinter import Tk, messagebox

# Directorio con imágenes conocidas
known_faces_dir = "C:\\Repo\\python\\face_recognition\\known_people"

# Cargar imágenes conocidas y sus codificaciones
known_faces = []
known_names = []

# Recorrer el directorio y cargar cada imagen
for file_name in os.listdir(known_faces_dir):
    if file_name.endswith(('.jpg', '.png', '.jpeg')):
        # Cargar la imagen
        image_path = os.path.join(known_faces_dir, file_name)
        image = face_recognition.load_image_file(image_path)

        # Obtener las codificaciones de los rostros en la imagen
        try:
            encoding = face_recognition.face_encodings(image)[0]
            known_faces.append(encoding)
            known_names.append(file_name.split('.')[0])  # Usar el nombre del archivo sin extensión
        except IndexError:
            print(f"Advertencia: No se encontraron rostros claros en la imagen {file_name}")

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Función para mostrar una alerta emergente
def show_alert(name):
    root = Tk()
    root.withdraw()  # Oculta la ventana principal
    messagebox.showinfo("Alerta de Coincidencia", f"¡Coincidencia encontrada con {name}!")
    root.destroy()

video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    name = "persona"
   
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    # Detectar ubicaciones y codificaciones de rostros en el frame actual
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Display the resulting frame
    cv2.imshow('Video', frame)
    
    # Comparar cada cara capturada con las caras conocidas
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        face_distances = face_recognition.face_distance(known_faces, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_names[best_match_index]
            print("Found {0} faces!".format(len(faces)))
            show_alert(name)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()