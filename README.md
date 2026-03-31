# 🎨 Virtual Drawing App — Hand Gesture

Draw on your screen using your **index finger via webcam** — no mouse, no stylus required.

This project uses real-time hand tracking to convert finger movements into digital drawing strokes, creating a natural and interactive human-computer interface.

---

## 🚀 Features

- ✋ Gesture-based drawing (no physical input device)
- 🎯 Accurate fingertip tracking using 21 hand landmarks
- ✍️ Smooth strokes with EMA (Exponential Moving Average)
- 🎨 5-color palette switching (live)
- 📏 Adjustable brush size (2–40 px)
- 🧼 Clear canvas with a key press
- 🔵 Live fingertip cursor indicator
- 🟢 Active draw mode indicator

---

## 🛠️ Tech Stack

- **MediaPipe** — Hand tracking (21 landmarks detection)
- **OpenCV** — Webcam capture and drawing
- **NumPy** — Canvas and array operations

---

## 📦 Installation & Setup

Follow these steps carefully:

### 1. Clone the Repository




2. Create Virtual Environment (Recommended)
python -m venv venv
Activate it:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
## ⚙️ How It Works

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

## Core Logic
The system tracks the index finger tip position
Drawing happens only when:
Index finger is UP
Middle finger is DOWN
Otherwise, the cursor moves without drawing


## 📁 Project Structure
virtual-drawing-app/
│
├── virtual_draw.py
├── README.md
└── requirements.txt

## ⚡ Performance
Runs at ~20–30 FPS on standard systems
Works best in good lighting conditions
Optimized for single-hand tracking

## ⚠️ Limitations
Reduced accuracy in low light
No multi-hand support
Limited gesture set

## 🔮 Future Improvements
Multi-hand interaction
Gesture-based tool selection
Save drawings as images
