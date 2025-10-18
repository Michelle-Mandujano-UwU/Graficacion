# Este programa usa la cámara para detectar la mano y dibuja un cuadrado
# que se puede mover con la mano y también cambiar de tamaño.
# Si abres los dedos el cuadro crece, si los juntas se hace chiquito.
# Como los hologramas de Iron Man pero bien sencillo jeje.

import cv2
import mediapipe as mp
import numpy as np

# Inicializamos lo de mediapipe (es lo que detecta la mano)
mp_manos = mp.solutions.hands
mp_dibujo = mp.solutions.drawing_utils
manos = mp_manos.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Variables para la posición y tamaño del cuadrado
x_cuadro, y_cuadro = 200, 150   # posición inicial
lado = 100                      # tamaño inicial
guardado = False                # para mantenerlo fijo si no hay mano

# Activamos la camara
camara = cv2.VideoCapture(0)

while camara.isOpened():
    ok, cuadro = camara.read()
    if not ok:
        break

    alto, ancho, _ = cuadro.shape
    cuadro_rgb = cv2.cvtColor(cuadro, cv2.COLOR_BGR2RGB)
    resultado = manos.process(cuadro_rgb)

    # Si se detecta la mano
    if resultado.multi_hand_landmarks:
        for mano in resultado.multi_hand_landmarks:
            mp_dibujo.draw_landmarks(cuadro, mano, mp_manos.HAND_CONNECTIONS)

            # Pulgar e indice (mediapipe usa esos números)
            pulgar = mano.landmark[4]
            indice = mano.landmark[8]

            # Coordenadas en pixeles
            x_pulgar, y_pulgar = int(pulgar.x * ancho), int(pulgar.y * alto)
            x_indice, y_indice = int(indice.x * ancho), int(indice.y * alto)

            # Calculamos distancia (para el zoom)
            distancia = np.sqrt((x_indice - x_pulgar) ** 2 + (y_indice - y_pulgar) ** 2)
            lado = int(distancia * 1.8)
            if lado < 50:
                lado = 50
            elif lado > 300:
                lado = 300

            # Calculamos centro del cuadro con la posición media entre los dedos
            x_cuadro = int((x_pulgar + x_indice) / 2)
            y_cuadro = int((y_pulgar + y_indice) / 2)

            # Si la mano se ve, actualizamos la posición
            guardado = True

    # Si ya hubo una mano antes, el cuadro se mantiene en su última posición
    if guardado:
        x1 = x_cuadro - lado // 2
        y1 = y_cuadro - lado // 2
        x2 = x_cuadro + lado // 2
        y2 = y_cuadro + lado // 2

        # Evitamos que se salga del frame
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(ancho, x2)
        y2 = min(alto, y2)

        # Dibujamos el cuadrado rojo
        cv2.rectangle(cuadro, (x1, y1), (x2, y2), (0, 0, 255), 5)

    # Mostramos el resultado
    cv2.imshow("Cuadro tipo Iron Man", cuadro)

    # Si se presiona la tecla q, se sale
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cerramos todo
camara.release()
cv2.destroyAllWindows()

