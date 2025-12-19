# Este código crea una ventana OpenGL que muestra una cuadrícula 4x4 de diferentes figuras geométricas.
# Cada figura tiene un color distintivo aplicado a través de una lista de colores predefinidos.
# Se utilizan las funciones de GLUT para dibujar las figuras y manejar la ventana.

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

# Dimensiones iniciales de la ventana
width, height = 900, 900
# Lista de 16 colores distintivos (para la cuadrícula 4x4)
COLORES_VARIADOS = [
    [0.9, 0.2, 0.2], # 0. Rojo
    [0.2, 0.9, 0.2], # 1. Verde
    [0.2, 0.2, 0.9], # 2. Azul
    [0.9, 0.9, 0.2], # 3. Amarillo
    [0.9, 0.2, 0.9], # 4. Magenta
    [0.2, 0.9, 0.9], # 5. Cian
    [0.9, 0.5, 0.1], # 6. Naranja
    [0.1, 0.5, 0.9], # 7. Azul Claro
    [0.6, 0.6, 0.6], # 8. Gris
    [0.4, 0.8, 0.4], # 9. Verde Menta
    [0.8, 0.4, 0.8], # 10. Lila
    [0.4, 0.4, 0.4], # 11. Gris Oscuro
    [0.7, 0.7, 0.2], # 12. Oliva
    [0.2, 0.7, 0.7], # 13. Turquesa
    [1.0, 0.6, 0.4], # 14. Piel 
    [0.4, 0.6, 1.0]  # 15. Azul Marino 
]

def init():
    """Configuración inicial de OpenGL."""
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    # Posición de la luz
    glLightfv(GL_LIGHT0, GL_POSITION, [2, 3, 4, 0]) 
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    # Fondo
    glClearColor(0.05, 0.05, 0.05, 1)

def dibujar(indice):
    # Dibuja una figura basada en el índice proporcionado
    if indice == 0: glutWireSphere(0.6, 20, 20)
    elif indice == 1: glutSolidSphere(0.6, 20, 20)
    elif indice == 2: glutWireCube(1.0)
    elif indice == 3: glutSolidCube(1.0)
    elif indice == 4: glutWireCone(0.6, 1.0, 20, 4)
    elif indice == 5: glutSolidCone(0.6, 1.0, 20, 4)
    elif indice == 6: glutWireDodecahedron()
    elif indice == 7: glutSolidDodecahedron()
    elif indice == 8: glutWireOctahedron()
    elif indice == 9: glutSolidOctahedron()
    elif indice == 10: glutWireTetrahedron()
    elif indice == 11: glutSolidTetrahedron()
    elif indice == 12: glutWireIcosahedron()
    elif indice == 13: glutSolidIcosahedron()
    elif indice == 14: glutWireTorus(0.2, 0.5, 20, 20) 
    elif indice == 15: glutSolidTorus(0.2, 0.5, 20, 20) 
    

def ver():
    """Bucle principal de dibujo, configura la ventana y aplica color."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    rows, cols = 4, 4
    cell_w = width // cols
    cell_h = height // rows
    
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            glViewport(c * cell_w, (rows - 1 - r) * cell_h, cell_w, cell_h)
            
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(45, cell_w / cell_h, 1, 20)
            
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            gluLookAt(0, 0, 3, 0, 0, 0, 0, 1, 0)
            
            # Rotación
            glRotatef(30, 0.5, 1.0, 0) 

            # índice 'i' para selecciona un color de la lista 
            glColor3fv(COLORES_VARIADOS[i])
            
            dibujar(i)
    
    glutSwapBuffers()

# Reajusta el tamaño de la ventana
def reshape(w, h):
    global width, height
    width, height = w, h
    
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Figuras con Glut")

    init()
    glutDisplayFunc(ver)
    glutReshapeFunc(reshape)
    glutMainLoop()

if __name__ == "__main__":
    main()