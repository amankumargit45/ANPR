from flask import Flask, request, render_template, redirect, url_for
from ultralytics import YOLO
import cv2
import easyocr
import os
import pandas as pd

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load YOLOv8 model
model = YOLO('runs/detect/license-plate6/weights/best.pt')
reader = easyocr.Reader(['en'])

# Ensure output directory exists
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Process the uploaded video
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return "Error: Cannot open video."

    license_plate_numbers = set()
    c = 1
    x1 = x2 = y1 = y2 = 0
    label = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process once every 32 frames
        if c % 32 == 0:
            results = model(frame)
            for r in results:
                for box in r.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    label = int(box.cls[0])
                    # License plate detected
                    if label == 0:  
                        license_plate = frame[y1:y2, x1:x2]
                        ress = reader.readtext(license_plate)
                        for (_, text, prob) in ress:
                            if prob > 0.5:
                                license_plate_numbers.add(text)
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        c += 1

    cap.release()

    # Save the results to CSV
    df = pd.DataFrame({'license_plate_numbers': list(license_plate_numbers)})
    csv_path = os.path.join(OUTPUT_FOLDER, 'License_plate.csv')
    df.to_csv(csv_path, index=False)

    return license_plate_numbers


# Home route to upload video
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle video upload and processing
@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        license_plates = process_video(file_path)
        record_list = list(license_plates)
        stolen_record = pd.read_csv('stolen_vehicles.csv')
        stolen_record_list = list(stolen_record['lplate'])
        detected_vehicle = set()
        for item in stolen_record_list:
            if item in record_list:
                detected_vehicle.add(item)
        return render_template('result.html', plates=detected_vehicle)

# Route for Video Page
@app.route('/video')
def video():
    return render_template('video.html')

#  Route for Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
