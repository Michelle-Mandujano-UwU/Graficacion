# Este programa agarra una imagen, la agranda (factor 2),
# le aplica un filtro bilineal para suavizar y luego la rota 45°
# volviendo a aplicar el filtro despues de girarla

import cv2 as cv
import numpy as np
import math

# Leer la imagen en blanco y negro
imagen = cv.imread('filtrob1.png', 0)

# Esto porque tarde mil años en que reconociera la imagen y solo era la extension XD
if imagen is None:
    print("No se encontro la imagen")
    exit()

# Tamaño original de la imagen
alto, ancho = imagen.shape

# Crear imagenes vacias como lienzos donde se guardaran las nuevas versiones
img_escalada = np.zeros((alto * 2, ancho * 2), dtype=np.uint8)
img_rotada = np.zeros_like(img_escalada)
img_filtro_escalada = np.zeros_like(img_escalada)
img_filtro_rotada = np.zeros_like(img_escalada)

# Angulo de rotacion en radianes
angulo = 45
rad = math.radians(angulo)

# Escalar imagen osea que agrandar al doble
# Aqui solo duplico las posiciones de los pixeles
for i in range(alto):
    for j in range(ancho):
        nuevo_y = i * 2
        nuevo_x = j * 2
        if nuevo_y < alto * 2 and nuevo_x < ancho * 2:
            img_escalada[nuevo_y, nuevo_x] = imagen[i, j]

# Aplicar filtro bilineal a la imagen escalada
# Este filtro suaviza la imagen haciendo un promedio de los pixeles cercanos
for i in range(1, img_escalada.shape[0] - 1):
    for j in range(1, img_escalada.shape[1] - 1):
        vecinos = img_escalada[i-1:i+2, j-1:j+2].flatten()
        img_filtro_escalada[i, j] = int(np.mean(vecinos))

# Rotar la imagen escalada 45 grados
# Aqui uso las formulas de rotacion para mover cada pixel a su nueva posicion
for i in range(img_escalada.shape[0]):
    for j in range(img_escalada.shape[1]):
        nuevo_x = int(i * math.cos(rad) + j * math.sin(rad))
        nuevo_y = int(j * math.cos(rad) - i * math.sin(rad))
        if 0 <= nuevo_x < img_rotada.shape[1] and 0 <= nuevo_y < img_rotada.shape[0]:
            img_rotada[nuevo_y, nuevo_x] = img_escalada[i, j]

# Filtro bilineal despues de la rotacion
# Se vuelve a aplicar el mismo promedio para suavizar los bordes que salieron al girar
for i in range(1, img_rotada.shape[0] - 1):
    for j in range(1, img_rotada.shape[1] - 1):
        vecinos = img_rotada[i-1:i+2, j-1:j+2].flatten()
        img_filtro_rotada[i, j] = int(np.mean(vecinos))

# Mostrar todas las imagenes generadas
cv.imshow('Original', imagen)
cv.waitKey(0)
cv.destroyWindow('Original')

cv.imshow('Escalada', img_escalada)
cv.waitKey(0)
cv.destroyWindow('Escalada')

cv.imshow('Escalada + Filtro Bilineal', img_filtro_escalada)
cv.waitKey(0)
cv.destroyWindow('Escalada + Filtro Bilineal')

cv.imshow('Rotada 45°', img_rotada)
cv.waitKey(0)
cv.destroyWindow('Rotada 45°')

cv.imshow('Rotada + Filtro Bilineal', img_filtro_rotada)
cv.waitKey(0)
cv.destroyWindow('Rotada + Filtro Bilineal')
