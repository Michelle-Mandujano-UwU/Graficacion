# Calculadora con deteccion de mano
# Este programa usa la camara para ver tu mano y detectar el dedo indice
# Al mover el dedo sobre los botones que aparecen en pantalla, puedes marcar
# numeros y operaciones como si fuera una calculadora en el aire
# Solo marca si mantienes el dedo sobre el boton por unos segundos, asi no se marcan de mas por error

import cv2 as cv
import mediapipe as mp
import numpy as np
import time

# Herramienta de MediaPipe para detectar manos
mp_manos = mp.solutions.hands
manos = mp_manos.Hands(max_num_hands=1)
mp_dibujo = mp.solutions.drawing_utils

# Abrir la camara
cam = cv.VideoCapture(0)

# Crear los botones de la calculadora con numeros y operaciones basicas
botones = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", "C", "=", "+"]
]

# Medidas de los botones y donde empiezan
ancho = 100
alto = 80
espacio = 15
x_inicial = 100
y_inicial = 120   # medida para que se vea toda la calculadora

# Se guardan las posiciones de cada boton
pos_botones = []
for fila in range(len(botones)):
    for col in range(len(botones[fila])):
        x = x_inicial + col * (ancho + espacio)
        y = y_inicial + fila * (alto + espacio)
        pos_botones.append((x, y, botones[fila][col]))

# Variables que se usan para controlar la logica
entrada = ""         # guarda lo que se va escribiendo
resultado = ""       # guarda el resultado de la operacion
boton_actual = None  # cual boton esta siendo tocado
tiempo_inicio = 0    # cuando se empezo a tocar el boton
tiempo_requerido = 2 # segundos que debe durar el toque para marcar

while True:
    ret, frame = cam.read()
    if not ret:
        break

    # Voltear la imagen como espejo visto en clase
    frame = cv.flip(frame, 1)

    # Se convierte a RGB para que funcione con MediaPipe
    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    res = manos.process(rgb)
    h, w, _ = frame.shape

    # Fondo claro para que se note la calculadora
    cv.rectangle(frame, (80, 60), (w - 80, h - 40), (245, 245, 245), -1)

    # Dibujar los botones con texto
    for (x, y, b) in pos_botones:
        cv.rectangle(frame, (x, y), (x + ancho, y + alto), (200, 200, 200), -1)
        cv.putText(frame, b, (x + 35, y + 55), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)

    # Deteccion de una mano
    if res.multi_hand_landmarks:
        for mano in res.multi_hand_landmarks:
            # Dibuja la estructura de la mano solo para ver la deteccion de la mano
            mp_dibujo.draw_landmarks(frame, mano, mp_manos.HAND_CONNECTIONS)

            # Coordenadas del dedo indice
            dedo = mano.landmark[8]
            x_dedo = int(dedo.x * w)
            y_dedo = int(dedo.y * h)

            # Dibuja un circulo donde esta el dedo para mayor presicion al tocar un boton saber donde esta
            cv.circle(frame, (x_dedo, y_dedo), 10, (255, 0, 255), -1)

            # Revisar si el dedo toca algun boton
            tocando = False
            for (x, y, b) in pos_botones:
                if x < x_dedo < x + ancho and y < y_dedo < y + alto:
                    # Si el dedo esta encima se ilumina
                    cv.rectangle(frame, (x, y), (x + ancho, y + alto), (255, 182, 193), -1)
                    cv.putText(frame, b, (x + 35, y + 55), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)
                    tocando = True

                    # Si el mismo boton se mantiene tocado calculo de duracion
                    if boton_actual == b:
                        tiempo_actual = time.time()
                        duracion = tiempo_actual - tiempo_inicio

                        # Si ya paso el tiempo requerido se ejecuta la accion
                        if duracion >= tiempo_requerido:
                            if b == "C":          # borrar todo
                                entrada = ""
                                resultado = ""
                            elif b == "=":        # calcular el resultado
                                try:
                                    resultado = str(eval(entrada))
                                except:
                                    resultado = "Error"
                            else:                 # agregar numero u operacion
                                entrada += b

                            # reiniciar el boton actual y tiempo
                            boton_actual = None
                            tiempo_inicio = 0
                    else:
                        # Si se toco un nuevo boton inicia el conteo de tiempo desde cero
                        boton_actual = b
                        tiempo_inicio = time.time()

                    break

            # Si no se esta tocando nada reinicia el contador
            if not tocando:
                boton_actual = None
                tiempo_inicio = 0

    # Dibujar la parte de arriba donde se muestra la operacion y resultado
    cv.rectangle(frame, (x_inicial, 40), (x_inicial + 4*(ancho + espacio) - espacio, 100), (255, 255, 255), -1)
    cv.putText(frame, entrada, (x_inicial + 10, 90), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)
    if resultado:
        cv.putText(frame, "="+resultado, (x_inicial + 300, 90), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

    # Mostrar la ventana
    cv.imshow("Calculadora con la mano", frame)

    # Presionar ESC para salir
    if cv.waitKey(1) & 0xFF == 27:
        break

# Cerrar la camara y cerrar ventanas
cam.release()
cv.destroyAllWindows()


