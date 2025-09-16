import cv2
import numpy as np

# Configuración del rango de color en HSV azu
lower_color = np.array([100, 150, 50])
upper_color = np.array([140, 255, 255])

# Captura de video desde la cámara
cap = cv2.VideoCapture(0)

# Crear una "lona" para dibujar el rastro
trail = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Inicializar la lona con las mismas dimensiones del frame
    if trail is None:
        trail = np.zeros_like(frame)

    # Convertir la imagen a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Crear máscara para el color deseado
    mask = cv2.inRange(hsv, lower_color, upper_color)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Encontrar contornos del objeto
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Tomar el contorno más grande
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if radius > 5:
            # Dibujar un círculo en la lona
            cv2.circle(trail, (int(x), int(y)), int(radius), (255, 0, 0), -1)

    # Combinar el frame con el rastro
    output = cv2.addWeighted(frame, 0.7, trail, 0.3, 0)

    cv2.imshow("Rastro de color", output)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Esc para salir
        break

cap.release()
cv2.destroyAllWindows()
