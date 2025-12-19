# este código crea una pizarra virtual donde se puede dibujar con un objeto de color azul
# La interfaz tiene botones circulares para seleccionar diferentes colores de dibujo
# Usa OpenCV para la captura de video y procesamiento de imágenes
import cv2
import numpy as np

# Inicialización de la cámara
dispositivo_video = cv2.VideoCapture(0)

# Conjuntos para almacenar las coordenadas (memoria de dibujo)
# Se usan sets para evitar duplicados y optimizar el guardado
puntos_verde = set()
puntos_rosa = set()
puntos_rojo = set()
puntos_morado = set()
puntos_naranja = set()
puntos_amarillo = set()
puntos_azul = set()
puntos_cyan = set()

# Tiempo para que el sensor de la cámara se ajuste
cv2.waitKey(1000)

# Estado inicial del dibujo
tono_seleccionado = [0, 255, 0] # verde por defecto

while dispositivo_video.isOpened(): # Bucle principal de captura
    # Lectura de un frame
    valido, toma_original = dispositivo_video.read()
    if not valido:
        break

    # Imagen donde se mostrará el dibujo y la interfaz
    pantalla = toma_original.copy()
    
    # Acuarela
    # Parámetros: (centro), radio, color, grosor (-1 es relleno) para circulos
    cv2.circle(pantalla, (40, 40), 30, (0, 255, 0), -1)       # Verde
    cv2.circle(pantalla, (120, 40), 30, (255, 0, 136), -1)   # Rosa
    cv2.circle(pantalla, (200, 40), 30, (0, 0, 255), -1)     # Rojo
    cv2.circle(pantalla, (280, 40), 30, (255, 0, 255), -1)   # Morado
    cv2.circle(pantalla, (360, 40), 30, (0, 136, 255), -1)   # Naranja
    cv2.circle(pantalla, (440, 40), 30, (0, 255, 255), -1)   # Amarillo
    cv2.circle(pantalla, (520, 40), 30, (255, 0, 0), -1)     # Azul
    cv2.circle(pantalla, (600, 40), 30, (255, 255, 0), -1)   # Cyan

    # Procesamiento de la imagen para detectar el objeto guía
    # Convertimos a espacio HSV para detectar el objeto físico (el puntero)
    hsv_analisis = cv2.cvtColor(toma_original, cv2.COLOR_BGR2HSV)
    
    # Rango para detectar el color azul del puntero
    limite_inf = np.array([100, 100, 20])
    limite_sup = np.array([130, 255, 255])
    # Crear máscara para el color azul
    mascara_puntero = cv2.inRange(hsv_analisis, limite_inf, limite_sup)
    
    dimension_y = toma_original.shape[0]
    dimension_x = toma_original.shape[1]

    # Escaneo de la máscara para encontrar píxeles del puntero
    for f in range(dimension_y):
        for c in range(dimension_x):
            if mascara_puntero[f, c] != 0: # Hay píxel del puntero
                
                # Detección de selección de color (si está en la interfaz)
                if f < 80:
                    if 10 < c < 70: tono_seleccionado = [0, 255, 0]
                    elif 90 < c < 150: tono_seleccionado = [255, 0, 136]
                    elif 170 < c < 230: tono_seleccionado = [0, 0, 255]
                    elif 250 < c < 310: tono_seleccionado = [255, 0, 255]
                    elif 330 < c < 390: tono_seleccionado = [0, 136, 255]
                    elif 410 < c < 470: tono_seleccionado = [0, 255, 255]
                    elif 490 < c < 550: tono_seleccionado = [255, 0, 0]
                    elif 570 < c < 630: tono_seleccionado = [255, 255, 0]

                # Accion de pintar (si está abajo de la interfaz)
                else:
                    if tono_seleccionado == [0, 255, 0]: puntos_verde.add((f, c))
                    elif tono_seleccionado == [255, 0, 136]: puntos_rosa.add((f, c))
                    elif tono_seleccionado == [0, 0, 255]: puntos_rojo.add((f, c))
                    elif tono_seleccionado == [255, 0, 255]: puntos_morado.add((f, c))
                    elif tono_seleccionado == [0, 136, 255]: puntos_naranja.add((f, c))
                    elif tono_seleccionado == [0, 255, 255]: puntos_amarillo.add((f, c))
                    elif tono_seleccionado == [255, 0, 0]: puntos_azul.add((f, c))
                    elif tono_seleccionado == [255, 255, 0]: puntos_cyan.add((f, c))

    # Mostrar el color seleccionado actualmente
    # Dibujamos en la pantalla final los píxeles guardados
    for coord in puntos_verde: pantalla[coord[0], coord[1]] = [0, 255, 0]
    for coord in puntos_rosa: pantalla[coord[0], coord[1]] = [255, 0, 136]
    for coord in puntos_rojo: pantalla[coord[0], coord[1]] = [0, 0, 255]
    for coord in puntos_morado: pantalla[coord[0], coord[1]] = [255, 0, 255]
    for coord in puntos_naranja: pantalla[coord[0], coord[1]] = [0, 136, 255]
    for coord in puntos_amarillo: pantalla[coord[0], coord[1]] = [0, 255, 255]
    for coord in puntos_azul: pantalla[coord[0], coord[1]] = [255, 0, 0]
    for coord in puntos_cyan: pantalla[coord[0], coord[1]] = [255, 255, 0]

    # Visualización de ventanas
    cv2.imshow("Pizarra", pantalla)
    cv2.imshow("Mascara del Objeto azul", mascara_puntero)

    # Salida del programa
    if cv2.waitKey(1) & 0xFF == ord('s'): # Salir con tecla 's'
        break
    if cv2.getWindowProperty("Pizarra con Circulos", cv2.WND_PROP_VISIBLE) < 1:
        break

dispositivo_video.release()
cv2.destroyAllWindows()