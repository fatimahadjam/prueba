import cv2
import numpy as np

# Ruta exacta del video
video_path = r'C:\Users\Lucas\Desktop\Casper\VID_20241027_144034.mp4'
cap = cv2.VideoCapture(video_path)

# Parámetros de detección
light_threshold = 180  # Umbral para detectar luz intensa

# Variables para almacenar el patrón detectado
pattern = []
current_duration = 0
detecting_light = False

# Dimensiones de la región de interés (ROI) donde está la lámpara
roi_x, roi_y, roi_width, roi_height = 550, 200, 250, 300

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Extrae solo el área de interés (ROI) de la lámpara
    roi = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]
    
    # Convierte la ROI a escala de grises y calcula el brillo promedio
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray)

    # Detecta si hay un destello en la ROI
    if avg_brightness > light_threshold:
        if not detecting_light:
            # Cambió de apagado a encendido
            if current_duration > 0:
                pattern.append(("apagado", current_duration))
            detecting_light = True
            current_duration = 1
        else:
            # Sigue encendido
            current_duration += 1
    else:
        if detecting_light:
            # Cambió de encendido a apagado
            if current_duration > 0:
                pattern.append(("encendido", current_duration))
            detecting_light = False
            current_duration = 1
        else:
            # Sigue apagado
            current_duration += 1

# Guarda el último estado
if current_duration > 0:
    if detecting_light:
        pattern.append(("encendido", current_duration))
    else:
        pattern.append(("apagado", current_duration))

cap.release()

# Imprime el patrón detectado
for estado, duracion in pattern:
    print(f"{estado}: {duracion} frames")