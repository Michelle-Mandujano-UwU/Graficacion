
# Este programa crea una ventana usando GLFW y dibuja una
# piramide 3D con base triangular (un tetraedro). La piramide
# gira poco a poco gracias a un angulo que se va incrementando.
# Se usa OpenGL para todo el dibujo en 3D y como base tome el
# codigo de rotar un cuadrado en 3D visto en clase.

import glfw
from OpenGL.GL import glClearColor, glEnable, glClear, glLoadIdentity, glTranslatef, glRotatef, glMatrixMode
from OpenGL.GL import glBegin, glColor3f, glVertex3f, glEnd, glFlush, glViewport
from OpenGL.GL import GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_TRIANGLES
from OpenGL.GL import GL_PROJECTION, GL_MODELVIEW
from OpenGL.GLU import gluPerspective
import sys

# Variables globales
ventana = None         # Para guardar la ventana creada por GLFW
angulo = 0             # Angulo para hacer girar la piramide cada cuadro

def init():
    # Configura el color de fondo de la pantalla (negro)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    # Activa el buffer de profundidad para el dibujo 3D
    glEnable(GL_DEPTH_TEST)

    # Cambia a la matriz de proyeccion (camara)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()   # Reinicia la matriz de proyeccion

    # Crea perspectiva tipo camara
    gluPerspective(45, 1.0, 0.1, 50.0)

    # Cambia a la matriz de modelo (donde se dibujan objetos)
    glMatrixMode(GL_MODELVIEW)

def draw_pyramid():   # dibujar piramide
    global angulo

    # Limpia la pantalla: color y profundidad
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Reinicia la matriz de modelo
    glLoadIdentity()

    # Aleja la camara para que el objeto se vea
    glTranslatef(0.0, 0.0, -6)

    # Rota la piramide segun el angulo actual
    glRotatef(angulo, 1, 1, 1)

    # Base (triangulo)
    b1 = (-1, -1,  1)
    b2 = ( 1, -1,  1)
    b3 = ( 0, -1, -1)

    # Vértice de arriba
    px, py, pz = (0, 1.2, 0)

    # Inicia para dibujar triangulos
    glBegin(GL_TRIANGLES)

    # Cara 1: la base
    glColor3f(1.0, 0.0, 0.0)   # Rojo
    glVertex3f(*b1)
    glVertex3f(*b2)
    glVertex3f(*b3)

    # Cara 2: lado verde
    glColor3f(0.0, 1.0, 0.0)   # Verde
    glVertex3f(*b1)
    glVertex3f(*b2)
    glVertex3f(px, py, pz)

    # Cara 3 : lado azul
    glColor3f(0.0, 0.0, 1.0)   # Azul
    glVertex3f(*b2)
    glVertex3f(*b3)
    glVertex3f(px, py, pz)

    # Cara 4 : lado amarillo
    glColor3f(1.0, 1.0, 0.0)   # Amarillo
    glVertex3f(*b3)
    glVertex3f(*b1)
    glVertex3f(px, py, pz)

    glEnd()    # Termina el dibujo
    glFlush()  # Fuerza a OpenGL a dibujar ya

    # Intercambia los buffers para animacion suave
    glfw.swap_buffers(ventana)

    # Aumenta el angulo para que gire un poquito cada frame
    angulo += 0.1

def main():
    global ventana

    # Inicializa GLFW
    if not glfw.init():
        sys.exit()

    # Tamaño de la ventana
    ancho, alto = 500, 500

    # Crea la ventana
    ventana = glfw.create_window(ancho, alto, "Piramide 3D", None, None)

    # Si no se pudo crear, salir
    if not ventana:
        glfw.terminate()
        sys.exit()

    # Indica que esta ventana usara OpenGL
    glfw.make_context_current(ventana)

    # Define el area de dibujo
    glViewport(0, 0, ancho, alto)

    # Llama a la configuracion inicial de OpenGL
    init()

    # Bucle principal de la ventana
    while not glfw.window_should_close(ventana):
        draw_pyramid()        # Dibuja la piramide
        glfw.poll_events() # Revisa eventos del teclado/ventana

    # Cuando se cierra la ventana, terminar GLFW
    glfw.terminate()

if __name__ == "__main__":
    main()

