import  numpy as np
import cv2 as cv 
 #Creasa una imagen de 500x500 pixeles, todos con valor 240  (gris claro)
#La imagen tiene solo un canal (escala de grises) y está inicializada a 255 (blanco)
img=np.ones((500,500),dtype=np.uint8)*255
#Dibujamos una linea
#Modifica algunos pixeles especificos con las coordenadas (30,30) a (30,35) y les asigna el valor
#Esto crea una línea ¿vertical? de 6 píxeles de longitud en la posición (30,30) con un valor de intensidad
for i in range(250):
    img[30,30+i]=1

#Supuestamente la línea sería vertical pero me sale horizontal
#Muestra la imagen en una ventana con el título 'img'
cv.imshow('imagen',img)
#Espera a que se presione una tecla para continuar
cv.waitKey()
cv.destroyAllWindows()

#Creasa una imagen de 500x500 pixeles, todos con valor 240  (gris claro)
#La imagen tiene solo un canal (escala de grises) y está inicializada a 255 (blanco)
img=np.ones((500,500),dtype=np.uint8)*255
#Dibujamos una linea
#Modifica algunos pixeles especificos con las coordenadas (30,30) a (30,35) y les asigna el valor
#Esto crea una línea ¿vertical? de 6 píxeles de longitud en la posición (30,30) con un valor de intensidad
img[30,30]=1
img[30,31]=1
img[30,32]=1
img[30,33]=1
img[30,34]=1
img[3,35]=1
#Supuestamente la línea sería vertical pero me sale horizontal
#Muestra la imagen en una ventana con el título 'img'
cv.imshow('img',img)
#Espera a que se presione una tecla para continuar
cv.waitKey()
cv.destroyAllWindows()