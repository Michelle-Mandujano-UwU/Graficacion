import cv2 as cv

# Lee la imagen (asegúrate de que 'ejemplo.png' esté en la misma carpeta que este .py)
img = cv.imread('ejemplo.jpg')

# Muestra la imagen en una ventana
cv.imshow('Ejemplo', img)

# Espera a que presiones una tecla
cv.waitKey(0)

# Cierra todas las ventanas abiertas por OpenCV
cv.destroyAllWindows()
 