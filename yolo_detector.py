import cv2
import numpy as np
from ultralytics import YOLO
import logging
from config import YOLO_MODEL_PATH, CONFIDENCE_THRESHOLD

logger = logging.getLogger(__name__)

class BoxDetector:
    def __init__(self):
        """Initialize the YOLO model for box detection."""
        try:
            self.model = YOLO(YOLO_MODEL_PATH)
            logger.info(f"Successfully loaded YOLO model from {YOLO_MODEL_PATH}")
        except Exception as e:
            logger.error(f"Failed to load YOLO model: {e}")
            raise

    def detect_boxes(self, frame):
        """
        Detect boxes in the given frame.
        
        Args:
            frame: numpy array containing the image
            
        Returns:
            list of dictionaries containing box information:
            {
                'box_id': str,
                'confidence': float,
                'bbox': [x1, y1, x2, y2]
            }
        """
        try:
            results = self.model(frame, conf=CONFIDENCE_THRESHOLD)[0]
            boxes = []
            
            for i, det in enumerate(results.boxes.data):
                x1, y1, x2, y2, conf, cls = det
                if conf >= CONFIDENCE_THRESHOLD:
                    box_info = {
                        'box_id': f'box_{i}',
                        'confidence': float(conf),
                        'bbox': [int(x1), int(y1), int(x2), int(y2)]
                    }
                    boxes.append(box_info)
            
            return boxes
        except Exception as e:
            logger.error(f"Error during box detection: {e}")
            return []

    def draw_boxes(self, frame, boxes, selected_box_id=None):
        """
        Draw bounding boxes on the frame.
        
        Args:
            frame: numpy array containing the image
            boxes: list of box dictionaries
            selected_box_id: ID of the selected box to highlight
            
        Returns:
            frame with drawn boxes
        """
        frame_copy = frame.copy()
        
        for box in boxes:
            x1, y1, x2, y2 = box['bbox']
            box_id = box['box_id']
            conf = box['confidence']
            
            # Choose color based on whether this is the selected box
            color = (0, 255, 0) if box_id == selected_box_id else (0, 0, 255)
            
            # Draw rectangle
            cv2.rectangle(frame_copy, (x1, y1), (x2, y2), color, 2)
            
            # Draw label
            label = f"{box_id} ({conf:.2f})"
            cv2.putText(frame_copy, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        return frame_copy

    def get_box_center(self, box):
        """Calculate the center point of a box."""
        x1, y1, x2, y2 = box['bbox']
        return ((x1 + x2) // 2, (y1 + y2) // 2)

# Create a singleton instance
box_detector = BoxDetector() 