import cv2
import numpy as np
 
logo = cv2.imread('icono-opencv.png', cv2.IMREAD_UNCHANGED)
minilogo = cv2.resize(logo, None, fx=0.34, fy=0.3)
cap = cv2.VideoCapture(0)

while True:
    ret, background = cap.read()

    primerplano = background[:, :, 0:3]
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

    cv2.imshow('MEZCLA',background)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()