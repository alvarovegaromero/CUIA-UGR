import cv2
import numpy as np
lena = cv2.imread('lena.tif')
opencv = cv2.imread('llama.png', cv2.IMREAD_UNCHANGED)

bg = lena
hbg, wbg, _ = bg.shape
fg = opencv[:, :, 0:3]
hfg, wfg, _ = fg.shape
alfa = opencv[:, :, 3]
afla = 255 - alfa #inverso de afla

alfa = cv2.cvtColor(alfa, cv2.COLOR_GRAY2BGR) / 255 # ]0-1]
afla = cv2.cvtColor(afla, cv2.COLOR_GRAY2BGR) / 255 # para usar alfa que sea de los 3 colores

x = wbg//2 - wfg//2
y = hbg//2 - hfg//2

mezcla = bg
mezcla[y:y+hfg, x:x+wfg] = mezcla[y:y+hfg, x:x+wfg]*afla + fg*alfa
#combinacion de alfa de la nueva y afla la antigua

cv2.imshow('MEZCLA', mezcla)
cv2.waitKey()
cv2.destroyAllWindows()

# si alfa es minimo, se ve el fondo (transparente), si es intermedio, mezcla y si no, lo original

#3 tarea: poner webcam y logotipo de opencv en una esquina
