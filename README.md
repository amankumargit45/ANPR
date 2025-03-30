# ANPR
This project implements an Automatic Number Plate Recognition (ANPR) system using Flask. The system processes uploaded video footage, extracts license plate numbers using YOLOv8 for Object Detection and EasyOCR for Optical Character Recognition (OCR), and checks against a stolen vehicle database stored in stolen_vehicles.csv. If a match is found, an alert is generated.

Features
Upload video files for processing.
Extract license plates using YOLOv8 & EasyOCR.
Cross-check detected plates with a stolen vehicle database.
Generate alerts if a match is found.
User-friendly Flask web interface.

Tech Stack
Backend: Flask, OpenCV, YOLOv8, EasyOCR, Ultralytics
Frontend: HTML, CSS, JavaScript
Database: CSV file (stolen_vehicles.csv), can be extended to SQL/NoSQL databases
Deployment: AWS/GCP or local server

Installation & Usage:
1️⃣ Clone the Repository
git clone https://github.com/yourusername/ANPR_Project.git
cd ANPR_Project

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Download YOLOv8 Model
from ultralytics import YOLO
model = YOLO("yolov8n.pt")
model.fuse()

4️⃣Run the Flask App
python app.py

5️⃣ Upload and Process a Video
Open the web app.
Upload a video file.
Wait for processing to complete.
View extracted license plates and alerts (if any match found).
