# Actividad en Apuntes de graficacion: Aplicar las transformaciones geométricas vistas en clase.
import cv2
import numpy as np

def aplicar_transformaciones():
    # Cargar imagen y obtener dimensiones
    foto = cv2.imread("ejemplo.jpg")
    if foto is None:
        print("Error: No se encontro la imagen")
        return

    h, w = foto.shape[:2] # alto y ancho
    
    # Rotacion cambio de angulo a 30°
    # Lienzo negro del mismo tamaño
    img_rotada = np.zeros_like(foto)
    theta = np.radians(30) # conversion a radianes
    c, s = np.cos(theta), np.sin(theta)
    mid_x, mid_y = w // 2, h // 2 # pivote

    for i in range(h):
        for j in range(w):
            # Coordenadas relativas al centro
            x_rel, y_rel = j - mid_x, i - mid_y
            
            new_x = int(x_rel * c - y_rel * s + mid_x)
            new_y = int(x_rel * s + y_rel * c + mid_y)

            if 0 <= new_x < w and 0 <= new_y < h: # para ver si siguen dentro del lienzo
                img_rotada[new_y, new_x] = foto[i, j]

    # Escalado cambio a 0.7x 
    img_escalada = np.zeros((h, w, 3), dtype=np.uint8)
    factor_x, factor_y = 0.7, 0.7

    for i in range(h):
        for j in range(w):
            # Que pixel de la original corresponde a la nueva posicion
            orig_x = int(j / factor_x)
            orig_y = int(i / factor_y)

            if 0 <= orig_x < w and 0 <= orig_y < h:
                img_escalada[i, j] = foto[orig_y, orig_x]

    # Translacion
    img_trasladada = np.zeros_like(foto)
    offset_x, offset_y = 80, 50 # Desplazamiento en píxeles

    for i in range(h):
        for j in range(w):
            target_x = j + offset_x
            target_y = i + offset_y

            if 0 <= target_x < w and 0 <= target_y < h:
                img_trasladada[target_y, target_x] = foto[i, j]

    # Reflexion
    img_reflejo = cv2.flip(foto, 0) # El 0 indica reflexión vertical

    # Visualización de resultados
    cv2.imshow("1. Rotacion 30 deg", img_rotada)
    cv2.imshow("2. Escalado 0.7x", img_escalada)
    cv2.imshow("3. Traslacion (80,50)", img_trasladada)
    cv2.imshow("4. Reflejo Vertical", img_reflejo)
    cv2.imshow("Original", foto)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    aplicar_transformaciones()
 