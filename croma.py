import cv2
import numpy as np
from matplotlib import pyplot as plt

lena = cv2.imread('lena.tif')

def eventoraton(evento, x, y, flags, params):
    if evento == cv2.EVENT_LBUTTONUP:
        print("H: ", framehsv[y, x, 0])
        print("S: ", framehsv[y, x, 1])
        print("V: ", framehsv[y, x, 2])

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print ("No se puede abrir la cámara.")
else:
    ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fondo = cv2.resize(lena, (ancho, alto))

    cv2.namedWindow("WEBCAM")
    cv2.setMouseCallback("WEBCAM", eventoraton)
    salir = False
    while not salir:
        ret, framebgr = cap.read()
        if not ret:
            print("No se ha podido leer el frame.")
            salir = True
        else:
            # Aquí se procesa el frame
            framehsv = cv2.cvtColor(framebgr, cv2.COLOR_BGR2HSV)

            mbg = cv2.inRange(framehsv, (35, 70, 70), (55, 255, 255))
            mascarabg = cv2.merge((mbg, mbg, mbg))
            mascarabg = cv2.GaussianBlur(mascarabg, (7, 7), 0)
            mascarafg = cv2.bitwise_not(mascarabg)
            fg = cv2.bitwise_and(framebgr, mascarafg)
            bg = cv2.bitwise_and(fondo, mascarabg)
            frame = cv2.bitwise_or(fg, bg)

            cv2.imshow('WEBCAM', frame)
            if cv2.waitKey(1) == ord(' '):
                salir = True

cap.release()
cv2.destroyWindow('WEBCAM')

#aparezca video debajo en bucle
#nos faltaria saber como hacer bucle y encajar frames de video con los de webcam
#y video mas corto para probar croma

#si te aburres pones "mosca" de opencv
