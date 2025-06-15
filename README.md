# AI-Guided Smart Pick System

An intelligent warehouse logistics system that uses computer vision and AI to guide workers to the correct boxes on shelves.

## Overview

This system combines YOLOv8 object detection with a web interface to create an efficient picking system for warehouses. It can:
- Detect boxes on shelves in real-time using a webcam
- Identify the correct box based on order ID
- Guide workers using LED indicators
- Track all picking activities in a database
- Provide a user-friendly web interface

## Tech Stack

- **Backend**: Python 3.8+
- **Web Framework**: Flask
- **Computer Vision**: OpenCV, YOLOv8
- **Database**: SQLite
- **Hardware**: Webcam, LED indicators (simulated or Raspberry Pi GPIO)

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-guided-smart-pick.git
cd ai-guided-smart-pick
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download YOLOv8 weights:
```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

5. Run the application:
```bash
python app.py
```

6. Access the web interface at `http://localhost:5000`

## Project Structure

```
ai-guided-smart-pick/
├── app.py              # Main Flask application
├── camera.py           # Camera handling
├── yolo_detector.py    # YOLO detection logic
├── hardware.py         # LED control
├── db.py              # Database operations
├── config.py          # Configuration settings
├── requirements.txt   # Project dependencies
└── README.md          # Project documentation
```


## Future Improvements

1. **Robot Arm Integration**
   - Add support for automated picking using robotic arms
   - Implement collision avoidance
   - Add force feedback for delicate items

2. **Enhanced Detection**
   - Support for multiple camera angles
   - Improved box detection accuracy
   - Barcode/QR code scanning integration

3. **Advanced Features**
   - Real-time inventory tracking
   - Order optimization
   - Worker performance analytics
   - Mobile app support

4. **System Improvements**
   - Distributed processing for multiple workstations
   - Cloud synchronization
   - Real-time monitoring dashboard
   - Integration with existing warehouse management systems

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
