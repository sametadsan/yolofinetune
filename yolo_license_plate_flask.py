import os
import time
import cv2
from ultralytics import YOLO
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from io import BytesIO
import numpy as np


app = Flask(__name__)

current_dir = Path(__file__).resolve().parent
output_dir = current_dir / 'output'
output_dir.mkdir(exist_ok=True)

LICENSE_PLATE_CLASS_ID = 0  

def load_yolo_v8_model():
    start_time = time.time()  
    model_path = current_dir / 'yolo' / 'last.pt'
    if not model_path.exists():
        print(f"Model file does not exist at {model_path}")
        return None
    model = YOLO(str(model_path))  # Convert Path object to string
    print("YOLOv8 model loaded successfully")
    end_time = time.time()  
    print(f"Model loading time: {end_time - start_time:.4f} seconds")  
    return model

def detect_license_plates_yolo_v8(image, model, confidence_threshold=0.2):
    start_time = time.time()  #  timing
    results = model(image)
    detections = []
    for box in results[0].boxes:
        cls = int(box.cls.item())  
        confidence = box.conf.item()  
        if cls == LICENSE_PLATE_CLASS_ID and confidence > confidence_threshold:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())  # Convert the bounding box 
            detections.append(((x1, y1, x2 - x1, y2 - y1), confidence))
    end_time = time.time()  # End timing
    print(f"License plate detection time: {end_time - start_time:.4f} seconds") 
    return detections

def add_watermark(image, text="sompo sigorta", opacity=0.5):
    start_time = time.time()  # Start timing
    overlay = image.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    font_color = (255, 255, 255)  
    font_thickness = 3
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
    image_height, image_width = image.shape[:2]
    text_x = (image_width - text_size[0]) // 2
    text_y = (image_height + text_size[1]) // 2
    cv2.putText(overlay, text, (text_x, text_y), font, font_scale, font_color, font_thickness, cv2.LINE_AA)
    cv2.addWeighted(overlay, opacity, image, 1 - opacity, 0, image)
    end_time = time.time()  # End timing
    print(f"Watermark addition time: {end_time - start_time:.4f} seconds")  
    return image

def cover_license_plate_with_black(image, model, debug=False):
    start_time = time.time()  # timing
    detections = detect_license_plates_yolo_v8(image, model)

    if not detections:
        print(f"No license plates detected.")
        image = add_watermark(image)
        return image

    if debug:
        for (box, confidence) in detections:
            x, y, w, h = box
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    for (box, confidence) in detections:
        x, y, w, h = box
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), -1)

    image = add_watermark(image)
    end_time = time.time()  # End timing
    print(f"Total processing time for this image: {end_time - start_time:.4f} seconds")
    return image

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist("files")  

    if files and files[0].filename:
        in_memory_file = BytesIO()
        files[0].save(in_memory_file)
        in_memory_file.seek(0)
        image = cv2.imdecode(np.frombuffer(in_memory_file.read(), np.uint8), cv2.IMREAD_COLOR)

        processed_image = cover_license_plate_with_black(image, model, debug=True)

        _, buffer = cv2.imencode('.png', processed_image)
        output_file = BytesIO(buffer)
        output_file.seek(0)

        return send_file(output_file, mimetype='image/png', as_attachment=True, download_name='processed_image.png')
    else:
        return "No file uploaded", 400

if __name__ == "__main__":
    model = load_yolo_v8_model()
    if model:
        app.run(debug=True)
