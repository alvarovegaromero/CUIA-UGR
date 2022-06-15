import cv2
import numpy as np
import camara

cap = cv2.VideoCapture(0)
lena = cv2.imread("lena.tif")
lenah, lenaw, _ = lena.shape
lenagris = cv2.cvtColor(lena, cv2.COLOR_BGR2GRAY)

detectorPC = cv2.SIFT_create() #genera puntos clave y descriptores
bf_matcher = cv2.BFMatcher() #Fuerza Bruta


FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=100)
flann_matcher = cv2.FlannBasedMatcher(index_params, search_params)


PClena = detectorPC.detect(lenagris)
PClena, DESClena = detectorPC.compute(lenagris, PClena)

lena = cv2.drawKeypoints(lena, PClena, lena, color=(0,255,255), flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

cv2.imshow("CUIA", lena)

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
            framerecortado = framerectificado[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
            frame = framerecortado
            hframe = roi_y
            wframe = roi_x

            gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #frame a escala de grises para busqueda de marcadores
            
            PCCam = detectorPC.detect(gris)
            PCCam, DESCCam, = detectorPC.compute(gris, PCCam)

            #frame = cv2.drawKeypoints(frame, PCCam, frame, color=(0,255,255), flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

            #coincidencias = bf_matcher.match(DESClena, DESCCam)
            #coincidencias = bf_matcher.knnMatch(DESClena, DESCCam, k=2)
            coincidencias = flann_matcher.knnMatch(DESClena, DESCCam, k=2)

            #coincidencias = sorted(coincidencias, key=lambda x: x.distance)
            good = []
            for c1, c2 in coincidencias:
                if c1.distance < 0.7*c2.distance: #distancia = semejanza entre descriptores
                    good.append(c1)

            if len(good) > 4:
                origen = []
                destino = []

                for k in good:
                    punto = PClena[k[0].queryIdx].pt
                    punto = list(punto).append(0)

                    origen.append(punto)
                    punto = PCCam[k[0].queryIdx].pt
                    destino.append(list(punto))

            det, rvec, tvec, inliers = cv2.solvePnP(np.array([origen]), np.array([destino]), camara.cameraMatrix, camara.distCoeffs)

            if ret: #refinado
                rvec, tvec = cv2.solvePnP(np.array([origen]), np.array([destino]), camara.cameraMatrix, camara.distCoeffs, rvec, tvec)


            #frame = cv2.drawMatches(lena, PClena, frame, PCCam, coincidencias[:20], frame, flags = cv2.DRAW_MATCHES_FLAGS_DEFAULT)
            frame = cv2.drawMatches(lena, PClena, frame, PCCam, good, frame, flags = cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

            cv2.imshow('WEBCAM', frame)
            if cv2.waitKey(1) == ord('q'):
                salir = True

    cap.release()
    cv2.destroyWindow('WEBCAM')


