# Actividad en Apuntes de graficacion: Generar al menos cinco operadores puntuales utilizando una imagen previamente cargada

import cv2
import numpy as np

# Cargar imagen
foto = cv2.imread("ejemplo.jpg")

if foto is None:
    print("Error: no se encontro el archivo de imagen")
else:
    # pasar a grises para practicidad
    fgris = cv2.cvtColor(foto, cv2.COLOR_BGR2GRAY)
    
    # Inversion total
    # Como las fotos viejitas
    viejita = 255 - fgris

    # Mas iluminacion
    # Aumentando 0 a la intensidad de cada punto
    brillo_alto = np.clip(fgris.astype(np.int16) + 40, 0, 255).astype(np.uint8)

    # Oscuridad
    # Restando 40 a la intensidad de cada punto
    brillo_bajo = np.clip(fgris.astype(np.int16) - 40, 0, 255).astype(np.uint8)

    # Umbralizacion (blanco y negro)
    # Si el pixel es mayor a 128 se vuelve 255, si no 0
    _, fbinaria = cv2.threshold(fgris, 128, 255, cv2.THRESH_BINARY)

    # Contrsaste reducido
    # Bajo un poquito a los grises para que no brille tanto
    contrasteR = (fgris * 0.8).astype(np.uint8)

    #mostrar
    cv2.imshow("Original en Gris", fgris)
    cv2.imshow("Efecto Negativo", viejita)
    cv2.imshow("Mas Iluminacion", brillo_alto)
    cv2.imshow("Menos Iluminacion", brillo_bajo)
    cv2.imshow("Umbralizacion", fbinaria)
    cv2.imshow("Contraste Reducido", contrasteR)
    cv2.waitKey(0)
    cv2.destroyAllWindows()