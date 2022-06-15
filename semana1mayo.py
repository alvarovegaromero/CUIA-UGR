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
            bboxs, ids, rechazados = aruco.detectMarkers(gris, DICCIONARIO)        
            for bbox in bboxs: #para cada conjunto de vertices de los encontrados
                cv2.cornerSubPix(gris, bbox, winSize=(3,3), zeroZone=(-1,-1), criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.0001)) #Afinar vertices dados
                #winsize y zerozone es terreno a jugar para afinar vertice. Criteria condicion de salida
                #cornerSubPix para afinado de vertices 
            
            rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(bboxs, 0.193, matrix, camara.distCoeffs) 
            #para cada marcados, devuelveme esta info. número es tamaño en mundo real
            #rvec y tvecs son rotacion y traslacion respecto al centro del marcador. Son metros
            if rvecs is not None: #si ha detectado algo
                for i in range(len(rvecs)):
                    frame = cv2.drawFrameAxes(frame, matrix, camara.distCoeffs, rvecs[i], tvecs[i], 0.1) 
                    #poner ejes de coordenadas dado marcador detectado. 0.1 es longitud en metrox de los ejes
                    distancia = int(100*np.linalg.norm(np.array(tvecs[i]), ord=2)) #distancia al marcador
                    #print(distancia)
                    coord, _ = cv2.projectPoints(np.array([[0.0,0.0,0.0]]), rvecs[i], tvecs[i], matrix, camara.distCoeffs ) 
                    #convierte coordenadas xyz en coordenadas xy de la pantalla

                    cv2.circle(frame, coord[0][0].astype(int), 10, (0,255,255), -1)
                    


            cv2.imshow('WEBCAM', frame)
            if cv2.waitKey(1) == ord('q'):
                salir = True

    cap.release()
    cv2.destroyWindow('WEBCAM')