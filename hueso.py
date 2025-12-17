# Programa para dibujar un hueso 3D con OpenGL en Python usando esferas y cilindros.
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Esta variable controla qué tan rápido da vueltas todo el conjunto
giro_total = 0.0

def crear_esfera(radio_esfera, segmentos_h=30, segmentos_v=30):
    """
    Crea una bola desde cero. 
    Usa bucles para calcular cada punto de la superficie y unirlos con cuadrados.
    """
    for i in range(segmentos_v): 
        latitud1 = math.pi * (-0.5 + i / segmentos_v) # Latitud del primer punto
        latitud2 = math.pi * (-0.5 + (i + 1) / segmentos_v) # Latitud del segundo punto
        
        glBegin(GL_QUAD_STRIP) # Empezamos a dibujar tiras de cuadrados
        for j in range(segmentos_h + 1):
            longitud = 2 * math.pi * j / segmentos_h
            
            # Punto superior del cuadrado
            x1 = math.cos(latitud1) * math.cos(longitud)
            y1 = math.sin(latitud1)
            z1 = math.cos(latitud1) * math.sin(longitud)
            
            # Punto inferior del cuadrado
            x2 = math.cos(latitud2) * math.cos(longitud)
            y2 = math.sin(latitud2)
            z2 = math.cos(latitud2) * math.sin(longitud)
            
            # Le decimos a OpenGL hacia dónde mira la cara (para la luz)
            glNormal3f(x1, y1, z1)
            glVertex3f(x1 * radio_esfera, y1 * radio_esfera, z1 * radio_esfera)
            
            glNormal3f(x2, y2, z2)
            glVertex3f(x2 * radio_esfera, y2 * radio_esfera, z2 * radio_esfera)
        glEnd()

def crear_tubo(radio_tubo):
    """
    Dibuja un cilindro
    """
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(0, 361):
        angulo_rad = math.radians(i)
        x = math.cos(angulo_rad)
        y = math.sin(angulo_rad)
        profundidad = 0.5
        
        glNormal3f(x, y, 0)
        glVertex3f(x * radio_tubo, y * radio_tubo, profundidad) # Frente del tubo
        glNormal3f(x, y, 0)
        glVertex3f((x * radio_tubo), (y * radio_tubo), (profundidad * 4))
    glEnd()

def construir_escena_ojos():
    """
    Aquí es donde posicionamos cada esfera y el cilindro en el espacio.
    """
    glPushMatrix() # Guardamos la posición base
   
    # Dibujamos el cilindro blanco (ahora está en una posición específica)
    glColor3f(1.0, 1.0, 1.0) 
    glPushMatrix()
    glRotate(90, 0, 1, 0) # Lo acostamos
    glTranslate(0, 0.22, 0.45) # Lo movemos un poco
    crear_tubo(0.4)
    glPopMatrix()

    # Esfera 1: Abajo a la izquierda
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(0.56, 0, 0)
    crear_esfera(0.6, 30, 30)
    glPopMatrix()
    
    # Esfera 2: Arriba a la izquierda
    glPushMatrix()
    glTranslatef(0.56, 0.54, 0)
    crear_esfera(0.6, 30, 30)
    glPopMatrix()
    
    # Esfera 3: Abajo a la derecha
    glPushMatrix()
    glTranslatef(2.56, 0, 0)
    crear_esfera(0.6, 30, 30)
    glPopMatrix()
    
    # Esfera 4: Arriba a la derecha
    glPushMatrix()
    glTranslatef(2.56, 0.54, 0)
    crear_esfera(0.6, 30, 30)
    glPopMatrix()

    glPopMatrix() # Regresamos a la posición original

def luces_y_sombras():
    """ Configuración para que no se vea plano y tenga volumen """
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST) # Para que lo que esté adelante tape lo de atrás
    glEnable(GL_COLOR_MATERIAL)
    
    posicion_foco = [1.0, 1.0, 1.0, 0.2]
    glLightfv(GL_LIGHT0, GL_POSITION, posicion_foco)

def iniciar_programa():
    global giro_total
    
    if not glfw.init():
        return

    # Creamos la ventana de visualización
    ventana = glfw.create_window(800, 600, "Hueso 3D", None, None)
    if not ventana:
        glfw.terminate()
        return

    glfw.make_context_current(ventana)

    # Fondo negro
    glClearColor(0.0, 0.0, 0.0, 1.0) 
    luces_y_sombras()

    while not glfw.window_should_close(ventana):
        # Limpiamos pantalla y el buffer de profundidad
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800/600, 0.1, 100.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(-1.5, -0.3, -5) # Centramos un poco la cámara para ver todas las esferas
        
        # Animación de rotación
        giro_total += 0.5
        glRotatef(giro_total, 0, 1, 0) 
        
        # Llamamos a nuestra función de dibujo
        construir_escena_ojos()
        
        glfw.swap_buffers(ventana)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    iniciar_programa()