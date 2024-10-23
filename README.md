# yolofinetune

input images path : "../yolofinetune/images"

run node main.js

make POST request on "http://localhost:3000/mask-plates"

download requirements : pip install -r requirements.txt

ssl-error : pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

run : python yolo_license_plate.py

run in background : Start-Process -NoNewWindow -FilePath "python" -ArgumentList "C:\path\to\your\application\yolo_license_plate.py"
