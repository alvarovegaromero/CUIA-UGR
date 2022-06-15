import cv2
import numpy as np
import camara

haar_cara = cv2.CascadeClassifier("Recursos\haarcascade_frontalface_default.xml")
haar_ojo = cv2.CascadeClassifier("Recursos\haarcascade_eye.xml")
haar_sonrisa = cv2.CascadeClassifier("Recursos\haarcascade_smile.xml")

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
            
            caras = haar_cara.detectMultiScale(gris, 1.2, 5) 
            for cx, cy, cw, ch in caras:
                frame = cv2.rectangle(frame, (cx, cy), (cx+cw, cy+ch), (255,0,0), 2)

                ojos = haar_ojo.detectMultiScale(gris[cy:cy+ch, cx:cx+cw], 1.1, 2, minSize=(30,30))
                for ox, oy, ow, oh in ojos:
                    frame = cv2.circle(frame, (cx+ox+ow//2, cy+oy+oh//2), (ow+oh)//4, (0,255,0), 2)

                sonrisas = haar_sonrisa.detectMultiScale(gris[cy:cy+ch, cx:cx+cw], 1.1, 2, minSize=(30,30))
                for sx, sy, sw, sh in sonrisas:
                    frame = cv2.rectangle(frame, (cx+sx, cy+sy), (cx+sx+sw, cy+sy+sh), (0,0,0), 2)

            cv2.imshow('WEBCAM', frame)
            if cv2.waitKey(1) == ord('q'):
                salir = True

    cap.release()
    cv2.destroyWindow('WEBCAM')