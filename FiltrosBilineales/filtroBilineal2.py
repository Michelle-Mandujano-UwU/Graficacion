# Segundo ejercicio
# Aqui se trabaja con otra imagen para repetir el proceso pero en diferente orden
# Se escala al doble, se rota 45 grados y al final se aplica el filtro bilineal

import cv2 as cv
import numpy as np
import math

# Leer la imagen en escala de grises
imagen = cv.imread('filBili2.png', 0)

# Verificar que la imagen se encuentra porq aja xD
if imagen is None:
    print("No se encontro la imagen")
    exit()

# Tamaño original de la imagen
alto, ancho = imagen.shape

# Crear imagenes vacias para cada paso del proceso
img_escalada = np.zeros((alto * 2, ancho * 2), dtype=np.uint8)
img_rotada = np.zeros_like(img_escalada)
img_filtro = np.zeros_like(img_escalada)

# Definir el angulo de rotacion en radianes
angulo = 45
rad = math.radians(angulo)

# Escalar imagen x2
# Aqui duplico el tamaño separando mas los pixeles
for i in range(alto):
    for j in range(ancho):
        nuevo_y = i * 2
        nuevo_x = j * 2
        if nuevo_y < alto * 2 and nuevo_x < ancho * 2:
            img_escalada[nuevo_y, nuevo_x] = imagen[i, j]

# Rotar imagen 45 grados
# Uso las formulas de rotacion en coordenadas x y para mover cada pixel
for i in range(img_escalada.shape[0]):
    for j in range(img_escalada.shape[1]):
        nuevo_x = int(i * math.cos(rad) + j * math.sin(rad))
        nuevo_y = int(j * math.cos(rad) - i * math.sin(rad))
        if 0 <= nuevo_x < img_rotada.shape[1] and 0 <= nuevo_y < img_rotada.shape[0]:
            img_rotada[nuevo_y, nuevo_x] = img_escalada[i, j]

# Aplicar filtro bilineal
# Este filtro suaviza los bordes haciendo un promedio de los pixeles cercanos
for i in range(1, img_rotada.shape[0] - 1):
    for j in range(1, img_rotada.shape[1] - 1):
        vecinos = img_rotada[i-1:i+2, j-1:j+2].flatten()
        img_filtro[i, j] = int(np.mean(vecinos))

# Mostrar una por una las imagenes generadas
cv.imshow('Original', imagen)
cv.waitKey(0)
cv.destroyWindow('Original')

cv.imshow('Escalada x2', img_escalada)
cv.waitKey(0)
cv.destroyWindow('Escalada x2')

cv.imshow('Escalada + Rotada 45 grados', img_rotada)
cv.waitKey(0)
cv.destroyWindow('Escalada + Rotada 45 grados')

cv.imshow('Escalada + Rotada + Filtro Bilineal', img_filtro)
cv.waitKey(0)
cv.destroyWindow('Escalada + Rotada + Filtro Bilineal')

# Cierra todas las ventanas al final
cv.destroyAllWindows()
