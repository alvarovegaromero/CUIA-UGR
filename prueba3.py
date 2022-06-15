import cv2
import numpy as np
#lena = cv2.imread('lena.tif')
opencv = cv2.imread('icono-opencv.png', cv2.IMREAD_UNCHANGED)
opencv_bgr = opencv[:, :, 0:3]
opencv_alfa = opencv[:, :, 3]
cv2.imshow('COLOR', opencv_bgr)
cv2.imshow('ALFA', opencv_alfa)
cv2.waitKey()
cv2.destroyAllWindows()
