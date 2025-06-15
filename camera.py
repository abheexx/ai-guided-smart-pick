import cv2
import threading
import time
import logging
from config import CAMERA_ID, CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_FPS

logger = logging.getLogger(__name__)

class Camera:
    def __init__(self):
        """Initialize the camera with specified settings."""
        self.camera_id = CAMERA_ID
        self.width = CAMERA_WIDTH
        self.height = CAMERA_HEIGHT
        self.fps = CAMERA_FPS
        self.cap = None
        self.frame = None
        self.is_running = False
        self.thread = None
        self.lock = threading.Lock()

    def start(self):
        """Start the camera capture in a separate thread."""
        if self.is_running:
            return

        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)

            if not self.cap.isOpened():
                raise RuntimeError("Failed to open camera")

            self.is_running = True
            self.thread = threading.Thread(target=self._update_frame)
            self.thread.daemon = True
            self.thread.start()
            logger.info("Camera started successfully")
        except Exception as e:
            logger.error(f"Failed to start camera: {e}")
            self.cleanup()
            raise

    def _update_frame(self):
        """Update frame in a loop."""
        while self.is_running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.frame = frame
            else:
                logger.warning("Failed to capture frame")
                time.sleep(0.1)

    def get_frame(self):
        """Get the current frame."""
        with self.lock:
            if self.frame is None:
                return None
            return self.frame.copy()

    def stop(self):
        """Stop the camera capture."""
        self.is_running = False
        if self.thread:
            self.thread.join()
        self.cleanup()

    def cleanup(self):
        """Clean up camera resources."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.frame = None
        logger.info("Camera resources cleaned up")

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()

# Create a singleton instance
camera = Camera() 