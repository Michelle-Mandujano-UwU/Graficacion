# En este programa se dibujan tres figuras geométricas utilizando OpenGL:
# un triángulo, un triángulo invertido y un cuadrado, cada uno con colores
# diferentes en sus vértices.
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_triangle():
    # Triángulo a la derecha
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)   # Rojo
    glVertex2f(0.2, -0.3)      # Inferior izquierdo
    glColor3f(0.0, 1.0, 0.0)   # Verde
    glVertex2f(0.8, -0.3)      # Inferior derecho
    glColor3f(0.0, 0.0, 1.0)   # Azul
    glVertex2f(0.5, 0.3)       # Superior
    glEnd()

def draw_trianguloinv():
    # Triángulo invertido arriba al centro
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 1.0, 0.0)   # Amarillo
    glVertex2f(-0.2, 0.8)      # Superior izquierdo
    glColor3f(0.0, 1.0, 1.0)   # Cian
    glVertex2f(0.2, 0.8)       # Superior derecho
    glColor3f(1.0, 0.0, 1.0)   # Magenta
    glVertex2f(0.0, 0.4)       # Punta inferior
    glEnd()

def draw_cuadrado():
    # Cuadrado a la izquierda
    glBegin(GL_QUADS)
    glColor3f(1.0, 0.0, 0.0)   # Rojo
    glVertex2f(-0.8, -0.4)     # Inferior izquierdo
    glColor3f(0.0, 1.0, 0.0)   # Verde
    glVertex2f(-0.2, -0.4)     # Inferior derecho
    glColor3f(0.0, 0.0, 1.0)   # Azul
    glVertex2f(-0.2, 0.4)      # Superior derecho
    glColor3f(1.0, 0.0, 1.0)   # Magenta
    glVertex2f(-0.8, 0.4)      # Superior izquierdo
    glEnd()



def main():
    # Inicializa GLFW
    if not glfw.init():
        return

    # Crear la ventana
    window = glfw.create_window(800, 600, "OpenGL Figuras", None, None)
    if not window:
        glfw.terminate()
        return

    # Hacer el contexto de OpenGL actual para la ventana
    glfw.make_context_current(window)

    # Configurar la proyección (2D simple)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)  # Proyección ortográfica 2D
    glMatrixMode(GL_MODELVIEW)

    # Bucle principal
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)  # Limpiar la pantalla con color de fondo

        draw_triangle()  # Dibujar el triángulo
        draw_cuadrado() #dibujar cuadrado
        draw_trianguloinv()  # Dibujar el triángulo invertido

        glfw.swap_buffers(window)  # Intercambiar los buffers
        glfw.poll_events()  # Comprobar eventos

    # Finalizar GLFW
    glfw.terminate()

if __name__ == "__main__":
    main()



