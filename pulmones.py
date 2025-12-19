# Simulación de un sistema pulmonar 3D con OpenGL
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Variables globales para la animación
giro_escena = 0.0
ritmo_respiracion = 0.0

def dibujar_forma_esferica(radio, seg_h=30, seg_v=30):
    """ Crea la geometría base para los pulmones """
    for i in range(seg_v):
        lat1 = math.pi * (-0.5 + i / seg_v)
        lat2 = math.pi * (-0.5 + (i + 1) / seg_v)
        glBegin(GL_QUAD_STRIP)
        for j in range(seg_h + 1):
            lng = 2 * math.pi * j / seg_h
            for lat in [lat1, lat2]:
                x = math.cos(lat) * math.cos(lng)
                y = math.sin(lat)
                z = math.cos(lat) * math.sin(lng)
                glNormal3f(x, y, z)
                glVertex3f(x * radio, y * radio, z * radio)
        glEnd()

def dibujar_tubo(radio, largo):
    """ Crea los bronquios y la tráquea """
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(0, 361):
        angulo = math.radians(i)
        x = math.cos(angulo)
        y = math.sin(angulo)
        glNormal3f(x, y, 0)
        glVertex3f(x * radio, y * radio, 0)
        glVertex3f(x * radio, y * radio, largo)
    glEnd()

def dibujar_sistema_pulmonar():
    global ritmo_respiracion
    
    # Calculamos el factor de inflado (oscila entre 1.0 y 1.1)
    # Para que parezca que están respirando
    inflado = 1.0 + (math.sin(ritmo_respiracion) * 0.05)
    
    glPushMatrix()
    
    # Dibujar la tráquea
    glColor3f(0.9, 0.8, 0.7) # Color hueso/cartílago
    glPushMatrix()
    glRotatef(-90, 1, 0, 0) # vertical
    glTranslatef(0, 0, 0.5)
    dibujar_tubo(0.15, 1.2)
    glPopMatrix()

    # pulmon izquierdo
    glColor3f(0.9, 0.5, 0.5) # Color rosado para los pulmones
    glPushMatrix()
    glTranslatef(-0.6, 0.5, 0)
    # estiramos la esfera en el eje Y para que parezca pulmón
    glScalef(0.8 * inflado, 1.5 * inflado, 0.7 * inflado)
    dibujar_forma_esferica(0.5)
    glPopMatrix()

    # pulmon derecho
    glPushMatrix()
    glTranslatef(0.6, 0.5, 0)
    glScalef(0.8 * inflado, 1.5 * inflado, 0.7 * inflado)
    dibujar_forma_esferica(0.5)
    glPopMatrix()

    glPopMatrix()

def configurar_luces(): # Configuración básica de luces
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 2.0, 1.0])

def main():
    global giro_escena, ritmo_respiracion
    
    if not glfw.init():
        return

    ventana = glfw.create_window(800, 600, "Pulmones 3D", None, None)
    if not ventana:
        glfw.terminate()
        return

    glfw.make_context_current(ventana)
    glClearColor(0.0, 0.0, 0.0, 1.0) # Fondo Negro
    configurar_luces()

    while not glfw.window_should_close(ventana):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800/600, 0.1, 100.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, -0.5, -5) # Bajamos un poco la cámara
        
        # Rotación automática para ver el modelo en 3D
        giro_escena += 0.5
        glRotatef(giro_escena, 0, 1, 0)
        
        # Aumentamos el tiempo de respiración
        ritmo_respiracion += 0.05
        
        dibujar_sistema_pulmonar()
        
        glfw.swap_buffers(ventana)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()