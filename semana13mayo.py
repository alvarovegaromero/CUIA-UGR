import cv2
import numpy as np
import camara

#frame = cv2.imread("lena.tif")
#frame = cv2.imread("figuras.jpg")
frame = cv2.imread("billar.jpeg")

gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, cv2.COLOR_BGR2GRAY)

#_, umbral = cv2.threshold(gris, 200, 255, cv2.THRESH_BINARY) #Cualquier pixel con escala de grises entre 200 y 255, ponlos a 255, y los de debajo a 0
_, umbral = cv2.threshold(gris, 100, 255, cv2.THRESH_BINARY) #Cualquier pixel con escala de grises entre 200 y 255, ponlos a 255, y los de debajo a 0

circulos = cv2.HoughCircles(umbral, cv2.HOUGH_GRADIENT, dp=1.5, minDist=100, param1=50, param2=30, minRadius=10, maxRadius=100 )

circulos = circulos.astype(int)

if circulos is not None:
    for c in circulos[0]:
        x, y, r = c
        cv2.circle(frame, (x,y), r, (0,0,255), 2)
        

""" Todo esto y lo de abajo lo hicimos con las figuras - Contornos a las figuras
contornos, _ = cv2.findContours(umbral, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #Vector de contornos

for c in contornos:
   vertices = cv2.approxPolyDP(c, 0.009*cv2.arcLength(c, True), True)
    
   if len(vertices) == 5: #Los que tengan 5 lados
        cv2.drawContours(frame, [vertices], 0, (255,0,0),3) #dibujar contornos de azul

   #Rectangulo normal
    x, y, w, h = cv2.boundingRect(c) 
    cv2.rectangle(frame, (x,y), (x+w, y+h), (255,255,0), 2) #Meter figuras en un rectangulo
    
    #Rectangulo de area minima
    mar = cv2.minAreaRect(c)
    box = cv2.boxPoints(mar) #Lista de coordenadas de rectangulo minimo
    cv2.polylines(frame, [box.astype(int)], True, (0,0, 255), 2)

    #Encontrar ciruclo de area minima que lo contiene
    (x,y), r = cv2.minEnclosingCircle(c)
    x = int(x)
    y = int(y)
    r = int(r)
    cv2.circle(frame, (x,y), r, (255,0,255), 2)
"""

"""  Mejora sobre harris
corners = cv2.goodFeaturesToTrack(umbral, maxCorners=66, qualityLevel=0.001, minDistance=25, useHarrisDetector=True, k=0.01) #Mejora sobre harris

for c in corners:
        x = c[0][0].astype(int)
        y = c[0][1].astype(int)
        cv2.circle(frame, (x,y), 5, (0,255,0), 2) #Poner ciruclos en verde
"""

""" Usando algoritmo de Harris:
harris = cv2.cornerHarris(umbral, blockSize=5, ksize=15, k=0.01) #Paremtros de formula de harris - Quedarnos con 
harris = cv2.dilate(harris, None)
_, harris = cv2.threshold(harris, 0.01*harris.max(), 255, 0) #Todo lo que tenga valor de >1%, ponlo a 255. -> Todos los pixeles en alrededores de vertices se potencian
harris = np.uint8(harris) #Poner formato que conozca
_, _, _, centroides = cv2.connectedComponentsWithStats(harris) #Identificar grupos de pixeles conexos y dar estadisticas de ellos. Entre ellos, centroides

for c in centroides:
        x = c[0].astype(int)
        y = c[1].astype(int)
        cv2.circle(frame, (x,y), 5, (0,255,0), 2) #Poner ciruclos en verde
"""

cv2.imshow("Original", frame)
#cv2.imshow("IMAGEN", harris)
cv2.waitKey()
cv2.destroyAllWindows()