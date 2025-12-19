# Este programa permite dibujar en una pizarra virtual usando el seguimiento de manos con MediaPipe
# Permite dibujar formas geométricas y pintar como en un lienzo con las manos
# Permite seleccionar colores y borrar el lienzo
# Si el pulgar está arriba se dibuja la forma seleccionada (like)

import cv2 # Para captura y procesamiento de video
import numpy as np # Para matrices del lienzo
import keyboard as tecla_rapida # por si se ocupa alguna tecla
import mediapipe as mp # Para el seguimiento de manos
import math # Para cálculos de circulos, rotaciones, etc

# Configuración de MediaPipe Hands
mediap_manos = mp.solutions.hands 
mediap_dibujo = mp.solutions.drawing_utils # puntos de manos
manos_deteccion = mediap_manos.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) #para detección y seguimiento

colores = (0,255,0) # Color inicial (verde)
seleccion = 0 # cual opcion se tiene pincel, rectangulo etc.

# Inicializar cámara web
captura = cv2.VideoCapture(0)
cv2.waitKey(2000) # tiempo de estabilizacion de la cámara
canvas = None   # lienzo del pincel (necesita el cuadro)
guardar_formas = []     

# Variables para detectar manos cual
mano_guardar=False
mano_de_control=None
pulgar_donde_x,pulgar_donde_y,indice_donde_x,indice_donde_y=0,0,0,0 # pulgar e indice mano actual
mx_1,my_1,mx_2,my_2=0,0,0,0 # pulgar e indice otra mano para borrar

def cambio(dx, dy, angulo, centrox, centoy):
    # Desplazamiento base, cuánto se debe mover el punto desde el centro antes de rotar (esquina del rectángulo, etc)
    coordenadax = int(centrox + dx * math.cos(angulo) - dy * math.sin(angulo)) # nueva coordenada x después de rotar y trasladar
    coordenaday = int(centoy + dx * math.sin(angulo) + dy * math.cos(angulo)) 
    return coordenadax, coordenaday # devuelve nueva coordenada y después de rotar y trasladar

def linea(x1,y1,x2,y2,guardar):
    centrox = (x2 + x1) / 2 # cañlculo del punto central X entre el pulgar y el índice.
    centroy = (y2 + y1) / 2 
    angulo = math.atan2(y2 - y1, x2 - x1)
    distancia = math.hypot(x2 - x1, y2 - y1)
    x1, y1 = cambio(-distancia * 1.5, 0, angulo, centrox, centroy)  # punto inicial de la línea
    x2, y2 = cambio(distancia * 1.5,0, angulo, centrox, centroy) # punto final de la línea
    if guardar:
        guardar_formas.append((5, (x1, y1, x2, y2), colores))
    return x1,y1,x2,y2

def estrella(x1, y1, x2, y2, guardar):
    centrox, centroy = (x2 + x1) / 2, (y2 + y1) / 2
    angulo = math.atan2(y2 - y1, x2 - x1)
    distancia = math.hypot(x2 - x1, y2 - y1)
    puntos = []
    for i in range(10):
        # Alternar entre puntos exteriores e interiores para crear la forma de estrella
        r = (distancia * 3) if i % 2 == 0 else (distancia * 1.2)
        ang_panta = angulo + (i * math.pi / 5) #
        coordenadax = int(centrox + r * math.cos(ang_panta))
        coordenaday = int(centroy + r * math.sin(ang_panta))
        puntos.append((coordenadax, coordenaday))
    if guardar:
        guardar_formas.append((10, puntos, colores))
    return puntos

def circulo(x1,y1,x2,y2,guardar):
    centrox = int((x2+x1)/2)
    centroy = int((y2+y1)/2)
    distancia = int(math.hypot(x2 - x1, y2 - y1)) # radio del círculo basado en la distancia entre el pulgar y el índice
    if guardar:
        guardar_formas.append((3, (centrox,centroy,distancia*1.1), colores)) # guardar el círculo en la lista de formas
    return centrox,centroy, distancia

def rectangulo(x1,y1,x2,y2,guardar):
    centrox = (x2+x1)/2 
    centroy = (y2+y1)/2 
    angulo = math.atan2(y2 - y1, x2 - x1) 
    distancia = math.hypot(x2 - x1, y2 - y1) 
     # Se usa la distancia y el angulo para proyectar los cuatro puntos (x1,y1, x2,y2, x3,y3, x4,y4)
    # La función cambio aplica la rotación y traslación al rededor del centro (centrox,centroy)
    # Los valores -distancia*2, distancia*2.5, etc son proporcionales al tamaño del rectángulo
    x1,y1 = cambio(-distancia*2,-distancia*2.5,angulo,centrox,centroy)
    x2,y2 = cambio(distancia*2,distancia*2.5,angulo,centrox,centroy)
    x3,y3 = cambio(-distancia*2,distancia*2.5,angulo,centrox,centroy)
    x4,y4 = cambio(distancia*2,-distancia*2.5,angulo,centrox,centroy)
    if guardar:
        guardar_formas.append((2, (x1,y1,x2,y2,x3,y3,x4,y4), colores)) 
    return x1,y1,x2,y2,x3,y3,x4,y4 

def triangulo(x1,y1,x2,y2,guardar):
    centrox = (x2 + x1) / 2
    centroy = (y2 + y1) / 2
    angulo = math.atan2(y2 - y1, x2 - x1) # ángulo entre el pulgar y el índice para orientar el triángulo
    distancia = math.hypot(x2 - x1, y2 - y1) # distancia entre el pulgar y el índice para escalar el triángulo
    x1, y1 = cambio(0, distancia * 2.5, angulo, centrox, centroy)       
    x2, y2 = cambio(-distancia * 2, -distancia * 2.5, angulo, centrox, centroy)  
    x3, y3 = cambio(distancia * 2, -distancia * 2.5, angulo, centrox, centroy)  
    if guardar:
        guardar_formas.append((4, (x1, y1, x2, y2, x3, y3), colores))
    return x1,y1,x2,y2,x3,y3

while captura.isOpened():  #bucle principal de captura de video
    exito, foto = captura.read()
    foto = cv2.flip(foto, 1)
    if not exito: break
    imagen_con_dibujos = foto.copy()
    # print("Opción actual:", seleccion) # Comentado para no saturar consola
    if canvas is None: canvas = np.zeros_like(foto)  # inicializar el lienzo con el mismo tamaño que el cuadro 

    alto, ancho = foto.shape[:2] 
    color_texto = (255, 255, 255) 
    fuente = cv2.FONT_HERSHEY_SIMPLEX

  
    # Rectángulo (Opción 2)
    cv2.putText(imagen_con_dibujos, "REC", (110, 75), fuente, 0.7, color_texto, 2)
    # Círculo (Opción 3)
    cv2.putText(imagen_con_dibujos, "CIR", (195, 75), fuente, 0.7, color_texto, 2)
    # Triángulo (Opción 4)
    cv2.putText(imagen_con_dibujos, "TRI", (280, 75), fuente, 0.7, color_texto, 2)
    # Línea (Opción 5)
    cv2.putText(imagen_con_dibujos, "LIN", (365, 75), fuente, 0.7, color_texto, 2)
    # Estrella (Opción 10)
    cv2.putText(imagen_con_dibujos, "EST", (450, 75), fuente, 0.7, color_texto, 2)
    # Pincel/Lápiz (Opción 1)
    cv2.putText(imagen_con_dibujos, "PIN", (30, 75), fuente, 0.7, color_texto, 2)

    # Paleta de colores (DERECHA)
    # Posicion
    opx1 = ancho - 110 # Límite izquierdo de detección
    opx2 = ancho - 20  # Límite derecho de detección

    # base
    centro_paleta = (ancho - 65, 265)
    # Óvalo forma
    cv2.ellipse(imagen_con_dibujos, centro_paleta, (55, 245), 0, 0, 360, (180, 215, 245), -1)
    # Borde del óvalo
    cv2.ellipse(imagen_con_dibujos, centro_paleta, (55, 245), 0, 0, 360, (100, 140, 190), 2)
    # Agujero
    cv2.circle(imagen_con_dibujos, (ancho - 65, 510), 20, (10, 10, 10), -1) 

    # Colores
    puntos_colores = [
        (65, (0, 255, 0)),    # Verde
        (145, (0, 0, 255)),   # Rojo
        (225, (255, 0, 140)), # Morado
        (305, (0, 136, 255)), # Naranja
        (385, (0, 255, 255)), # Amarillo
        
    ]

    for y_pos, col in puntos_colores:
        # Dibujar colores como círculos
        cv2.circle(imagen_con_dibujos, (ancho - 65, y_pos), 28, col, -1)
        # Efecto de brillo para que parezca pintura real
        cv2.circle(imagen_con_dibujos, (ancho - 75, y_pos - 10), 6, (255, 255, 255), -1)
        
        # Resaltar si el color está seleccionado actualmente
        if colores == col:
            cv2.circle(imagen_con_dibujos, (ancho - 65, y_pos), 33, (255, 255, 255), 3)
  
    
    # Iconos Izquierda
    cv2.putText(imagen_con_dibujos, "DEL", (35, 200), fuente, 0.6, (255, 255, 255), 2) # Borrar lienzo
    cv2.putText(imagen_con_dibujos, "CLR", (35, 285), fuente, 0.6, (255, 255, 255), 2) # Limpiar figuras

    hsv = cv2.cvtColor(foto, cv2.COLOR_BGR2HSV)
    mascara = cv2.inRange(hsv, np.array([100, 80, 40]), np.array([140, 255, 255])) # detección azul, donde haya un 1 en la mascara, se pintará
   # Procesamiento de la imagen para la detección de manos
    imagen_analizada = cv2.cvtColor(foto, cv2.COLOR_BGR2RGB)
    observacion_manos = manos_deteccion.process(imagen_analizada)


    if observacion_manos.multi_hand_landmarks and observacion_manos.multi_handedness: # si se detectan manos entras
        for marcas_manos, lateralidad in zip(observacion_manos.multi_hand_landmarks, observacion_manos.multi_handedness):# recorrer las manos detectadas
            guardar = False # bandera para guardar la forma
            quien_cual = lateralidad.classification[0].label # izquierda o derecha
            if not mano_guardar:
                mano_de_control = quien_cual
                mano_guardar = True
                
            mediap_dibujo.draw_landmarks(imagen_con_dibujos, marcas_manos, mediap_manos.HAND_CONNECTIONS)# dibujar puntos y conexiones de la mano
            pulgar = marcas_manos.landmark[4]
            pulgar_nudillo = marcas_manos.landmark[3] # nudillo del pulgar para detectar si está doblado
            indice = marcas_manos.landmark[8] 
            indice_nudillo = marcas_manos.landmark[5] 
            
            if quien_cual == mano_de_control:
                pulgar_donde_x, pulgar_donde_y = int(pulgar.x * ancho), int(pulgar.y * alto)
                indice_donde_x, indice_donde_y = int(indice.x * ancho), int(indice.y * alto)
                
            if quien_cual != mano_de_control:
                # El pulgar está arriba si su punta (4) es más alta en pantalla que su base (3)
                if pulgar.y < pulgar_nudillo.y and pulgar.y < indice_nudillo.y:
                    guardar = True
            
            # Detección de zonas
            if 30 < indice_donde_y < 100: 
                if 30 < indice_donde_x < 100: seleccion = 1
                elif 110 < indice_donde_x < 180: seleccion = 2
                elif 190 < indice_donde_x < 260: seleccion = 3
                elif 270 < indice_donde_x < 340: seleccion = 4
                elif 350 < indice_donde_x < 420: seleccion = 5
                elif 430 < indice_donde_x < 500: seleccion = 10
                
            if opx1 < indice_donde_x < opx2: 
                if 30 < indice_donde_y < 100: colores = (0, 255, 0)
                elif 110 < indice_donde_y < 180: colores = (0, 0, 255)
                elif 190 < indice_donde_y < 260: colores = (255, 0, 140)
                elif 270 < indice_donde_y < 340: colores = (0, 136, 255)
                elif 350 < indice_donde_y < 420: colores = (0, 255, 255)
                elif 430 < indice_donde_y < 500: colores = (255, 0, 0)

            if 30 < indice_donde_x < 100: 
                if 160 < indice_donde_y < 230: seleccion = 7 # DEL (Borrar lienzo)
                elif 240 < indice_donde_y < 310: seleccion = 6 # CLR (Borrar historial)
                elif 320 < indice_donde_y < 390: seleccion = 1
                
            # Dibujar según la selección modo fantasma
            if seleccion==2:
                x1,y1,x2,y2,x3,y3,x4,y4=rectangulo(pulgar_donde_x,pulgar_donde_y,indice_donde_x,indice_donde_y,guardar)
                for p in [(x1,y1,x3,y3), (x2,y2,x4,y4), (x1,y1,x4,y4), (x2,y2,x3,y3)]:
                    cv2.line(imagen_con_dibujos, (p[0],p[1]), (p[2],p[3]), colores, 3)
            if seleccion==3:
                cx,cy,dist=circulo(pulgar_donde_x,pulgar_donde_y,indice_donde_x,indice_donde_y,guardar)
                cv2.circle(imagen_con_dibujos,(cx,cy),int(dist*1.1),colores,3)
            if seleccion==4:
                x1,y1,x2,y2,x3,y3=triangulo(pulgar_donde_x,pulgar_donde_y,indice_donde_x,indice_donde_y,guardar)
                cv2.line(imagen_con_dibujos,(x1,y1),(x3,y3),colores,3); cv2.line(imagen_con_dibujos,(x2,y2),(x1,y1),colores,3); cv2.line(imagen_con_dibujos,(x2,y2),(x3,y3),colores,3)
            if seleccion==5:
                x1,y1,x2,y2 = linea(pulgar_donde_x,pulgar_donde_y,indice_donde_x,indice_donde_y, guardar)
                cv2.line(imagen_con_dibujos, (x2, y2), (x1, y1), colores, 3)
            if seleccion == 10:
                p = estrella(pulgar_donde_x, pulgar_donde_y, indice_donde_x, indice_donde_y, guardar)
                for i in range(10): cv2.line(imagen_con_dibujos, p[i], p[(i+1)%10], colores, 3)
            if seleccion==6: guardar_formas.clear()
            if seleccion==7: canvas[:] = 0 
            
    else: mano_guardar=False     
   
    if seleccion in [0,1]:
        coordenadas = np.column_stack(np.where(mascara==255)) # obtener coordenadas donde la máscara es blanca
        for y,x in coordenadas:
            if seleccion==1: canvas[y,x] = colores # pintar en el lienzo

    fusion = cv2.addWeighted(imagen_con_dibujos, 0.7, canvas, 0.3, 0) #donde multiplicamos para ver el lienzo
    
    for fig in guardar_formas: # dibujar las formas guardadas
        tipo, coordenadas, col = fig
        if tipo == 2: 
            cv2.line(fusion,(coordenadas[0],coordenadas[1]),(coordenadas[4],coordenadas[5]),col,3); cv2.line(fusion,(coordenadas[2],coordenadas[3]),(coordenadas[6],coordenadas[7]),col,3)
            cv2.line(fusion,(coordenadas[0],coordenadas[1]),(coordenadas[6],coordenadas[7]),col,3); cv2.line(fusion,(coordenadas[2],coordenadas[3]),(coordenadas[4],coordenadas[5]),col,3)
        elif tipo == 3: cv2.circle(fusion,(coordenadas[0],coordenadas[1]),int(coordenadas[2]),col,3)
        elif tipo == 4:
            cv2.line(fusion,(coordenadas[0],coordenadas[1]),(coordenadas[4],coordenadas[5]),col,3); cv2.line(fusion,(coordenadas[2],coordenadas[3]),(coordenadas[0],coordenadas[1]),col,3); cv2.line(fusion,(coordenadas[2],coordenadas[3]),(coordenadas[4],coordenadas[5]),col,3)
        elif tipo == 5: cv2.line(fusion,(coordenadas[0],coordenadas[1]),(coordenadas[2],coordenadas[3]),col,3) #mandar puntos de linea
        elif tipo == 10:
            for i in range(10): cv2.line(fusion, coordenadas[i], coordenadas[(i+1)%10], col, 3)

    cv2.imshow("Paint Pro", fusion)
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("Paint Pro", cv2.WND_PROP_VISIBLE) < 1: break

captura.release()
cv2.destroyAllWindows()