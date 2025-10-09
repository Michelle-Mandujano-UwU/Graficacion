import cv2 as cv
import numpy as np

# Cargar el clasificador de rostros
rostro = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_alt.xml')

# Iniciar la cámara
cap = cv.VideoCapture(0)

while True:
    ret, img = cap.read()
    if not ret:
        break

    gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gris, 1.3, 5)

    for (x, y, w, h) in rostros:
        # Cuadro del rostro
        cv.rectangle(img, (x, y), (x + w, y + h), (234, 23, 23), 2)

        # Orejas
        color_piel = (210, 190, 170)
        # Izquierda
        cv.ellipse(img, (x + int(w * 0.03), y + int(h * 0.42)), (int(w * 0.07), int(h * 0.20)), 0, 0, 360, color_piel, -1)
        # Derecha
        cv.ellipse(img, (x + int(w * 0.97), y + int(h * 0.42)), (int(w * 0.07), int(h * 0.20)), 0, 0, 360, color_piel, -1)

        # Ojos
        cv.circle(img, (x + int(w * 0.3), y + int(h * 0.4)), 22, (0, 0, 0), 2)
        cv.circle(img, (x + int(w * 0.7), y + int(h * 0.4)), 22, (0, 0, 0), 2)

        cv.circle(img, (x + int(w * 0.3), y + int(h * 0.4)), 20, (255, 255, 255), -1)
        cv.circle(img, (x + int(w * 0.7), y + int(h * 0.4)), 20, (255, 255, 255), -1)

        cv.circle(img, (x + int(w * 0.3), y + int(h * 0.4)), 6, (0, 0, 0), -1)
        cv.circle(img, (x + int(w * 0.7), y + int(h * 0.4)), 6, (0, 0, 0), -1)

        # Nariz
        pts = np.array([
            (x + int(w * 0.5), y + int(h * 0.45)),
            (x + int(w * 0.45), y + int(h * 0.65)),
            (x + int(w * 0.55), y + int(h * 0.65))
        ], np.int32)
        cv.fillPoly(img, [pts], (0, 0, 0))

        # Boca
        centro_boca = (x + int(w / 2), y + int(h * 0.75))
        cv.ellipse(img, centro_boca, (int(w * 0.25), int(h * 0.08)), 0, 0, 180, (0, 0, 150), -1)
        cv.ellipse(img, centro_boca, (int(w * 0.25), int(h * 0.08)), 0, 0, 180, (0, 0, 0), 2)

    # Mostrar el resultado
    cv.imshow('Detector de rostro con dibujo', img)


    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
