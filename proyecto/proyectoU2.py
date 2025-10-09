import cv2 as cv
import numpy as np
import math

face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_alt.xml')
smile_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_smile.xml')

cap = cv.VideoCapture(0)

# pupilas mov. y orejas
pupil_offset_x = 0
pupil_offset_y = 0
pupil_dx = 0.6 #horizontal
pupil_dy = 0.6 #vertical
oreja_offset = 0
oreja_dy = 1
frame_count = 0

# base de ojos y suavizado
ojo_radio_base = 25
ojo_radio_suavizado = ojo_radio_base
suavizado_factor = 0.15

while True:
    ret, img = cap.read()
    if not ret:
        break

    img = cv.flip(img, 1) # espejo horizontal
    gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gris, 1.3, 5) # detectar caras

    frame_count += 1
    head_angle = int(10 * math.sin(frame_count * 0.05)) # mov. cabeza
    dientes_visibles = (frame_count // 20) % 2 == 0

    for (x, y, w, h) in faces:
        color_piel = (180, 200, 255)
        centro_cara = (x + w // 2 + head_angle, y + h // 2)

        # cercania ojos / pupilas
        factor_cercania = np.interp(w, [80, 200, 350], [0.3, 1.0, 3.5])
        factor_cercania = max(0.3, min(factor_cercania, 3.5))

        ojo_radio_objetivo = ojo_radio_base * factor_cercania
        ojo_radio_suavizado = ojo_radio_suavizado * (1 - suavizado_factor) + ojo_radio_objetivo * suavizado_factor
        ojo_radio = int(ojo_radio_suavizado)


        # circulo para cara
        cv.circle(img, centro_cara, w // 2, color_piel, -1)

        # orejas
        oreja_offset += oreja_dy
        if abs(oreja_offset) > 5:
            oreja_dy *= -1
        cv.ellipse(img, (x + int(w * 0.05) + head_angle, y + int(h * 0.45) + oreja_offset),
                   (int(w * 0.10), int(h * 0.25)), 0, 0, 360, color_piel, -1)
        cv.ellipse(img, (x + int(w * 0.95) + head_angle, y + int(h * 0.45) - oreja_offset),
                   (int(w * 0.10), int(h * 0.25)), 0, 0, 360, color_piel, -1)

        # ojos
        radio_pupila = max(4, int(ojo_radio * 0.3))
        cx_izq = x + int(w * 0.3) + head_angle
        cx_der = x + int(w * 0.7) + head_angle
        cy_ojo = y + int(h * 0.4)

        for cx in [cx_izq, cx_der]:
            cv.circle(img, (cx, cy_ojo), ojo_radio, (255, 255, 255), -1)
            cv.circle(img, (cx, cy_ojo), ojo_radio + 2, (0, 0, 0), 2)

        # movimiento pupilas proporcional al tamaño del ojo
        limite_pupila = max(4, ojo_radio // 2 - radio_pupila - 2)
        pupil_offset_x += pupil_dx
        pupil_offset_y += pupil_dy
        if abs(pupil_offset_x) >= limite_pupila:
            pupil_dx *= -1
            pupil_offset_x = np.sign(pupil_dx) * limite_pupila
        if abs(pupil_offset_y) >= limite_pupila:
            pupil_dy *= -1
            pupil_offset_y = np.sign(pupil_dy) * limite_pupila

        for cx in [cx_izq, cx_der]:
            cv.circle(img, (int(cx + pupil_offset_x), int(cy_ojo + pupil_offset_y)),
                      radio_pupila, (0, 0, 0), -1)

        # nariz
        pts = np.array([
            (x + int(w * 0.5) + head_angle, y + int(h * 0.45)),
            (x + int(w * 0.45) + head_angle, y + int(h * 0.65)),
            (x + int(w * 0.55) + head_angle, y + int(h * 0.65))
        ], np.int32)
        cv.fillPoly(img, [pts], (0, 0, 0))

        # boca con dientes
        centro_boca = (x + int(w / 2) + head_angle, y + int(h * 0.75))
        ancho_boca = int(w * 0.3)
        alto_boca = int(h * 0.12)
        cv.ellipse(img, centro_boca, (ancho_boca, alto_boca), 0, 0, 180, (0, 0, 0), -1)
        cv.ellipse(img, centro_boca, (ancho_boca, alto_boca), 0, 0, 180, (0, 0, 0), 4)

        if (frame_count // 20) % 2 == 0:
            num_dientes = 6
            fila_y = centro_boca[1] - int(alto_boca * 0.1)
            for i in range(num_dientes):
                d_x = centro_boca[0] - int(ancho_boca * 0.8) // 2 + i * int(ancho_boca * 0.8 / (num_dientes - 1))
                cv.rectangle(img, (d_x - 5, fila_y), (d_x + 5, fila_y + 10), (255, 255, 255), -1)

        # lengua si sonríes
        roi_gray = gris[y + int(h * 0.6): y + h, x:x + w]
        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.7, minNeighbors=20)
        if len(smiles) > 0:
            lengua_altura = int(alto_boca * 2)
            cv.ellipse(img,
                       (centro_boca[0], centro_boca[1] + int(alto_boca / 1.5)),
                       (int(ancho_boca / 4), lengua_altura),
                       0, 0, 180, (180, 105, 255), -1)

    cv.imshow('Filtro', img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()











