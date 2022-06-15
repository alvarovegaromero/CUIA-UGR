import cv2
import numpy as np
lena = cv2.imread('lena.tif')
b, g, r = cv2.split(lena)
lena_grb = cv2.merge((g, r, b))
cv2.imshow('GRB', lena_grb)
cv2.waitKey()
cv2.destroyAllWindows()
