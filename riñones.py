# Este codigo crea un objeto en 3D de unos riñones utilizando OpenGL y GLFW. Formado por primitivas ( esferas y cilindros)

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

angulito = 0.0 # Angulo de rotacion
velA = 0.05 # Velocidad de rotacion

def luces():
    # Lo de siempre para que no se vea plano
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glLightfv(GL_LIGHT0, GL_POSITION, [3, 4, 8, 1]) # Luz desde arriba a la derecha

def bolitas(r, col): # La masa del riñon
    q = gluNewQuadric()
    # Le quito el brillo porque si no parece de metal
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0, 0, 0, 1])
    glColor3f(*col)
    gluSphere(q, r, 30, 30) # Hacemos una esfera

def palitos(r, largo, col): # para las cositas cafes
    q = gluNewQuadric()
    glColor3f(*col)
    gluCylinder(q, r, r, largo, 15, 15) # Hacemos un cilindro

def rinon(derecha=False):
    inv = -1 if derecha else 1
    rojo_oscuro = (0.7, 0.1, 0.1)
    color_tubo = (0.4, 0.25, 0.1)
    glPushMatrix()
    for y_pos in [0.35, -0.35]: # Las dos bolitas de arriba y abajo
        glPushMatrix()
        glTranslatef(0, y_pos, 0)
        bolitas(0.28, rojo_oscuro)
        glPopMatrix()

    # La de en medio, un poco aplastada para que de la forma
    glPushMatrix()
    glTranslatef(-0.07 * inv, 0, 0)
    glScalef(1.25, 0.95, 1.0)
    bolitas(0.3, rojo_oscuro)
    glPopMatrix()
   
    for alt in [0.1, -0.1]:  # Los dos palitos cafes horizontales
        glPushMatrix()
        glTranslatef(0.12 * inv, alt, 0)
        glRotatef(90 * inv, 0, 1, 0)
        palitos(0.04, 0.4, color_tubo)
        glPopMatrix()

    # El tubo que baja que no se que es
    glPushMatrix()
    glTranslatef(0.4 * inv, -0.05, 0)
    glRotatef(100, 1, 0, 0)
    palitos(0.022, 0.8, color_tubo)
    glPopMatrix()

    glPopMatrix()

def main(): # Funcion principal
    global angulito
    
    if not glfw.init():
        return

    ventana = glfw.create_window(800, 800, "riñon", None, None) 
    glfw.make_context_current(ventana)
    # Fondo azul clarito
    glClearColor(0.6, 0.7, 0.85, 1.0)
    luces()

    while not glfw.window_should_close(ventana): # 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1.0, 0.1, 60.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -4.2) 
        
        # Animacion de rotacion
        glRotatef(angulito, 0, 1, 0)
        angulito += velA

        # El de la izquierda
        glPushMatrix()
        glTranslatef(-0.8, 0, 0)
        glRotatef(12, 0, 0, 1)
        rinon(False)
        glPopMatrix()

        # El de la derecha va espejado
        glPushMatrix()
        glTranslatef(0.8, 0, 0)
        glRotatef(-12, 0, 0, 1)
        glScalef(-1, 1, 1) 
        rinon(False)
        glPopMatrix()

        glfw.swap_buffers(ventana)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()