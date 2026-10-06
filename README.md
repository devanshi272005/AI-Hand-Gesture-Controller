# 🤖 AI Hand Gesture Controller
![AI Hand Gesture Controller Demo](demo.png)
An AI-powered hand gesture recognition system that uses a webcam to detect hand gestures in real time and control computer media functions without using a keyboard or mouse.

## ✨ Features

* Real-time hand detection using a webcam
* Hand landmark tracking using MediaPipe
* Automatic finger counting
* Gesture recognition
* Gesture stabilization using multiple frames
* Computer media control using PyAutoGUI
* Professional on-screen gesture control panel
* Mirror camera view
* Supports multiple hand gestures

## 🖐️ Gesture Controls

| Hand Gesture  | Computer Action |
| ------------- | --------------- |
| 👍 Thumbs Up  | Volume Up       |
| ✊ Fist        | Volume Down     |
| 🖐️ Open Palm | Play / Pause    |
| ✌️ Peace      | Next Track      |
| ☝️ One Finger | Previous Track  |

## 🛠️ Technologies Used

* Python
* OpenCV
* MediaPipe
* NumPy
* PyAutoGUI

## 📁 Project Structure

```text
Hand-Gesture-Recognition/
│
├── main.py
├── README.md
└── venv/
```

## ⚙️ Installation

Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\activate
```

Install the required libraries:

```powershell
pip install opencv-python numpy mediapipe==0.10.21 pyautogui
```

## ▶️ How to Run

Activate the virtual environment and run:

```powershell
python main.py
```

The webcam window will open automatically.

Show a supported hand gesture in front of the camera and the corresponding computer action will be performed.

Press **Q** to exit the application.

## 🧠 How It Works

1. The webcam captures the user's hand.
2. OpenCV processes the camera frames.
3. MediaPipe detects hand landmarks.
4. The program analyzes finger positions.
5. The detected gesture is confirmed across multiple frames for better stability.
6. PyAutoGUI performs the corresponding computer control action.

## 🔮 Future Improvements

* Add more gestures
* Support multiple hands
* Add custom user-defined gestures
* Improve recognition under different lighting conditions
* Add voice feedback
* Add a graphical settings interface
* Add application-specific controls

## 👩‍💻 Author

**Devanshi **

CSE Student | Python & AI Enthusiast
