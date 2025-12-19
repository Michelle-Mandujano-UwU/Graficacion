# Este código crea una escena 3D simple usando OpenGL y GLFW para dibujar un cerdito.
# El cerdito está compuesto por varias esferas.
# Se aplican transformaciones geométricas para posicionar y escalar las partes del cerdito.
# Incluye iluminación básica.
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# rotación de la escena
rotacion_escena = 0.0

def dibujar_esfera(radio, rebanadas=30, pilas=30):
    """Dibuja una esfera usando mallas de cuadriláteros"""
    for i in range(pilas): # De polo a polo
        latitud1 = math.pi * (-0.5 + i / pilas)
        latitud2 = math.pi * (-0.5 + (i + 1) / pilas)
        # Dibujar una tira de cuadriláteros entre las dos latitudes
        glBegin(GL_QUAD_STRIP)
        for j in range(rebanadas + 1):
            longitud = 2 * math.pi * j / rebanadas# Longitud va de 0 a 2PI
            
            # Punto 1
            x1 = math.cos(latitud1) * math.cos(longitud)
            y1 = math.sin(latitud1)
            z1 = math.cos(latitud1) * math.sin(longitud)
            
            # Punto 2
            x2 = math.cos(latitud2) * math.cos(longitud)
            y2 = math.sin(latitud2)
            z2 = math.cos(latitud2) * math.sin(longitud)
            
            glNormal3f(x1, y1, z1)
            glVertex3f(x1 * radio, y1 * radio, z1 * radio) # Punto en la superficie
            
            glNormal3f(x2, y2, z2)
            glVertex3f(x2 * radio, y2 * radio, z2 * radio)
        glEnd()

def dibujar_detalle_circular(radio, grados, grosor):
    """Dibuja una línea circular"""
    glLineWidth(grosor)
    glBegin(GL_LINE_STRIP)
    for i in range(0, grados): # De 0 a 'grados'
        angulo = math.radians(i)
        x = math.cos(angulo) * radio 
        y = math.sin(angulo) * radio
        glVertex3f(x, y, 0)
    glEnd()

def dibujar_cerdito():
    """Transformaciones geometricas para el cerdito"""
    
    # cuerpo panzon
    glColor3f(1.0, 0.7, 0.75) # Rosado claro
    glPushMatrix()
    glScalef(1.2, 1.0, 1.0) # Alargar un poco el cuerpo
    dibujar_esfera(1.0)
    glPopMatrix()

    # cabeza
    glPushMatrix()
    glTranslatef(0.8, 0.3, 0)
    dibujar_esfera(0.6)
    
    # nariz
    glColor3f(1.0, 0.5, 0.6) # Rosado más fuerte
    glPushMatrix()
    glTranslatef(0.5, -0.1, 0)
    glScalef(0.4, 0.4, 0.6)
    dibujar_esfera(0.5)
    glPopMatrix()

    # ojos
    glColor3f(0, 0, 0) # Negro
    # derecho
    glPushMatrix()
    glTranslatef(0.4, 0.3, 0.3)
    dibujar_esfera(0.08)
    glPopMatrix()
    # izquierdo
    glPushMatrix()
    glTranslatef(0.4, 0.3, -0.3)
    dibujar_esfera(0.08)
    glPopMatrix()
    
    glPopMatrix() 

    # patas
    glColor3f(1.0, 0.6, 0.7)
    #esferas pequeñas para patas
    posiciones_patas = [
        (0.5, -0.8, 0.4), (-0.5, -0.8, 0.4),
        (0.5, -0.8, -0.4), (-0.5, -0.8, -0.4)
    ]
    for pos in posiciones_patas:
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        dibujar_esfera(0.25)
        glPopMatrix()

    # orejas
    glPushMatrix()
    glTranslatef(1.0, 0.8, 0.3)
    glRotatef(-30, 0, 0, 1)
    glScalef(0.1, 0.3, 0.2)
    dibujar_esfera(0.8)
    glPopMatrix()

    # esferas aplastadas para orejas
    glPushMatrix()
    glTranslatef(1.0, 0.8, -0.3)
    glRotatef(-30, 0, 0, 1)
    glScalef(0.1, 0.3, 0.2)
    dibujar_esfera(0.8)
    glPopMatrix()

def configurar_iluminacion():
    """Configuracion de luces"""
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    
    posicion_luz = [2.0, 2.0, 2.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, posicion_luz) # Luz en posición
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])

def main():
    global rotacion_escena
    
    if not glfw.init():
        return

    ventana = glfw.create_window(800, 600, "Cerdito usando OpenGL", None, None)
    if not ventana:
        glfw.terminate()
        return

    glfw.make_context_current(ventana) # Hacer el contexto actual
    glClearColor(0.2, 0.5, 0.2, 1.0) # Fondo verde
    configurar_iluminacion()

    while not glfw.window_should_close(ventana):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Configuración de Cámara
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800/600, 0.1, 100.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(5, 3, 5,  # Dónde está la cámara
                  0, 0, 0,  # A dónde mira
                  0, 1, 0)  # Vector hacia arriba
        
        # Rotar el cerdito continuamente
        rotacion_escena += 0.7
        glRotatef(rotacion_escena, 0, 1, 0) 
        
        dibujar_cerdito()
        
        glfw.swap_buffers(ventana)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()