import cv2
from ultralytics import YOLO
import serial
import sqlite3
from datetime import datetime
import os
import time

# ===== НАСТРОЙКИ =====
DB_PATH = "detections.db"
IMAGE_DIR = "captures"
MODEL_PATH = "yolov8n.pt"  # можно заменить на свою обученную модель
CONF_THRESHOLD = 0.6
SERIAL_PORT = "/dev/ttyACM0"
BAUDRATE = 9600
# ======================

os.makedirs(IMAGE_DIR, exist_ok=True)

# Подключение к Arduino
arduino = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
time.sleep(2)

# Загрузка модели
model = YOLO(MODEL_PATH)

def save_to_db(conf, x1, y1, x2, y2, img_path):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO detections 
        (timestamp, confidence, x1, y1, x2, y2, image_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        conf, x1, y1, x2, y2, img_path
    ))

    conn.commit()
    conn.close()

def main():
    cap = cv2.VideoCapture(0)

    print("Bird detection started...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        detected = False

        for r in results:
            boxes = r.boxes

            if boxes is not None and len(boxes) > 0:
                for box in boxes:
                    conf = float(box.conf[0])
                    cls = int(box.cls[0])

                    # если используешь обычную yolov8n.pt,
                    # класс 14 = bird
                    if cls == 14 and conf > CONF_THRESHOLD:
                        detected = True

                        x1, y1, x2, y2 = box.xyxy[0].tolist()

                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        img_path = f"{IMAGE_DIR}/bird_{timestamp}.jpg"

                        cv2.imwrite(img_path, frame)

                        save_to_db(conf, x1, y1, x2, y2, img_path)

        if detected:
            arduino.write(b'H')
        else:
            arduino.write(b'L')

        cv2.imshow("Bird Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    arduino.close()

if __name__ == "__main__":
    main()
