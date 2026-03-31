Virtual Drawing App — Hand Gesture

Draw on your screen using just your index finger via webcam — no mouse, no stylus required.

This project uses real-time hand tracking to convert finger movements into digital drawing strokes, creating a natural and interactive human-computer interface.

🚀 Features
✋ Gesture-based drawing (no physical input device)
🎯 Accurate fingertip tracking using 21 hand landmarks
✍️ Smooth strokes with EMA (Exponential Moving Average)
🎨 5-color palette switching (live)
📏 Adjustable brush size (2–40 px)
🧼 Clear canvas with a key press
🔵 Live cursor indicator
🟢 Draw mode indicator
🛠️ Tech Stack
Library	Role
MediaPipe	Hand tracking (21 landmarks detection)
OpenCV	Video capture & drawing
NumPy	Canvas and array operations
📦 Installation & Setup

Follow these steps carefully. No prior setup is assumed.

1. Clone the Repository
git clone https://github.com/your-username/virtual-drawing-app.git
cd virtual-drawing-app
2. Create Virtual Environment (Recommended)
python -m venv venv

Activate it:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
3. Install Dependencies
pip install opencv-python mediapipe numpy
4. Run the Application
python virtual_draw.py
🎮 Controls
Key / Gesture	Action
☝️ Index up, middle folded	Draw
✌️ Index + middle up	Move cursor (no drawing)
C	Clear canvas
1 – 5	Change color (Yellow / Blue / Green / Red / White)
+ / -	Increase / decrease brush size
Q / ESC	Quit
⚙️ How It Works
Webcam Input
     ↓
MediaPipe Hand Detection
     ↓
21 Hand Landmarks Identified
     ↓
Index Finger Tip (Landmark 8)
     ↓
Gesture Detection Logic
     ↓
EMA Smoothing (Noise Reduction)
     ↓
Drawing on Canvas (cv2.line)
     ↓
Overlay Canvas on Frame
     ↓
Display Output (Real-time)
Core Logic
The system detects the index finger tip position
Gesture conditions determine whether to draw or not:
Index finger UP
Middle finger DOWN
If conditions are satisfied → drawing starts
Otherwise → cursor moves without drawing
🧠 Key Concepts Used
Real-time video processing
Hand landmark detection
Gesture recognition logic
Noise reduction using EMA
Frame overlay and rendering
📁 Project Structure
virtual-drawing-app/
│
├── virtual_draw.py      # Main application file
├── README.md            # Project documentation
└── requirements.txt     # (Optional) dependencies
⚡ Performance
Runs at ~20–30 FPS on standard systems
Works best under good lighting conditions
Single-hand tracking optimized
⚠️ Limitations
Reduced accuracy in low light
No multi-hand support
Limited gesture set
🔮 Future Improvements
Multi-hand interaction
Gesture-based tool selection
Save drawings as images
GUI-based controls
AR/VR integration
