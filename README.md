# Bird Detection System (YOLO + Arduino)

## 📌 Description

This project detects birds using a USB camera and YOLOv8.
When a bird is detected:

- The system saves the image
- Logs data into SQLite database
- Sends signal to Arduino
- Arduino activates sound deterrent

## 🧠 Technologies Used

- Raspberry Pi
- USB Web Camera
- YOLOv8 (Ultralytics)
- Arduino
- SQLite
- OpenCV

## ⚙️ Setup

1. Create virtual environment:
   python3 -m venv birdenv
   source birdenv/bin/activate

2. Install dependencies:
   pip install -r requirements.txt

3. Initialize database:
   python init_db.py

4. Run detection:
   python detect_and_log.py

## 🔊 Arduino

Upload arduino_buzzer.ino to Arduino.

Buzzer connects to pin 8.

## 📊 Database

All detections are stored in:
detections.db

Images are saved in:
captures/
