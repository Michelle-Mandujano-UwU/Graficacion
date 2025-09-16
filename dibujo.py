import cv2 as cv
import numpy as np

# Crear fondo gris
img = np.ones((500,500,3), np.uint8) * 200  

# Monitor (rectángulo grande)
cv.rectangle(img, (100,80), (400,250), (50,50,50), -1)   # pantalla
cv.rectangle(img, (120,100), (380,230), (0,0,0), -1)     # parte negra de la pantalla

# Base del monitor
cv.rectangle(img, (220,250), (280,300), (80,80,80), -1)  # soporte
cv.rectangle(img, (180,300), (320,320), (100,100,100), -1)  # base

# CPU (torre)
cv.rectangle(img, (50,180), (90,350), (70,70,70), -1)    # torre
cv.circle(img, (70,200), 8, (0,0,255), -1)               # botón de encendido
cv.rectangle(img, (55,220), (85,230), (0,0,255), -1)     # entrada CD

# Teclado
cv.rectangle(img, (120,350), (380,400), (60,60,60), -1)  # teclado
cv.line(img, (120,370), (380,370), (255,255,255), 1)     # división teclas
cv.line(img, (120,385), (380,385), (255,255,255), 1)

# Mouse
cv.rectangle(img, (400,360), (430,390), (80,80,80), -1)  # mouse base
cv.line(img, (415,360), (415,390), (0,0,0), 1)           # división click


cv.imshow("img", img)
cv.waitKey(0)
cv.destroyAllWindows()
