module.exports = {
  apps: [
    {
      name: 'YolofinetuneFlaskService',
      script: 'yolo_license_plate_flask.py',
      interpreter: 'python',
      instances: 1,
      exec_mode: 'fork',
      watch: false, // Dosya değişikliklerini izleme
      env: {
        FLASK_ENV: 'production', // Ortam değişkenleri (isteğe bağlı)
        PORT: 5001,
      },
    },
  ],
}
