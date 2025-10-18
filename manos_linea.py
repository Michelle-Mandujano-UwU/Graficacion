# este programa usa la camara para detectar la mano y dibuja una linea entre el pulgar y el indice
# usa la libreria mediapipe que permite reconocer los puntos de la mano

import cv2  # pa usar la camara y dibujar cosas
import mediapipe as mp  # esta es la que detecta la mano
import numpy as np  # ni se si lo use pero lo dejo xd

# esto es lo que se necesita pa que mediapipe funcione con manos
mp_manos = mp.solutions.hands
mp_dibujo = mp.solutions.drawing_utils
manos = mp_manos.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# estas son las variables donde voy a guardar los puntos del pulgar e indice
pulgar = None
indice = None

# se prende la camara
camara = cv2.VideoCapture(0)

while camara.isOpened():
    ok, cuadro = camara.read()  # aqui se lee lo que ve la camara
    if not ok:
        break  # si no se pudo leer pues se sale

    # saca el tamaño del cuadro (osea alto y ancho)
    alto, ancho, _ = cuadro.shape

    # mediapipe quiere las imagenes en RGB (no en BGR como cv2)
    cuadro_rgb = cv2.cvtColor(cuadro, cv2.COLOR_BGR2RGB)

    # aqui ya se procesa la imagen para ver si hay mano
    resultado = manos.process(cuadro_rgb)

    # si detecta manos, dibuja los puntos
    if resultado.multi_hand_landmarks:
        for mano in resultado.multi_hand_landmarks:
            # dibuja los puntos de la mano y las lineas
            mp_dibujo.draw_landmarks(cuadro, mano, mp_manos.HAND_CONNECTIONS)

            # ahora saco el punto del pulgar (4) y del indice (8)
            pulgar = mano.landmark[4]
            indice = mano.landmark[8]

            # se convierten las coordenadas de 0 a 1 a pixeles
            px, py = int(pulgar.x * ancho), int(pulgar.y * alto)
            ix, iy = int(indice.x * ancho), int(indice.y * alto)

        # ya con eso dibujamos la linea (color rojito)
        cv2.line(cuadro, (px, py), (ix, iy), (0, 0, 255), 2)

    # se muestra la ventana del video
    cv2.imshow("Mano con linea", cuadro)

    # si presionas la q se cierra
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# se apaga todo ya al final
camara.release()
cv2.destroyAllWindows()
