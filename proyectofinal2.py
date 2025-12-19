# Proyecto Final 2 - Filtro Diablo raro loquillo
# Es un filtro de diablo con cuernos, ojos locos y lengua utilizando OpenGL y MediaPipe.
# Es un  filtro tipo snapchat que superpone gráficos 3D sobre la cara detectada en tiempo real.
import glfw
import cv2
import mediapipe as mp
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Configuración de la ventana
ANCHO_VENTANA, ALTO_VENTANA = 640, 480
filtro = "Proyecto Final - Filtro de diablo loquillo"

def iniciarGraf():
    if not glfw.init(): # Inicializar GLFW para crear ventana
        print("No se pudo iniciar GLFW")
        return None
    
    win = glfw.create_window(ANCHO_VENTANA, ALTO_VENTANA, filtro, None, None) # Crear ventana GLFW
    if not win:
        glfw.terminate()
        return None
     
    glfw.make_context_current(win)
    glfw.swap_interval(1) # Espera a que el monitor termine de dibujar un cuadro antes de enviarle el siguiente
    return win

def ajustes(): # Configurar parámetros de dibujo
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def lienzo(): # Preparar textura para video
    id_tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, id_tex)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return id_tex

def corregir_coordenadas(punto):
   # Ajustar coordenadas de MediaPipe a OpenGL
    return ((punto.x - 0.5) * 2, -2 * (punto.y - 0.5), (punto.z) * 2)

# Dibujar objetos del filtro

def cuernito(x, y, z, lado="izquierdo"):
    # Dibuja un cuerno en la posición dada
    glPushMatrix()
    glTranslatef(x, y, z)
    # Ajuste de rotación para cuernos
    glRotatef(-20 if lado=="izquierdo" else 20, 0, 0, 1)
    glRotatef(-110, 1, 0, 0) 
    glColor3f(0.8, 0.0, 0.0) 
    figura = gluNewQuadric()
    # Dibujar cono
    gluCylinder(figura, 0.03, 0.0, 0.15, 16, 16) 
    glPopMatrix()

def lengua(x, y_sup, y_inf, z, apertura):

    apertura_max = min(apertura, 0.07) # Limitar apertura máxima para evitar exagerar y ya no parezca lengua
    if apertura_max < 0.02: return # Si la boca está casi cerrada, no dibujar lengua
    punto_medio_y = (y_sup + y_inf) / 2 # Calcular punto medio en Y para centrar la lengua justo de donde debe de salir
    
    glPushMatrix()
    # El z + 0.02 es para que no parpadee con la textura del fondo
    glTranslatef(x, punto_medio_y, z + 0.02)
    # Inclinación leve hacia adelante para dar efecto de profundidad
    glRotatef(15, 1, 0, 0) 
    # El grosor Y para que no choque con los labios
    ancho = 0.04
    grosor = apertura_max * 0.4  # Se vuelve más gruesa si abres más la boca
    largo = apertura_max * 6.0    # Crecimiento que parezca como si saliera de la camara
    glScalef(ancho, grosor, largo)
    glTranslatef(0, 0, 1.0) # Mueve la esfera para que crezca desde la base hacia afuera
    glColor3f(1.0, 0.1, 0.2) 
    
    esfera = gluNewQuadric() # Crear esfera para lengua
    gluSphere(esfera, 1, 32, 32) 
    glPopMatrix()

def ojos(x, y, z):
    # Globo ocular
    glColor3f(1, 1, 1)
    glPushMatrix() # Guardar estado actual
    glTranslatef(x, y, z)
    ojo = gluNewQuadric() # Crear esfera para ojo
    gluSphere(ojo, 0.025, 16, 16) #  Globo blanco
    glPopMatrix()
    
    # Pupila
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(x, y, z + 0.015) # Mover un poco hacia adelante para que no se vea dentro del globo y parezca loquillo
    gluSphere(ojo, 0.01, 16, 16)
    glPopMatrix()

def fondo(img_rgb, textur, parpadeando):
    glDisable(GL_DEPTH_TEST)
    if parpadeando:
        glClearColor(0.8, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
    else: 
        glClearColor(0.0, 0.0, 0.0, 1.0) # Fondo negro
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 1, 0, 1) 
        glMatrixMode(GL_MODELVIEW) # Volver a modelo vista
        glPushMatrix()
        glLoadIdentity()
        # Convertimos la imagen de la cámara en una textura de OpenGL
        glBindTexture(GL_TEXTURE_2D, textur) # Enlazar textura
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_rgb.shape[1], img_rgb.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, img_rgb) # Cargar imagen de la cámara como textura
        
        glEnable(GL_TEXTURE_2D)
        glBegin(GL_QUADS) # Dibujar cuadrado con textura de cámara
        glTexCoord2f(0, 1); glVertex2f(0, 0)
        glTexCoord2f(1, 1); glVertex2f(1, 0)
        glTexCoord2f(1, 0); glVertex2f(1, 1)
        glTexCoord2f(0, 0); glVertex2f(0, 1)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        # Limpiar y regresamr al modo 3D para los cuernos y lengua
        glPopMatrix() # Restaurar estado anterior
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

def ejecutar():
    ventana = iniciarGraf() # Iniciar ventana OpenGL
    if not ventana: return
    ajustes()
    id_tex = lienzo()
    
    cara = mp.solutions.face_mesh 
    malla = cara.FaceMesh(refine_landmarks=True) # Activar detección facial con refinamiento de puntos clave
    cap = cv2.VideoCapture(0)

    while not glfw.window_should_close(ventana):
        ret, frame = cap.read()
        if not ret: break
        
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Convertir a RGB para MediaPipe
        res = malla.process(rgb)

        parp = False # Variable para detectar parpadeo
        if res.multi_face_landmarks:
            p = res.multi_face_landmarks[0].landmark
            if abs(p[159].y - p[145].y) < 0.007 and abs(p[386].y - p[374].y) < 0.007:
                parp = True

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Limpiar buffers
        fondo(rgb, id_tex, parp)

        if res.multi_face_landmarks:
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            gluPerspective(45, ANCHO_VENTANA/ALTO_VENTANA, 0.1, 100)
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()
            gluLookAt(0, 0, 2, 0, 0, 0, 0, 1, 0)
            
            p = res.multi_face_landmarks[0].landmark # Obtener puntos faciales

            # Dibujar los elementos del filtro
            # Cuernos
            cx_i, cy_i, cz_i = corregir_coordenadas(p[103])
            cx_d, cy_d, cz_d = corregir_coordenadas(p[332])
            cuernito(cx_i, cy_i, cz_i, "izquierdo")
            cuernito(cx_d, cy_d, cz_d, "derecho")

            # Ojos
            ox_i, oy_i, oz_i = corregir_coordenadas(p[468])
            ox_d, oy_d, oz_d = corregir_coordenadas(p[473])
            ojos(ox_i, oy_i, oz_i)
            ojos(ox_d, oy_d, oz_d)

            # Lengua
            ls_x, ls_y, ls_z = corregir_coordenadas(p[13])
            li_x, li_y, li_z = corregir_coordenadas(p[14])
            separacion = abs(ls_y - li_y)

            # Pasamos labio superior y labio inferior para calcular el centro
            lengua(li_x, ls_y, li_y, li_z, separacion)

            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)

        glfw.swap_buffers(ventana)
        glfw.poll_events()

    cap.release()
    glfw.terminate()

if __name__ == "__main__":
    ejecutar()