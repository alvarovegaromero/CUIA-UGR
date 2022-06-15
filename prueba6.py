
import cv2
import numpy as np
import time

video = cv2.VideoCapture("video10s.mp4")  #lmread pero para video
fps = video.get(cv2.CAP_PROP_FPS)
numframes = video.get(cv2.CAP_PROP_FRAME_COUNT)

if not video.isOpened(): #buena idea hacerlo antes de las 3 lineas anteriores - más trat de errpres
    print("No se puede abrir el fichero")
    exit()
inicio = time.time()
while True:
    ret, frame = video.read() #frame leido y booleano si se ha podido leer
    intervalo = int(800/fps) #ejecuta a 25.8

    if not ret: #si es false
        print("No he podido leer el frame")
        break

    cv2.imshow('VIDEO', frame) # mostrarlo

    if cv2.waitKey(intervalo) == ord('q'):
        break
fin = time.time()
video.release()

print("FPS: ", fps)
print("Número de frames: ", numframes)
print("Duración: ", fin-inicio, " segundos")
print("FPS efectivos: ", numframes/(fin-inicio))


cv2.destroyWindow('VIDEO')

#hacer que video se reproduzca a los fps que dice - en cualquier video y ordenador

