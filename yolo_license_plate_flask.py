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

def load_yolo_v8_model(model_name='last.pt'):
    start_time = time.time()  
    model_path = current_dir / 'yolo' / model_name
    if not model_path.exists():
        print(f"Model file does not exist at {model_path}")
        return None
    model = YOLO(str(model_path)) 
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

def add_watermark(image, text="Sompo Sigorta A.S.", opacity=0.5):
    start_time = time.time()  # Start timing
    overlay = image.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.5
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

    start_time = time.time()  
    original_image = image.copy()  
    angles = [0, 90, 180, 270]  
    processed = False

    for angle in angles:
        rotated_image = rotate_image(image, angle)
        detections = detect_license_plates_yolo_v8(rotated_image, model)

        if detections:
            if debug:
                for (box, confidence) in detections:
                    x, y, w, h = box
                    cv2.rectangle(rotated_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            for (box, confidence) in detections:
                x, y, w, h = box
                cv2.rectangle(rotated_image, (x, y), (x + w, y + h), (0, 0, 0), -1)

            image = rotate_image(rotated_image, -angle)
            processed = True
            break

    if not processed:
        image = add_watermark(image)
    else:
        image = add_watermark(image)

    end_time = time.time()  # End timing
    print(f"Total processing time for this image: {end_time - start_time:.4f} seconds")
    return image

def cover_license_plate_with_black(image, model, debug=False):
    start_time = time.time()  
    angles = [0, 90, 180, 270]  
    original_image = image.copy()  
    image_height, image_width = image.shape[:2]

    
    mask = np.zeros((image_height, image_width), dtype=np.uint8)

    for angle in angles:
        
        rotated_image = rotate_image(original_image, angle)
        detections = detect_license_plates_yolo_v8(rotated_image, model)

        if detections:
            for (box, confidence) in detections:
                x, y, w, h = box

                
                if angle == 90:
                    x, y = y, image_height - x - w
                    w, h = h, w
                elif angle == 180:
                    x, y = image_width - x - w, image_height - y - h
                elif angle == 270:
                    x, y = image_width - y - h, x
                    w, h = h, w

                
                cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

    
    original_image[mask == 255] = [0, 0, 0]

    
    original_image = add_watermark(original_image)
    
    end_time = time.time()  
    print(f"Total processing time for this image: {end_time - start_time:.4f} seconds")
    return original_image

def rotate_image(image, angle):
    if angle == 0:
        return image.copy()
    elif angle == 90:
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        return cv2.rotate(image, cv2.ROTATE_180)
    elif angle == 270:
        return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)



@app.route('/license-plate/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist("files")
    model_name = request.args.get('model_name', 'last.pt') # default last model
   
    if files and files[0].filename:
        in_memory_file = BytesIO()
        files[0].save(in_memory_file)
        in_memory_file.seek(0)
        image = cv2.imdecode(np.frombuffer(in_memory_file.read(), np.uint8), cv2.IMREAD_COLOR)

        model = load_yolo_v8_model(model_name)
        if not model:
            return f"Model {model_name} not found.", 404

        processed_image = cover_license_plate_with_black(image, model, debug=True)

        _, buffer = cv2.imencode('.png', processed_image)
        output_file = BytesIO(buffer)
        output_file.seek(0)

        return send_file(output_file, mimetype='image/png', as_attachment=True, download_name='processed_image.png')
    else:
        return "No file uploaded", 400

def main():
    app.run(port=5001, debug=False)

if __name__ == "__main__":
    main()
