import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Database configuration
DATABASE_URL = f"sqlite:///{BASE_DIR}/picking_logs.db"

# Camera settings
CAMERA_ID = 0  # Default webcam
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# YOLO settings
YOLO_MODEL_PATH = "yolov8n.pt"
CONFIDENCE_THRESHOLD = 0.5

# LED settings (for Raspberry Pi)
LED_PIN = 18  # GPIO pin number for LED

# Flask settings
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True

# Logging settings
LOG_LEVEL = "INFO"
LOG_FILE = BASE_DIR / "app.log" 