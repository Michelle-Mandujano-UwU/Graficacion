# Actividad en Apuntes de graficacion: Generar una imagen tipo pixel art utilizando una matriz de enteros en el rango de 0 a 255.

import numpy as np 
import cv2 as cv

# Imagen blanca
img = np.ones((300, 300, 3), dtype=np.uint8) * 255 # Al multiplicar por 255 todos los pixeles se inicializan en color blanco

# Colores BGR
cafe = (60, 80, 160)
negro = (0, 0, 0)

# Tamaño del pixel
# Cada pixel del pixel art se representa como un bloque de p x p pxeles reales
p = 10

# Posicion inicial
x, y = 80, 80

# Cabeza
for i in range(6):
    for j in range(6):
        img[x+i*p:(x+(i+1)*p), y+j*p:(y+(j+1)*p)] = cafe 

# Orejas
for i in range(2):
    img[x-2*p:x, y+i*p:(y+(i+1)*p)] = cafe
    img[x-2*p:x, y+4*p+i*p:(y+5*p+i*p)] = cafe

# Ojos
img[x+2*p:x+3*p, y+1*p:y+2*p] = negro
img[x+2*p:x+3*p, y+4*p:y+5*p] = negro

# Nariz
img[x+3*p:x+4*p, y+2*p:y+4*p] = negro

# Mostrar
cv.imshow("perrito tipo pixel art", img)
cv.waitKey(0)
cv.destroyAllWindows()
