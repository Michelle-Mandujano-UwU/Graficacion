import cv2
import numpy as np

# Tamaño del frame (ventana de juego)
width, height = 600, 400

# Cargar imagen de fondo y redimensionarla al tamaño del frame
background = cv2.imread("pastel.jpg")  
background = cv2.resize(background, (width, height))

# CONFIGURACIÓN DE LAS PELOTAS
# Pelota azul que rebota
ball_pos = np.array([300, 200], dtype=np.int32)  # posición inicial (x, y)
ball_vel = np.array([4, 3], dtype=np.int32)      # velocidad inicial (dx, dy)
ball_radius = 20                                 # radio de la pelota

# Pelota rosa que esquiva
dodger_pos = np.array([100, 100], dtype=np.int32)  # posición inicial (x, y)
dodger_radius = 20                                 # radio de la pelota que esquiva
dodger_speed = 5                                   # velocidad de movimiento al esquivar

while True:
    # Crear un frame a partir de la imagen de fondo
    # Esto asegura que cada fotograma comience limpio
    frame = background.copy()

    # ACTUALIZAR PELOTA AZUL QUE REBOTA
    ball_pos += ball_vel  # mover la pelota sumando la velocidad a la posición actual

    # Rebote horizontal: invertir la velocidad si toca los bordes izquierdo/derecho
    if ball_pos[0] - ball_radius <= 0 or ball_pos[0] + ball_radius >= width:
        ball_vel[0] *= -1

    # Rebote vertical: invertir la velocidad si toca los bordes superior/inferior
    if ball_pos[1] - ball_radius <= 0 or ball_pos[1] + ball_radius >= height:
        ball_vel[1] *= -1

    # Dibujar la pelota azul en el frame (BGR: azul)
    cv2.circle(frame, tuple(ball_pos), ball_radius, (255, 0, 0), -1)

    # ACTUALIZAR PELOTA ROSA QUE ESQUIVA
    # Calcular vector de distancia entre la pelota azul y la rosa
    dx = ball_pos[0] - dodger_pos[0]
    dy = ball_pos[1] - dodger_pos[1]
    dist = np.sqrt(dx**2 + dy**2)  # distancia euclidiana

    # Si la pelota azul está demasiado cerca, mover la rosa en dirección contraria
    if dist < 120:
        # Movimiento horizontal: alejarse de la azul
        dodger_pos[0] -= dodger_speed if dx > 0 else -dodger_speed
        # Movimiento vertical: alejarse de la azul
        dodger_pos[1] -= dodger_speed if dy > 0 else -dodger_speed

    # Mantener la pelota rosa dentro de los límites del frame
    dodger_pos[0] = np.clip(dodger_pos[0], dodger_radius, width - dodger_radius)
    dodger_pos[1] = np.clip(dodger_pos[1], dodger_radius, height - dodger_radius)

    # Dibujar la pelota rosa en el frame (BGR: rosa)
    cv2.circle(frame, tuple(dodger_pos), dodger_radius, (147, 20, 255), -1)

    # MOSTRAR EL FRAME
    cv2.imshow("Pelotas con fondo", frame)

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Cerrar todas las ventanas abiertas de OpenCV
cv2.destroyAllWindows()
