"""
Virtual Drawing App — Hand Gesture (MediaPipe 0.10.x + OpenCV)
---------------------------------------------------------------
Compatible with mediapipe >= 0.10.30 (uses the new Tasks API)

Controls:
  • Index up + middle folded  → Draw
  • Both fingers up           → Pen lifted (move freely)
  • C key                     → Clear canvas
  • Q / ESC                   → Quit
  • 1-5 keys                  → Change color
  • +/- keys                  → Change brush size
"""

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision
import urllib.request
import os

# ── Download model file if not present ───────────────────────────────────────
MODEL_PATH = "hand_landmarker.task"
MODEL_URL  = (
    "https://storage.googleapis.com/mediapipe-models/"
    "hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
)

if not os.path.exists(MODEL_PATH):
    print("Downloading hand landmarker model (~8 MB)…")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("Model downloaded.")

# ── MediaPipe Hand Landmarker setup ──────────────────────────────────────────
base_options = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
options = mp_vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=mp_vision.RunningMode.IMAGE,
    num_hands=1,
    min_hand_detection_confidence=0.6,
    min_hand_presence_confidence=0.6,
    min_tracking_confidence=0.5,
)
detector = mp_vision.HandLandmarker.create_from_options(options)

# Hand skeleton connections (MediaPipe 21-landmark layout)
HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (0,9),(9,10),(10,11),(11,12),
    (0,13),(13,14),(14,15),(15,16),
    (0,17),(17,18),(18,19),(19,20),
    (5,9),(9,13),(13,17),
]

# ── Color palette (BGR) ───────────────────────────────────────────────────────
COLORS = {
    "1": (  0, 255, 255),   # yellow
    "2": (255,  80,  80),   # blue
    "3": ( 80, 255,  80),   # green
    "4": ( 80,  80, 255),   # red
    "5": (255, 255, 255),   # white
}
COLOR_NAMES = {"1": "Yellow", "2": "Blue", "3": "Green", "4": "Red", "5": "White"}

# ── App state ─────────────────────────────────────────────────────────────────
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

ret, frame = cap.read()
if not ret:
    raise RuntimeError("Cannot open webcam.")

h, w    = frame.shape[:2]
canvas  = np.zeros((h, w, 3), dtype=np.uint8)
prev_pt = None
draw_color = COLORS["1"]
color_name = COLOR_NAMES["1"]
brush_size = 6
smoothed_pt = None

# ── Helpers ───────────────────────────────────────────────────────────────────

def get_tip(landmarks):
    """Index finger tip = landmark index 8."""
    lm = landmarks[8]
    return int(lm.x * w), int(lm.y * h)


def smooth(new_pt, old_pt, alpha=0.5):
    if old_pt is None:
        return new_pt
    return (
        int(alpha * new_pt[0] + (1 - alpha) * old_pt[0]),
        int(alpha * new_pt[1] + (1 - alpha) * old_pt[1]),
    )


def is_drawing(landmarks):
    """
    Draw when index finger is UP and middle finger is DOWN.
    Uses y-coordinate: smaller y = higher on screen.
    """
    index_up  = landmarks[8].y  < landmarks[6].y   # tip above PIP
    middle_up = landmarks[12].y < landmarks[10].y
    return index_up and not middle_up


def draw_skeleton(img, landmarks):
    """Draw hand skeleton manually from landmark list."""
    pts = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
    for connection in HAND_CONNECTIONS:
        a, b = connection
        cv2.line(img, pts[a], pts[b], (80, 80, 80), 1, cv2.LINE_AA)
    for pt in pts:
        cv2.circle(img, pt, 3, (150, 150, 150), -1, cv2.LINE_AA)


def draw_hud(img, color, cname, size):
    overlay = img.copy()
    cv2.rectangle(overlay, (0, 0), (260, h), (15, 15, 15), -1)
    cv2.addWeighted(overlay, 0.55, img, 0.45, 0, img)

    cv2.putText(img, "VIRTUAL DRAW", (12, 36),
                cv2.FONT_HERSHEY_DUPLEX, 0.85, (200, 200, 200), 1, cv2.LINE_AA)

    cv2.rectangle(img, (12, 55), (52, 95), color, -1)
    cv2.rectangle(img, (12, 55), (52, 95), (200, 200, 200), 1)
    cv2.putText(img, cname, (60, 83),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (200, 200, 200), 1, cv2.LINE_AA)

    cv2.circle(img, (32, 128), max(2, size), color, -1)
    cv2.putText(img, f"Size: {size}", (60, 134),
                cv2.FONT_HERSHEY_SIMPLEX, 0.58, (180, 180, 180), 1, cv2.LINE_AA)

    tips = [
        "1-5  Change color",
        "+/-  Brush size",
        " C   Clear canvas",
        " Q   Quit",
        "",
        "Raise index finger",
        "Fold middle finger",
        "to DRAW",
    ]
    for i, t in enumerate(tips):
        cv2.putText(img, t, (12, 180 + i * 24),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48, (140, 140, 140), 1, cv2.LINE_AA)


# ── Main loop ─────────────────────────────────────────────────────────────────
print("Virtual Drawing App started. Press Q or ESC to quit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

    result      = detector.detect(mp_img)
    active_draw = False

    if result.hand_landmarks:
        landmarks = result.hand_landmarks[0]   # first hand

        draw_skeleton(frame, landmarks)

        raw_pt      = get_tip(landmarks)
        smoothed_pt = smooth(raw_pt, smoothed_pt)

        if is_drawing(landmarks):
            active_draw = True
            if prev_pt:
                cv2.line(canvas, prev_pt, smoothed_pt, draw_color,
                         brush_size, cv2.LINE_AA)
            prev_pt = smoothed_pt
        else:
            prev_pt = None

        ring_color = draw_color if active_draw else (100, 100, 100)
        cv2.circle(frame, smoothed_pt, brush_size + 6, ring_color, 2, cv2.LINE_AA)
        cv2.circle(frame, smoothed_pt, 3, (255, 255, 255), -1, cv2.LINE_AA)
    else:
        prev_pt     = None
        smoothed_pt = None

    # Blend canvas onto frame
    mask = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
    blended = cv2.addWeighted(frame, 0.15, canvas, 0.85, 0)
    frame[mask > 0] = blended[mask > 0]

    draw_hud(frame, draw_color, color_name, brush_size)

    dot_color = (0, 255, 100) if active_draw else (60, 60, 60)
    cv2.circle(frame, (w - 20, 20), 10, dot_color, -1, cv2.LINE_AA)

    cv2.imshow("Virtual Drawing App  |  Press Q to quit", frame)

    key = cv2.waitKey(1) & 0xFF
    if key in (ord("q"), 27):
        break
    elif key == ord("c"):
        canvas[:] = 0
        prev_pt   = None
    elif chr(key) in COLORS:
        draw_color = COLORS[chr(key)]
        color_name = COLOR_NAMES[chr(key)]
    elif key == ord("+"):
        brush_size = min(40, brush_size + 2)
    elif key == ord("-"):
        brush_size = max(2, brush_size - 2)

cap.release()
cv2.destroyAllWindows()
detector.close()
print("App closed.")
