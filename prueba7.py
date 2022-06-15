import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se puede abrir la cámara")
    exit()
    
while True:
    ret, frame = cap.read()

    if not ret:
        print("No he podido leer el frame")
        break # Procesado de imágenes aquí

    cv2.imshow('WEBCAM', frame)

    if cv2.waitKey(1) == ord(' '):
        break

cap.release()
cv2.destroyWindow('WEBCAM')
