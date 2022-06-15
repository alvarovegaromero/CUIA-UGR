from ast import AsyncWith
import cv2
import numpy as np
import time

capcam = cv2.VideoCapture(0)
cap = cv2.VideoCapture("video10s.mp4")
ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter('video10sresize.mp4', (ancho, alto))
 
while True:
    ret, frame = cap.read()
    if ret == True:
        b = cv2.resize(frame,(ancho,alto))
        out.write(b)
    else:
        break
    
cap.release()
out.release()
cv2.destroyAllWindows()