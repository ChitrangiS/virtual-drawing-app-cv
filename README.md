
# Virtual Drawing Application using Hand Gesture Recognition

---

## 1. Project Overview

The Virtual Drawing Application is a computer vision-based system that enables users to draw on a digital canvas using hand gestures captured through a webcam. The system eliminates the need for traditional input devices such as a mouse or stylus by leveraging real-time hand tracking.

The application uses hand landmark detection to identify the position of the index finger and maps its movement onto the screen to simulate drawing. It provides an intuitive and interactive interface, demonstrating the practical application of gesture-based human-computer interaction.

---

## 2. Features

- Real-time hand tracking using webcam input  
- Gesture-based drawing using index finger  
- Smooth drawing using noise reduction techniques (EMA smoothing)  
- Multiple color options for drawing  
- Adjustable brush size  
- Clear canvas functionality  
- Real-time rendering and visual feedback  

---

## 3. System Requirements

### Hardware Requirements

- A system with a working webcam  
- Minimum 4 GB RAM (8 GB recommended)  
- Processor: Intel i3 or equivalent and above  

### Software Requirements

- Python 3.8 or higher  
- Operating System: Windows, macOS, or Linux  

---

## 4. Environment Setup

It is recommended to create a virtual environment to manage dependencies effectively.

### Step 1: Create a Virtual Environment

```bash
python -m venv venv
##  How It Works

Webcam Input
     ↓
MediaPipe Hand Detection
     ↓
21 Hand Landmarks
     ↓
Index Finger Tip (Landmark 8)
     ↓
Gesture Detection
     ↓
EMA Smoothing
     ↓
Drawing using OpenCV
     ↓
Overlay Canvas
     ↓
Real-time Display
```
## Core Logic
The system tracks the index finger tip position
Drawing happens only when:
Index finger is UP
Middle finger is DOWN
Otherwise, the cursor moves without drawing


## Project Structure
virtual-drawing-app/
│
├── virtual_draw.py
├── README.md
└── requirements.txt

##  Performance
Runs at ~20–30 FPS on standard systems
Works best in good lighting conditions
Optimized for single-hand tracking

##  Limitations
Reduced accuracy in low light
No multi-hand support
Limited gesture set

##  Future Improvements
Multi-hand interaction
Gesture-based tool selection
Save drawings as images
