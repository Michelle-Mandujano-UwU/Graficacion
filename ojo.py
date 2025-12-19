# Programa para dibujar un ojo 3D con OpenGL en Python añadiendo detalles rojos de venas y nervio óptico.

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Esta variable controla qué tan rápido da vueltas el ojo
rotacion_ojo = 0.0

def dibujar_esfera(radio, divisiones_h=30, divisiones_v=30):
    """ 
    Crea una bola desde cero usando coordenadas polares.
    Es la base para el globo ocular, el iris y la pupila.
    """
    for i in range(divisiones_v):
        lat1 = math.pi * (-0.5 + i / divisiones_v)
        lat2 = math.pi * (-0.5 + (i + 1) / divisiones_v)
        
        glBegin(GL_QUAD_STRIP) # Dibuja tiras de quads
        for j in range(divisiones_h + 1):
            lng = 2 * math.pi * j / divisiones_h
            x1 = math.cos(lat1) * math.cos(lng)
            y1 = math.sin(lat1)
            z1 = math.cos(lat1) * math.sin(lng)
            x2 = math.cos(lat2) * math.cos(lng)
            y2 = math.sin(lat2)
            z2 = math.cos(lat2) * math.sin(lng)
            
            glNormal3f(x1, y1, z1)
            glVertex3f(x1 * radio, y1 * radio, z1 * radio)
            
            glNormal3f(x2, y2, z2)
            glVertex3f(x2 * radio, y2 * radio, z2 * radio)
        glEnd()

def dibujar_venas(radio, divisiones_h=30, divisiones_v=10):
    """
    Dibuja esas ramificaciones rojas sobre el blanco del ojo que simulan las venas.
    """
    glColor3f(0.8, 0.0, 0.0) # Rojo para las venas
    
    for i in range(divisiones_v): 
        lat1 = math.pi * (-0.5 + i / divisiones_v)
        lat2 = math.pi * (-0.5 + (i + 1) / divisiones_v)
        
        glLineWidth(2)
        glBegin(GL_LINE_STRIP)
        
        for j in range((divisiones_h + 1)//3): # Solo un tercio para simular las venas
            lng = 2 * math.pi * j / divisiones_h
            x1 = math.cos(lat1) * math.cos(lng)
            y1 = math.sin(lat1)
            z1 = math.cos(lat1) * math.sin(lng)
            
            glNormal3f(x1, y1, z1)
            glVertex3f(x1 * radio, y1 * radio, z1 * radio)
            
        for j in range((divisiones_h + 1)//3): # Otro tercio para otra vena
            j = j + (2 * (divisiones_h + 1) // 3)
            lng = 2 * math.pi * j / divisiones_h
            x1 = math.cos(lat1) * math.cos(lng)
            y1 = math.sin(lat1)
            z1 = math.cos(lat1) * math.sin(lng)
            
            glNormal3f(x1 // 4, y1 // 4, z1)
            glVertex3f(x1 * radio, y1 * radio, z1 * radio)
        glEnd()

def dibujar_cilindro(radio):
    """ 
    Dibuja el nervio de atrás del ojo como un cilindro rojo.
    """
    glColor3f(0.8, 0.0, 0.0) 
    glBegin(GL_TRIANGLE_STRIP) # Cilindro simple
    for i in range(0, 361):
        angulo = math.radians(i)
        x1 = math.cos(angulo)
        y1 = math.sin(angulo)
        z1 = 0.5
        glNormal3f(x1, y1, 0)
        glVertex3f(x1 * radio, y1 * radio, z1)
        glNormal3f(x1, y1, 0)
        glVertex3f((x1 * radio), (y1 * radio), (z1 * 2))
    glEnd()

def dibujar_ojo_completo():
    """ Ensamblaje final de todas las partes """
    glPushMatrix()
   
    # 1. Base trasera 
    glColor3f(0.7, 0.0, 0.0) 
    glPushMatrix()
    glTranslatef(0.7, 0, 0)
    dibujar_esfera(0.54, 30, 30)
    glPopMatrix()
    
    # 2. El nervio/cilindro (Rojo)
    glPushMatrix()
    glRotate(90, 0, 1, 0)
    glTranslate(0, 0, 0.54)
    dibujar_cilindro(0.2)
    glPopMatrix()

    # 3. Lo blanco del ojo con sus venas rojas
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(0.56, 0, 0)
    dibujar_esfera(0.6, 30, 30)
    dibujar_venas(0.61) 
    glPopMatrix()
    
    # 4. Iris (Azul)
    glColor3f(0.2, 0.4, 0.8)
    glPushMatrix()
    glTranslatef(0.49, 0, 0)
    dibujar_esfera(0.55, 30, 30)
    glPopMatrix()

    # 5. Pupila (Negro)
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0.3, 0, 0)
    dibujar_esfera(0.4, 30, 30)
    glPopMatrix()

    glPopMatrix()

def configurar_iluminacion():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    
    posicion_luz = [1.0, 1.0, 1.0, 0.2]
    glLightfv(GL_LIGHT0, GL_POSITION, posicion_luz)

def ejecutar_programa():
    global rotacion_ojo # Variable global para rotar el ojo
    
    if not glfw.init(): # Inicialización de GLFW
        return

    ventana = glfw.create_window(800, 600, "Ojo 3D", None, None)
    if not ventana:
        glfw.terminate()
        return

    glfw.make_context_current(ventana)
    glClearColor(0.05, 0.05, 0.05, 1.0) # Fondo muy oscuro para apreciar mejor
    configurar_iluminacion()

    while not glfw.window_should_close(ventana): # Loop principal
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_PROJECTION) # Configuración de la cámara perspectiva 
        glLoadIdentity()
        gluPerspective(45, 800/600, 0.1, 100.0)
        
        glMatrixMode(GL_MODELVIEW) # Vista de la cámara
        glLoadIdentity()
        glTranslatef(0, 0, -5)
        
        rotacion_ojo += 0.7 # Un poco más rápido para ver el detalle rojo atrás
        glRotatef(rotacion_ojo, 0, 1, 0) 
        
        dibujar_ojo_completo()
        
        glfw.swap_buffers(ventana)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    ejecutar_programa()