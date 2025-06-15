import cv2
import base64
import logging
from flask import Flask, render_template, Response, request, jsonify
from camera import camera
from yolo_detector import box_detector
from hardware import led_controller
from db import init_db, add_picking_log, get_picking_logs, update_picking_status
from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG
import threading
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global variables
current_order_id = None
selected_box_id = None
detection_thread = None
is_detecting = False

def encode_frame(frame):
    """Encode frame to base64 for streaming."""
    if frame is None:
        return None
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')

def detection_loop():
    """Main detection loop running in a separate thread."""
    global selected_box_id, is_detecting
    
    while is_detecting:
        frame = camera.get_frame()
        if frame is None:
            continue

        # Detect boxes
        boxes = box_detector.detect_boxes(frame)
        
        # If we have an order ID, find the corresponding box
        if current_order_id and boxes:
            # In a real system, you would have a mapping between order IDs and box IDs
            # For demo purposes, we'll just select the first box
            selected_box_id = boxes[0]['box_id']
            led_controller.turn_on()
            
            # Log the detection
            add_picking_log(
                order_id=current_order_id,
                box_id=selected_box_id,
                confidence=boxes[0]['confidence']
            )
        else:
            selected_box_id = None
            led_controller.turn_off()

        # Draw boxes on frame
        frame = box_detector.draw_boxes(frame, boxes, selected_box_id)
        
        time.sleep(0.1)  # Prevent CPU overload

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Stream the video feed."""
    def generate():
        while True:
            frame = camera.get_frame()
            if frame is not None:
                # Draw boxes on frame
                boxes = box_detector.detect_boxes(frame)
                frame = box_detector.draw_boxes(frame, boxes, selected_box_id)
                
                # Encode frame
                encoded_frame = encode_frame(frame)
                if encoded_frame:
                    yield f"data:image/jpeg;base64,{encoded_frame}\n\n"
            time.sleep(0.1)

    return Response(generate(), mimetype='text/event-stream')

@app.route('/start_detection', methods=['POST'])
def start_detection():
    """Start the detection process."""
    global is_detecting, detection_thread
    
    if not is_detecting:
        is_detecting = True
        detection_thread = threading.Thread(target=detection_loop)
        detection_thread.daemon = True
        detection_thread.start()
        return jsonify({'status': 'success', 'message': 'Detection started'})
    return jsonify({'status': 'error', 'message': 'Detection already running'})

@app.route('/stop_detection', methods=['POST'])
def stop_detection():
    """Stop the detection process."""
    global is_detecting, detection_thread
    
    if is_detecting:
        is_detecting = False
        if detection_thread:
            detection_thread.join()
        led_controller.turn_off()
        return jsonify({'status': 'success', 'message': 'Detection stopped'})
    return jsonify({'status': 'error', 'message': 'Detection not running'})

@app.route('/set_order', methods=['POST'])
def set_order():
    """Set the current order ID."""
    global current_order_id
    data = request.get_json()
    if data and 'order_id' in data:
        current_order_id = data['order_id']
        return jsonify({'status': 'success', 'message': f'Order ID set to {current_order_id}'})
    return jsonify({'status': 'error', 'message': 'No order ID provided'})

@app.route('/get_logs')
def get_logs():
    """Get picking logs."""
    order_id = request.args.get('order_id')
    logs = get_picking_logs(order_id)
    return jsonify([{
        'id': log.id,
        'order_id': log.order_id,
        'box_id': log.box_id,
        'timestamp': log.timestamp.isoformat(),
        'confidence': log.confidence,
        'status': log.status
    } for log in logs])

def cleanup():
    """Clean up resources."""
    global is_detecting
    is_detecting = False
    if detection_thread:
        detection_thread.join()
    camera.stop()
    led_controller.cleanup()

if __name__ == '__main__':
    try:
        # Initialize database
        init_db()
        
        # Start camera
        camera.start()
        
        # Run Flask app
        app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
    except Exception as e:
        logger.error(f"Application error: {e}")
    finally:
        cleanup() 