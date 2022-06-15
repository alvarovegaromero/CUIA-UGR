import cv2
import os
import numpy as np
from cv2 import aruco
import camara

DICCIONARIO = aruco.getPredefinedDictionary(aruco.DICT_5X5_50)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("No se puede abrir la camara")
else:
    hframe = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    wframe = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    matrix, roi = cv2.getOptimalNewCameraMatrix(camara.cameraMatrix, camara.distCoeffs, (wframe, hframe), 1, (wframe, hframe))
    #Calcular matrix optima y region de interes

    #Coordenada x e y de la zona sin banda negras, ancho y alto de la region de interes
    roi_x, roi_y, roi_w, roi_h = roi

    salir = False
    while not salir:
        ret, frame = cap.read()
        if not ret:
            print("No se ha podido leer el archivo")
            salir = True
        else:
            framerectificado = cv2.undistort(frame, camara.cameraMatrix, camara.distCoeffs, None, matrix)
            #Opcional - Recortar frame para que no haya bandas negras
            framerecortado = framerectificado[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
            frame = framerecortado
            hframe = roi_y
            wframe = roi_w

            gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #frame a escala de grises para busqueda de marcadores
            
            cv2.imshow('WEBCAM', frame)
            if cv2.waitKey(1) == ord('q'):
                salir = True

    cap.release()
    cv2.destroyWindow('WEBCAM')