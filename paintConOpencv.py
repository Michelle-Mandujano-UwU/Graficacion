# Unidad 1 parte 2 que nunca subi y que pense que si habia subido :(
# Este código crea una pizarra virtual donde se puede dibujar con un objeto de color azul dependiendo del color seleccionado en la acuaerela circular
# Usa OpenCV para la captura de video y procesamiento de imágenes
import cv2
import numpy as np

# Inicialización de la cámara
dispositivo_video = cv2.VideoCapture(0)

# creacion de matriz negra del mismo tamaño que el video    
# Esta matriz funciona como una capa transparente donde se queda guardado el dibujo
valido, frame_guia = dispositivo_video.read()
alto, ancho = frame_guia.shape[:2]
lienzo_dibujo = np.zeros((alto, ancho, 3), dtype=np.uint8)

# Tiempo para que el sensor de la cámara se ajuste
cv2.waitKey(1000)

# Estado inicial del dibujo
tono_seleccionado = [0, 255, 0] # verde por defecto

while dispositivo_video.isOpened(): # Bucle principal de captura
    valido, toma_original = dispositivo_video.read()
    if not valido: break
    
    toma_original = cv2.flip(toma_original, 1)
    
    # Procesamiento de la imagen para detectar el objeto guía
    hsv_analisis = cv2.cvtColor(toma_original, cv2.COLOR_BGR2HSV)
    
    # Rango para detectar el color azul del puntero
    limite_inf = np.array([100, 100, 20])
    limite_sup = np.array([130, 255, 255])
    mascara_puntero = cv2.inRange(hsv_analisis, limite_inf, limite_sup)
    
    # acuarelas
    # Dibuja los botones en una copia temporal para no pintar sobre el video original
    pantalla = toma_original.copy()
    cv2.circle(pantalla, (40, 40), 30, (0, 255, 0), -1)       # Verde
    cv2.circle(pantalla, (120, 40), 30, (255, 0, 136), -1)   # Rosa
    cv2.circle(pantalla, (200, 40), 30, (0, 0, 255), -1)     # Rojo
    cv2.circle(pantalla, (280, 40), 30, (255, 0, 255), -1)   # Morado
    cv2.circle(pantalla, (360, 40), 30, (0, 136, 255), -1)   # Naranja
    cv2.circle(pantalla, (440, 40), 30, (0, 255, 255), -1)   # Amarillo
    cv2.circle(pantalla, (520, 40), 30, (255, 0, 0), -1)     # Azul
    cv2.circle(pantalla, (600, 40), 30, (255, 255, 255), -1) # Goma
    cv2.circle(pantalla, (600, 40), 30, (0, 0, 0), 1)        # Borde goma

    # Escaneo de la máscara para encontrar píxeles del puntero
    # Busca las coordenadas donde la máscara es blanca (255)
    coordenadas = np.where(mascara_puntero == 255)
    
    for f, c in zip(coordenadas[0], coordenadas[1]):
        # Detección de selección de color
        if f < 80:
            if 10 < c < 70: tono_seleccionado = [0, 255, 0]
            elif 90 < c < 150: tono_seleccionado = [255, 0, 136]
            elif 170 < c < 230: tono_seleccionado = [0, 0, 255]
            elif 250 < c < 310: tono_seleccionado = [255, 0, 255]
            elif 330 < c < 390: tono_seleccionado = [0, 136, 255]
            elif 410 < c < 470: tono_seleccionado = [0, 255, 255]
            elif 490 < c < 550: tono_seleccionado = [255, 0, 0]
            elif 570 < c < 630: tono_seleccionado = [255, 255, 255] # Activador goma
        
        # Acción de pintar o borrar
        else:
            if tono_seleccionado == [255, 255, 255]:
                # Si es goma, pintamos de negro en el lienzo para dar efecto borrado porque terminara ciendo negro
                cv2.circle(lienzo_dibujo, (c, f), 10, (0, 0, 0), -1)
            else:
                # Pinta directamente en el lienzo con el color seleccionado
                # Usa un círculo pequeño para que el trazo sea más continuo
                cv2.circle(lienzo_dibujo, (c, f), 3, tono_seleccionado, -1)

    # Solo mostramos en 'pantalla' lo que no sea negro en 'lienzo_dibujo'
    indices_dibujo = np.any(lienzo_dibujo != [0, 0, 0], axis=-1)
    pantalla[indices_dibujo] = lienzo_dibujo[indices_dibujo]

    # Visualización de ventanas
    cv2.imshow("Pizarra", pantalla)
    cv2.imshow("Mascara del Objeto azul", mascara_puntero)

    # Salida del programa
    if cv2.waitKey(1) & 0xFF == ord('s'): break # Salir con tecla 's'
    if cv2.getWindowProperty("Pizarra", cv2.WND_PROP_VISIBLE) < 1: break

dispositivo_video.release()
cv2.destroyAllWindows()