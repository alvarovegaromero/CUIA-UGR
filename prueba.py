import cv2
import numpy as np
rgb = np.random.randint(255, size=(250,250,3), dtype=np.uint8)
cv2.imshow('TEST', rgb)
cv2.waitKey()
cv2.destroyWindow('TEST')
