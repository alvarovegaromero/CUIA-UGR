import cv2
import numpy as np
import camara
import pafy

haar_cara = cv2.CascadeClassifier("Recursos\haarcascade_frontalface_default.xml")
haar_ojo = cv2.CascadeClassifier("Recursos\haarcascade_eye.xml")
haar_sonrisa = cv2.CascadeClassifier("Recursos\haarcascade_smile.xml")

youtube = pafy.new("https://www.youtube.com/watch?v=2_N7pSphUQU")
print(youtube.allstreams)
url = (youtube.allstreams[2]).url

cap = cv2.VideoCapture(url)
#cap = cv2.VideoCapture(0)
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
            
            caras = haar_cara.detectMultiScale(gris, 1.2, 5) 
            for cx, cy, cw, ch in caras:
                micara = cv2.resize(gris[cy:cy+ch, cx:cx+cw], (200,200))
                cv2.imwrite("micara.jpg", micara)


            cv2.imshow('WEBCAM', frame)
            if cv2.waitKey(1) == ord('q'):
                salir = True

    cap.release()
    cv2.destroyWindow('WEBCAM')