import cv2
import numpy as np
lena = cv2.imread('lena.tif')
opencv = cv2.imread('icono-opencv.png', cv2.IMREAD_UNCHANGED)

fondo = lena
hfondo, wfondo, _ = fondo.shape #alto, ancho y numero de canalesde la imagen fondo
primerplano = opencv[:, :, 0:3]
hprimerplano, wprimerplano, _ = primerplano.shape

x = wfondo//2 - wprimerplano//2 # para centrarlo, esquina izq y arriba de opencv
y = hfondo//2 - hprimerplano//2 # es division entera
                                #hemos despreciado canal alfa - png
                                # no solo cambiar -> combinar

mezcla = fondo
mezcla[y:y+hprimerplano, x:x+wprimerplano] = primerplano #submatriz del centro, cambiala por la de opencv

cv2.imshow('MEZCLA', mezcla)
cv2.waitKey()
cv2.destroyAllWindows()
