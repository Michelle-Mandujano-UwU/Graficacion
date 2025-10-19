# este programa centra la imagen, la rota 90 grados, la escala x2 y al final le pone un filtro bilineal
import cv2 as cv
import numpy as np
import math

# abro la imagen en blanco y negro
imagen = cv.imread('filbili3.png', 0)

# saco el tamaño alto y ancho
alto, ancho = imagen.shape

# creo unos lienzos para ir guardando resultados
img_escalada = np.zeros((alto * 2, ancho * 2), dtype=np.uint8)
img_rotada = np.zeros((alto * 2, ancho * 2), dtype=np.uint8)
img_filtro_rotada = np.zeros((alto * 2, ancho * 2), dtype=np.uint8)

# centro original de la imagen
centro_x, centro_y = ancho // 2, alto // 2

# angulo para girar 90 grados
angulo = 90
radianes = math.radians(angulo)

# escalo la imagen al x2 centrada
for i in range(alto):
    for j in range(ancho):
        # lo muevo pa que quede centrado en la nueva imagen mas grande
        nuevo_y = int((i - alto / 2) * 2 + alto)
        nuevo_x = int((j - ancho / 2) * 2 + ancho)
        if 0 <= nuevo_x < ancho * 2 and 0 <= nuevo_y < alto * 2:
            img_escalada[nuevo_y, nuevo_x] = imagen[i, j]

# roto la imagen alrededor del centro
cx, cy = ancho, alto  # centro de la imagen escalada
for i in range(alto * 2):
    for j in range(ancho * 2):
        x_rel = j - cx
        y_rel = i - cy
        nuevo_x = int(cx + x_rel * math.cos(radianes) - y_rel * math.sin(radianes))
        nuevo_y = int(cy + x_rel * math.sin(radianes) + y_rel * math.cos(radianes))
        if 0 <= nuevo_x < ancho * 2 and 0 <= nuevo_y < alto * 2:
            img_rotada[nuevo_y, nuevo_x] = img_escalada[i, j]

# le paso un filtro bilineal
# básicamente suaviza tomando un promedio mas centrado
for i in range(1, (alto * 2) - 1):
    for j in range(1, (ancho * 2) - 1):
        # saco promedio con los 4 de alrededor
        a = int(img_rotada[i, j])
        b = int(img_rotada[i + 1, j])
        c = int(img_rotada[i, j + 1])
        d = int(img_rotada[i + 1, j + 1])
        prom = (a + b + c + d) / 4
        img_filtro_rotada[i, j] = int(prom)

# muestro las imagenes para ver como quedaron
cv.imshow('Original', imagen)
cv.imshow('Escalada x2', img_escalada)
cv.imshow('Rotada 90° (Centro)', img_rotada)
cv.imshow('Rotada + Filtro Bilineal', img_filtro_rotada)
cv.waitKey(0)
cv.destroyAllWindows()
