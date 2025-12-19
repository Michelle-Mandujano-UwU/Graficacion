# Este proyecto no fue el que se pidio pero igual lo subo ya que lo mostre en la presentacion de los proyectos, el que esta bien es el otro proyectofinal22.py
# Proyecto Final - Detección de Somnolencia con Temática Navideña
# Este programa utiliza OpenCV y MediaPipe para detectar somnolencia mediante el seguimiento facial.
# Cuando se detecta somnolencia, se dibuja un gorro de dormir y una animación de "Zzz".
# Si la persona está despierta y de frente, se dibuja un gorro navideño y pinos animados.
import numpy as np
import cv2
import mediapipe as mp
#import time
import math 
import imutils
import glfw 
from OpenGL.GL import * 
if not glfw.init():
    raise Exception("No se pudo inicializar GLFW")

# ventana glfw 
ventana_gl = glfw.create_window(640, 480, "Contexto OpenGL", None, None)
glfw.make_context_current(ventana_gl)
glfw.hide_window(ventana_gl) 

RUTA_GORRO = r'C:\Users\miche\Documents\VS\phyton\graficacion\curso python\entorno2\OpenGl\gorro_navidad.png'
IMG_GORRO = cv2.imread(RUTA_GORRO, cv2.IMREAD_UNCHANGED)

if IMG_GORRO is None:
    print("Error: No se pudo cargar la imagen del gorro.")

# Umbrales para Pose
UMBRAL_GIRO = 15    # Ángulo para detectar giro de cabeza (izquierda/derecha) 
UMBRAL_INCLINACION_ABAJO = -15 # Ángulo para detectar cabeza agachada (somnolencia) 
UMBRAL_INCLINACION_ARRIBA = 10 # Ángulo para detectar cabeza levantada (despierto)
 
# Umbral para el ratio de aspecto de la boca
UMBRAL_MAR = 0.65  # Umbral para detectar boca abierta
CONTEO_FRAMES_BOSTEZO = 8  # Cuántos frames seguidos debe estar la boca abierta

# Texto fuente
ESCALA_FUENTE_PREDETERMINADA = 0.8
ESCALA_FUENTE_SOMNOLENCIA = 1.0 
GROSOR_FUENTE = 2

# Inicialización de MediaPipe
mp_rostro = mp.solutions.face_mesh # Módulo de malla facial
malla_facial = mp_rostro.FaceMesh(max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) 

# estetica
mp_dibujo = mp.solutions.drawing_utils 
especificacion_dibujo = mp_dibujo.DrawingSpec(thickness=1, circle_radius=1) 

# Puntos clave necesarios
INDICES_PUNTOS_POSE = [33, 263, 1, 61, 291, 199]  # Puntos para estimar la pose de la cabeza
INDICE_PUNTO_SUPERIOR_CABEZA = 10 
INDICES_PUNTOS_BOCA = [61, 291, 13, 14] 

# Puntos clave del ojo 
PUNTOS_OJO_DERECHO = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
PUNTOS_OJO_IZQUIERDO = [362, 382, 381, 380, 374, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]

cap = cv2.VideoCapture(0)

# Variables de estado
contador_bostezo = 0 # Contador de frames con boca abierta
esta_durmiendo = False 
frame_animacion = 0  # muchas hojitas para la animación
centro_boca = (0, 0) # Centro de la boca para animaciones

# no se usa
def relacion_aspecto_ojo(puntos_ojo):
    # Calcula la relacion del aspecto del ojo
    A = np.linalg.norm(puntos_ojo[1] - puntos_ojo[5])
    B = np.linalg.norm(puntos_ojo[2] - puntos_ojo[4])
    C = np.linalg.norm(puntos_ojo[0] - puntos_ojo[3])
    # evitar division por cero
    if C == 0: return 0 
    # Calculo del de relacion de ancho-alto
    ear = (A + B) / (2.0 * C)
    return ear

def relacion_aspecto_boca(puntos_boca):
    # calcula la relacion del aspecto de la boca
    A = np.linalg.norm(puntos_boca[2] - puntos_boca[3]) # distancia vertical
    B = np.linalg.norm(puntos_boca[0] - puntos_boca[1]) # distancia horizontal
    if B == 0: return 0
    mar = A / B
    return mar

def dibujar_gorro_dormir_opengl(imagen, punto_centro, ancho_cara, indice_frame):
    """Dibuja un gorro de dormir usando lógica de primitivas."""
    punta = (punto_centro[0], punto_centro[1] - int(ancho_cara * 1.5))
    base_izq = (punto_centro[0] - ancho_cara // 2, punto_centro[1])
    base_der = (punto_centro[0] + ancho_cara // 2, punto_centro[1])
    oscilacion = int(15 * math.sin(indice_frame * 0.2))
    pts = np.array([punta, base_izq, base_der], np.int32)
    cv2.fillConvexPoly(imagen, pts, (128, 0, 128)) # Cuerpo (Triángulo)
    cv2.circle(imagen, (punta[0] + oscilacion, punta[1] - 10), 12, (255, 255, 255), -1) # Borla (Punto)

def dibujar_animacion_sueno(imagen, centro_x, centro_y, indice_frame):
    """Dibuja una animación de Zzz que simula salir de la boca/cara."""
    color = (255, 0, 0) # Color azul BGR
    for i in range(3): # Dibujar 3 letras Z
        desplazamiento_y = -30 - (i * 20) + 15 * math.sin(indice_frame * 0.15 + i * 0.5)  # Movimiento vertical oscilante
        desplazamiento_x = 10 * math.cos(indice_frame * 0.1 + i * 0.8) # Movimiento horizontal oscilante
        # Posición de la letra Z
        z_x = centro_x + int(desplazamiento_x) + (i * 10) 
        z_y = centro_y + int(desplazamiento_y)
        # Dibujar la letra Z
        cv2.putText(imagen, "Z", (z_x, z_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3) 
        
def dibujar_gorro_navidad_2d(imagen, punto_superior_2d, ancho_cara_px, angulo_x, angulo_y):
    # Global para acceder a la imagen cargada fuera de la función
    global IMG_GORRO
    if IMG_GORRO is None: # Si la imagen no se cargó correctamente, salir
        return
    ancho_g = int(ancho_cara_px * 2.1)
    gorro_res = imutils.resize(IMG_GORRO, width=ancho_g)
    alto_h, ancho_h, _ = gorro_res.shape
    # Calcular posición
    x_offset = punto_superior_2d[0] - (ancho_h // 2) 
    y_offset = punto_superior_2d[1] - alto_h + int(ancho_cara_px * 0.4) 
    # Límites de la pantalla para que no se cierre si salgo
    h, w, _ = imagen.shape
    y1, y2 = max(0, y_offset), min(h, y_offset + alto_h) 
    x1, x2 = max(0, x_offset), min(w, x_offset + ancho_h)
    # Recorte del gorro para que encaje en la sección visible
    g_y1, g_y2 = max(0, -y_offset), min(alto_h, h - y_offset)
    g_x1, g_x2 = max(0, -x_offset), min(ancho_h, w - x_offset)
    if y1 >= y2 or x1 >= x2:
        return
    # Pegado con Transparencia
    gorro_roi = gorro_res[g_y1:g_y2, g_x1:g_x2] # Región del gorro recortada
    fondo_roi = imagen[y1:y2, x1:x2] # Región de la imagen donde se pegará el gorro
    if gorro_roi.shape[2] == 4:
        canal_alfa = gorro_roi[:, :, 3] / 255.0 # Canal alfa normalizado 
        canal_inv = 1.0 - canal_alfa # lo que no se tapa del gorro
        for c in range(0, 3): # Mezclar colores B, G, R con cara y gorro
            imagen[y1:y2, x1:x2, c] = (canal_alfa * gorro_roi[:, :, c] +
                                      canal_inv * fondo_roi[:, :, c])
    else:
        # Si no tiene transparencia, pegar directo
        imagen[y1:y2, x1:x2] = gorro_roi[:, :, :3]

def dibujar_pinos_navidad_animados(imagen, img_ancho, img_alto, indice_frame):
    """Dibuja pinos de Navidad animados a los costados."""
    color_verde = (0, 255, 0)
    color_marron = (42, 42, 165) 
    pulsacion = 1 + 0.2 * math.sin(indice_frame * 0.15) 
    tamaño_base = int(img_ancho * 0.1 * pulsacion)
    altura = int(img_alto * 0.2 * pulsacion)
    pino_izq_x = int(img_ancho * 0.1)
    pino_der_x = int(img_ancho * 0.9)
    pino_y = int(img_alto * 0.8)  # Base del pino
    # Pino Izquierdo
    cv2.rectangle(imagen, (pino_izq_x - 10, pino_y), (pino_izq_x + 10, pino_y + 30), color_marron, -1)
    pts_izq = np.array([[pino_izq_x, pino_y - altura], 
                         [pino_izq_x - tamaño_base // 2, pino_y], 
                         [pino_izq_x + tamaño_base // 2, pino_y]], np.int32)
    cv2.fillConvexPoly(imagen, pts_izq, color_verde)
    # Pino Derecho
    cv2.rectangle(imagen, (pino_der_x - 10, pino_y), (pino_der_x + 10, pino_y + 30), color_marron, -1)
    pts_der = np.array([[pino_der_x, pino_y - altura], 
                          [pino_der_x - tamaño_base // 2, pino_y], 
                          [pino_der_x + tamaño_base // 2, pino_y]], np.int32)
    cv2.fillConvexPoly(imagen, pts_der, color_verde)

# Bucle principal de procesamiento de video
while cap.isOpened(): # Mientras la cámara esté abierta
    exito, imagen = cap.read() # Leer un frame
    if not exito:
        print("Ignorando frame vacío de la cámara.")
        break

    imagen = cv2.flip(imagen, 1) # Voltear horizontalmente para efecto espejo
    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB) # Cambiar oirden de RGB para MediaPipe
    imagen_rgb.flags.writeable = False # Marcar como no escribible para mejorar rendimiento ( solo lectura)
    resultados = malla_facial.process(imagen_rgb) # Procesar la imagen y detectar la malla facial
    imagen_rgb.flags.writeable = True # Marcar como escribible de nuevo
    imagen = cv2.cvtColor(imagen_rgb, cv2.COLOR_RGB2BGR) # Convertir de nuevo a BGR para OpenCV

    img_alto, img_ancho, _ = imagen.shape # Obtener dimensiones del video
    
    rostro_2d = [] # miradas guardadas partes de ojos frente y cejas
    rostro_3d = []
    
    # Estado inicial por defecto: Navidad
    texto_pose_actual = "DESPERTE, ¿ES NAVIDAD?" 
    esta_durmiendo = False
    
    if resultados.multi_face_landmarks:
        for marcas_faciales in resultados.multi_face_landmarks:
            
            # obtencion de pose
            punto_superior_cabeza = None
            coords_boca = []
            # Recolectar puntos clave necesarios
            for indice, lm in enumerate(marcas_faciales.landmark): # recorrer todos los puntos detectados
                x, y = int(lm.x * img_ancho), int(lm.y * img_alto) # Convertir a coordenadas de píxeles
                
                if indice in INDICES_PUNTOS_POSE:
                    rostro_2d.append([x, y])
                    rostro_3d.append([x, y, lm.z])
                
                if indice == INDICE_PUNTO_SUPERIOR_CABEZA:
                    punto_superior_cabeza = (x, y)
                
                if indice in INDICES_PUNTOS_BOCA:
                    coords_boca.append(np.array([x, y]))
            
            if not rostro_2d or not coords_boca: continue 

            # Cálculo de pose
            rostro_2d = np.array(rostro_2d, dtype=np.float64) 
            rostro_3d = np.array(rostro_3d, dtype=np.float64) # Convertir a array numpy
            distancia_camara = 1 * img_ancho # Asumir distancia focal igual al ancho de la imagen 
            matriz_camara = np.array([[distancia_camara, 0, img_alto / 2], [0, distancia_camara, img_ancho / 2], [0, 0, 1]]) # describe cómo la cámara proyecta puntos 3D en la imagen 2D.
            matriz_distorsion = np.zeros((4, 1), dtype=np.float64) # Asumir sin distorsión (representa la distorsión radial y tangencial del lente)
            exito, vec_rot, vec_trans = cv2.solvePnP(rostro_3d, rostro_2d, matriz_camara, matriz_distorsion)
            matriz_rotacion, _ = cv2.Rodrigues(vec_rot) # orientación del rostro en el espacio 3D
            # Obtener ángulos de Euler a partir de la matriz de rotación
            angulos, _, _, _, _, _ = cv2.RQDecomp3x3(matriz_rotacion)

            angulo_x = angulos[0] * 360  #   convertir a grados
            angulo_y = angulos[1] * 360 
            
            # calculo del aspecto de la boca
            centro_boca = (coords_boca[0] + coords_boca[1]) // 2 
            valor_mar = relacion_aspecto_boca(np.array(coords_boca))
            
            # somnoliento o navidad???
            
            # Condición A: Cabeza Agachada
            if angulo_x < UMBRAL_INCLINACION_ABAJO:
                esta_durmiendo = True
                texto_pose_actual = "SE ESTA QUEDANDO DORMIDO"
                contador_bostezo = 0 # Resetear contador de bostezo
            
            # Condición B: Bostezo (MAR alto)
            elif valor_mar > UMBRAL_MAR:
                contador_bostezo += 1
                if contador_bostezo >= CONTEO_FRAMES_BOSTEZO:
                    esta_durmiendo = True
                    texto_pose_actual = "BOSTEZANDO" 

                    ancho_cara_px = int(np.linalg.norm(np.array(marcas_faciales.landmark[33].x * img_ancho) - np.array(marcas_faciales.landmark[263].x * img_ancho)))
                    dibujar_gorro_dormir_opengl(imagen, punto_superior_cabeza, ancho_cara_px, frame_animacion)
            
            # Condición C: Restablecer Contadores si la persona está activa
            else:
                contador_bostezo = 0
                esta_durmiendo = False
                
                # Pose Normal/Navidad o Mirando a los lados
                if angulo_y < -UMBRAL_GIRO:
                    texto_pose_actual = "MIRA IZQUIERDA"
                elif angulo_y > UMBRAL_GIRO:
                    texto_pose_actual = "MIRA DERECHA"
                else:
                    # De frente, despierto (boca cerrada)
                    texto_pose_actual = "DESPERTE, ¿ES NAVIDAD?"
            
            # DIBUJOS Y ANIMACIONES
            
            # Dibujo de la Máscara de MediaPipe
            #mp_dibujo.draw_landmarks(
                #image=imagen,
                #landmark_list=marcas_faciales,
                #connections=mp_rostro.FACEMESH_CONTOURS,
                #landmark_drawing_spec=especificacion_dibujo,
                #connection_drawing_spec=especificacion_dibujo)

            # Dibujo del Gorro 2D Navideño (SOLO si está de frente y despierto)
            if texto_pose_actual == "DESPERTE, ¿ES NAVIDAD?" and punto_superior_cabeza is not None:
                ancho_cara_px = int(np.linalg.norm(np.array(marcas_faciales.landmark[33].x * img_ancho) - np.array(marcas_faciales.landmark[263].x * img_ancho)))
                dibujar_gorro_navidad_2d(imagen, punto_superior_cabeza, ancho_cara_px, angulo_x, angulo_y)

            # Dibujo del texto de Estado 
            color_texto = (255, 0, 0) if esta_durmiendo else (0, 255, 0) 
            escala_fuente = ESCALA_FUENTE_SOMNOLENCIA if esta_durmiendo else ESCALA_FUENTE_PREDETERMINADA
            
            cv2.putText(imagen, texto_pose_actual, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, escala_fuente, color_texto, GROSOR_FUENTE)
            
            # Dibujo de la ANIMACIÓN DE SUEÑO/BOSTEZO
            if esta_durmiendo:
                # La animación Zzz siempre sale del centro de la boca para ambos casos (bostezo o cabeza agachada)
                dibujar_animacion_sueno(imagen, centro_boca[0], centro_boca[1], frame_animacion)
                
    
    # Dibujo de los pinos animados (CONDICIONAL: Solo si está de frente y despierto)
    if not esta_durmiendo and texto_pose_actual == "DESPERTE, ¿ES NAVIDAD?":
        dibujar_pinos_navidad_animados(imagen, img_ancho, img_alto, frame_animacion)
    
    frame_animacion += 1

    cv2.imshow('Deteccion de Somnolencia', imagen)
    
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
glfw.terminate()
malla_facial.close()