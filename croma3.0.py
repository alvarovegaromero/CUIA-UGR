import cv2
import numpy as np
from matplotlib import pyplot as plt

logo = cv2.imread('icono-opencv.png', cv2.IMREAD_UNCHANGED)
minilogo = cv2.resize(logo, None, fx=0.34, fy=0.3)

cap = cv2.VideoCapture(0)

video = cv2.VideoCapture("video10s.mp4")  #lmread pero para video
fps = video.get(cv2.CAP_PROP_FPS)
numframes = video.get(cv2.CAP_PROP_FRAME_COUNT)

def eventoraton(evento, x, y, flags, params):
    if evento == cv2.EVENT_LBUTTONUP:
        print("H: ", framehsv[y, x, 0])
        print("S: ", framehsv[y, x, 1])
        print("V: ", framehsv[y, x, 2])

if not cap.isOpened():
    print ("No se puede abrir la cámara.")
else:
    if not video.isOpened(): #buena idea hacerlo antes de las 3 lineas anteriores - más trat de errpres
        print("No se puede abrir el fichero")

    else:
        cv2.namedWindow("WEBCAM")
        cv2.setMouseCallback("WEBCAM", eventoraton)
        salir = False
        contadorvideo = 0
        while not salir:
            ret, framebgr = cap.read()
            retvideo, framevideo = video.read() #leer video. Tratamos cada frame como una imagen

            ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fondo = cv2.resize(framevideo, (ancho, alto))

            contadorvideo+=1

            if(contadorvideo == video.get(cv2.CAP_PROP_FRAME_COUNT)): #Para poner video en bucle
                contadorvideo = 0
                video.set(cv2.CAP_PROP_POS_FRAMES, 0)

            if not ret or not retvideo:
                print("No se ha podido leer el frame.")
                salir = True
            else:
                # Aquí se procesa el frame
                framehsv = cv2.cvtColor(framebgr, cv2.COLOR_BGR2HSV)

                mbg = cv2.inRange(framehsv, (90, 150, 70), (140, 255, 255))
                mascarabg = cv2.merge((mbg, mbg, mbg))
                mascarabg = cv2.GaussianBlur(mascarabg, (7, 7), 0)
                mascarafg = cv2.bitwise_not(mascarabg)
                fg = cv2.bitwise_and(framebgr, mascarafg)
                bg = cv2.bitwise_and(fondo, mascarabg)
                frame = cv2.bitwise_or(fg, bg)

                # Parte de "mosca" #############################################
                primerplano = frame[:, :, 0:3]
                hprimerplano, wprimerplano, _ = primerplano.shape
                minilog = minilogo[:, :, 0:3]
                hlogo, wlogo, _ = minilog.shape
                alfa = minilogo[:, :, 3]
                afla = 255 - alfa #inverso de alfa

                alfa = cv2.cvtColor(alfa, cv2.COLOR_GRAY2BGR) / 255 # ]0-1]
                afla = cv2.cvtColor(afla, cv2.COLOR_GRAY2BGR) / 255 # para usar alfa que sea de los 3 colores

                #x = wprimerplano//2 - wlogo//2
                #y = hprimerplano//2 - hlogo//2

                mezcla = primerplano

                #colocarlo en la esquina abajo a la derecha con un margen de 10 pixeles
                esquina_inferior = mezcla[hprimerplano-hlogo-10:hprimerplano-10,   wprimerplano-wlogo-10:wprimerplano-10]*afla + minilog*alfa
                mezcla[hprimerplano-hlogo-10:hprimerplano-10,   wprimerplano-wlogo-10:wprimerplano-10] = esquina_inferior

                #############################################

                cv2.imshow('WEBCAM', mezcla)
                if cv2.waitKey(1) == ord('q'):
                    salir = True

video.release()
cap.release()
cv2.destroyAllWindows()