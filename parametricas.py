# Actividad en Apuntes de graficacion: Programar al menos 10 ecuaciones parametricas

import math
import cv2 as cv
import numpy as np

# Config de pantalla
ancho, alto = 800, 800
centrox, centroy = ancho // 2, alto // 2
t = 0.0 

colores = {
    "Estrella de nunca mas": (150, 250, 150),
    "Esponja de maquillaje": (255, 180, 100),
    "Reloj de arena celestial": (120, 120, 255),
    "Giro giro": (220, 220, 220),
    "Cerro": (50, 255, 255),
    "Corazon": (100, 100, 255),
    "Trebol": (255, 255, 255),
    "Marco derecho": (255, 100, 255),
    "Arco de agua": (250, 150, 50),
    "Flor": (100, 255, 100)
}

# Crear los lienzos
lienzo = {nombre: np.zeros((alto, ancho, 3), dtype=np.uint8) for nombre in colores}

# para evitar division entre 0
def evitarErrores(x, y):
    try:
        # Si el numero es infinito o no existe, lo mandamos al centro para que no estorbe
        if not math.isfinite(x) or not math.isfinite(y):
            return (centrox, centroy)
        # redondeo
        return (int(x), int(y))
    except:
        return (centrox, centroy)

while True:
    # Estrella de nunca mas
    ex, ey = centrox + 200 * math.cos(t)**3, centroy + 200 * math.sin(t)**3
    
    # Esponja de maquillaje
    esx = centrox + 100 * (3 * math.cos(t) - math.cos(3 * t))
    esy = centroy + 100 * (3 * math.sin(t) - math.sin(3 * t))
    
    # Reloj de arena celestial
    rx = centrox + 250 * math.sin(3 * t + 1.5)
    ry = centroy + 200 * math.sin(2 * t)
    
    # Giro giro
    radio = 3 * t * 5
    arcx, arcy = centrox + radio * math.cos(t), centroy + radio * math.sin(t)
    
    # Cerro
    div = 1 + math.sin(t)**3 + math.cos(t)**3
    cx = centrox + (300 * math.sin(t)) / div if abs(div) > 0.01 else centrox
    cy = centroy + (300 * math.sin(t)**2) / div if abs(div) > 0.01 else centroy

    # Corazon
    corx = centrox + 15 * (16 * math.sin(t)**3)
    cory = centroy - 15 * (13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))

    # Trebol
    rt = 200 * math.cos(3 * t)
    trx, try_ = centrox + rt * math.cos(t), centroy + rt * math.sin(t)

    # Marco derecho
    mx = centrox + 120 * (math.cos(t) + 5 * math.cos(t/4))
    my = centroy + 120 * (math.sin(t) - 5 * math.sin(t/4))

    # Arco de agua
    cos_t = math.cos(t)
    arcx = centrox + 150 * (math.sin(t)**2)
    arcy = centroy + 150 * (math.sin(t)**3 / cos_t) if abs(cos_t) > 0.01 else centroy

    # Flor
    rfl = 200 * math.sin(4 * t)
    flx, fly = centrox + rfl * math.cos(t), centroy + rfl * math.sin(t)

    # Convertir a enteros
    puntos = [
        evitarErrores(ex, ey), evitarErrores(esx, esy), evitarErrores(rx, ry),
        evitarErrores(arcx, arcy), evitarErrores(cx, cy), evitarErrores(corx, cory),
        evitarErrores(trx, try_), evitarErrores(mx, my), evitarErrores(arcx, arcy),
        evitarErrores(flx, fly)
    ]

    # Dibujar
    for (nombre, color), punto in zip(colores.items(), puntos):
        cv.circle(lienzo[nombre], punto, 2, color, -1)
        cv.imshow(nombre, lienzo[nombre])

    t += 0.07
    if cv.waitKey(1) & 0xFF == 27:
        break

cv.destroyAllWindows()