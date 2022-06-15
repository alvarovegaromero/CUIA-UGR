import cv2
from cv2 import aruco
import numpy as np
import time

DICCIONARIO = aruco.Dictionary_get(aruco.DICT_6X6_250)
charuco = aruco.CharucoBoard_create(6, 8, 0.03, 0.02, DICCIONARIO)

CPS = 1
allCorners = []
allIds = []
criterio = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)
tiempo = 1.0 / CPS

cap = cv2.VideoCapture(0)
if cap.isOpened():
    wframe = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    hframe = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    final = False
    n = 0
    antes = time.time()
    while not final:
        ret, frame = cap.read()
        if not ret:
            final = True
        else:
            if time.time()-antes > tiempo:
                antes = time.time()
                gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                bboxs, ids, rechazados = aruco.detectMarkers(gris, DICCIONARIO)
                bboxs, ids, _, _ = aruco.refineDetectedMarkers(gris, charuco, bboxs, ids, rechazados)

                if ids is not None:
                    for bbox in bboxs:
                        cv2.cornerSubPix(gris, bbox, winSize = (3,3), zeroZone = (-1,-1), criteria = criterio)
                    num, bboxsInt, idsInt = aruco.interpolateCornersCharuco(bboxs, ids, gris, charuco)
                    if num>=8 and bboxsInt is not None and idsInt is not None:
                        aruco.drawDetectedMarkers(frame, bboxs)
                        allCorners.append(bboxsInt)
                        allIds.append(idsInt)
                        n = n + 1
            cv2.putText(frame, str(n), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))
            cv2.imshow("WEBCAM", frame)
            if cv2.waitKey(5) == ord(' '):
                final = True
    cap.release()
    cv2.destroyAllWindows()
    print("Espera mientras calculo los resultados de calibración de la cámara...")

    cameraMatrixInt = np.array([[ 1000,    0, hframe/2],
                                [    0, 1000, wframe/2],
                                [    0,    0,        1]])
    distCoeffsInt = np.zeros((5, 1))
    flags = (cv2.CALIB_USE_INTRINSIC_GUESS + cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_FIX_ASPECT_RATIO)
    (ret, cameraMatrix, distCoeffs, rvec, tvec, stdInt, stdExt, errores) = aruco.calibrateCameraCharucoExtended(charucoCorners=allCorners,
                                                                                                              charucoIds=allIds,
                                                                                                              board=charuco,
                                                                                                              imageSize=(hframe, wframe),
                                                                                                              cameraMatrix=cameraMatrixInt,
                                                                                                              distCoeffs=distCoeffsInt,
                                                                                                              flags=flags,
                                                                                                              criteria=(cv2.TERM_CRITERIA_EPS & cv2.TERM_CRITERIA_COUNT, 10000, 1e-9))

    print("Error:", ret)

    with open('camara.py', 'w') as fichero:
        fichero.write("import numpy as np\n")
        fichero.write("cameraMatrix = np.")
        fichero.write(repr(cameraMatrix))
        fichero.write("\ndistCoeffs = np.")
        fichero.write(repr(distCoeffs))
        fichero.close()
        print("Los resultados de calibración se han guardado en el fichero camara.py")
else:
    print("No se pudo abrir la cámara")
