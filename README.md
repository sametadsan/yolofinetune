# yolofinetune

input images path : "../yolofinetune/images"

run node main.js

make POST request on "http://localhost:3000/mask-plates"

download requirements : pip install -r requirements.txt

ssl-error : pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

run : python yolo_license_plate.py

run in background : Start-Process -NoNewWindow -FilePath "python" -ArgumentList "C:\path\to\your\application\yolo_license_plate.py"

create packages : pip download -r requirements.txt -d packages

create packages ssl error : pip download --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt -d packages

packages in run command : pip install --no-index --find-links=packages -r requirements.txt

PM2
npm install pm2

start app services : pm2 start ecosystem.config.js

status : pm2 status

changed ecosytem config : pm2 reload ecosystem.config.js

log : pm2 logs

detail : pm2 show YolofinetuneFlaskService

stop : pm2 stop YolofinetuneFlaskService

restart : pm2 restart YolofinetuneFlaskService

startup :
pm2 start ecosystem.config.js

pm2 start

npm install pm2-windows-startup -g

pm2 install pm2-windows-service

pm2-startup install

pm2 save

production:

python setup.py sdist bdist_wheel

/dist -> pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org yolofinetune-0.1.tar.gz

pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org yolofinetune-0.1-py3-none-any.whl

yolofinetune.exe created

pm2 start : pm2 start yolofinetune.exe --name yolofinetune

startup ->
pm2-startup install

pm2 save
