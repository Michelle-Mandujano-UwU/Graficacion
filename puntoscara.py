# Programa para detectar y rastrear puntos clave en la cara usando MediaPipe y OpenCV
import cv2
import mediapipe as mp
import numpy as np


# Inicializamos el sistema de malla facial (Face Mesh)
mp_malla_facial = mp.solutions.face_mesh
malla_facial = mp_malla_facial.FaceMesh(
    static_image_mode=False,        # False porque es video en vivo, no fotos sueltas
    max_num_faces=2,               # Cuántas caras queremos detectar a la vez
    min_detection_confidence=0.5,  # Qué tan seguro debe estar de que hay una cara
    min_tracking_confidence=0.5,   # Qué tan seguro debe estar al seguir el movimiento
)

# Captura de video
camara = cv2.VideoCapture(0)

# Lista de índices de puntos clave (Landmarks) 
# Estos números representan partes como ojos, nariz y boca en el mapa de MediaPipe
puntos_seleccionados = [33, 133, 362, 263, 4, 61, 291, 0, 17]

def calcular_distancia(punto1, punto2):
    """ Calcula qué tan lejos está un punto del otro (matemática pura) """
    return np.linalg.norm(np.array(punto1) - np.array(punto2))

while camara.isOpened():
    exito, cuadro = camara.read() 
    if not exito:
        print("¡Ups! No se pudo leer la cámara.")
        break

    # Volteamos el cuadro como un espejo
    cuadro = cv2.flip(cuadro, 1) 
    
    # MediaPipe trabaja mejor con colores RGB, pero OpenCV usa BGR, así que convertimos
    rgb_cuadro = cv2.cvtColor(cuadro, cv2.COLOR_BGR2RGB)
    resultados = malla_facial.process(rgb_cuadro)

    # Si el programa encuentra caras...
    if resultados.multi_face_landmarks:
        for marcas_faciales in resultados.multi_face_landmarks:
            diccionario_puntos = {}

            # Recorremos solo los puntos que nos interesan
            for id_punto in puntos_seleccionados:
                # Calculamos las coordenadas reales (píxeles) 
                pos_x = int(marcas_faciales.landmark[id_punto].x * cuadro.shape[1])
                pos_y = int(marcas_faciales.landmark[id_punto].y * cuadro.shape[0])
                
                diccionario_puntos[id_punto] = (pos_x, pos_y)
                
                # Dibujamos un circulito verde en cada punto detectado
                cv2.circle(cuadro, (pos_x, pos_y), 2, (0, 255, 0), -1)

            # Si detectamos los puntos del ojo izquierdo (33 y 133), podemos poner texto
            if 33 in diccionario_puntos and 133 in diccionario_puntos:
                # Coordenadas cerca de la boca (punto 61)
                if 61 in diccionario_puntos:
                    cv2.putText(
                        cuadro,
                        f"Coord: {diccionario_puntos[61]}",
                        (diccionario_puntos[61][0], diccionario_puntos[61][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0), # Color verde
                        1
                    )

    # Mostramos la ventana con los puntos dibujados
    cv2.imshow("Rastreador de Puntos Faciales", cuadro)

    # Si presionas la tecla 'q', el programa se cierra
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Al terminar, liberamos la cámara y cerramos las ventanas
camara.release()
cv2.destroyAllWindows()