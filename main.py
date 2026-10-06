import cv2
import mediapipe as mp
import pyautogui
import time


# -----------------------------
# MediaPipe setup
# -----------------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)


# -----------------------------
# Camera setup
# -----------------------------
cap = cv2.VideoCapture(0)

# Better camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# -----------------------------
# Gesture stabilization
# -----------------------------
candidate_gesture = "No Hand"
stable_gesture = "No Hand"

gesture_frames = 0
required_frames = 5

last_action_time = 0
cooldown = 1.2


# -----------------------------
# Function: Count fingers
# -----------------------------
def count_fingers(hand_landmarks, handedness):
    landmarks = hand_landmarks.landmark

    fingers = []

    # Thumb
    if handedness == "Right":
        if landmarks[4].x < landmarks[3].x:
            fingers.append(1)
        else:
            fingers.append(0)
    else:
        if landmarks[4].x > landmarks[3].x:
            fingers.append(1)
        else:
            fingers.append(0)

    # Index finger
    if landmarks[8].y < landmarks[6].y:
        fingers.append(1)
    else:
        fingers.append(0)

    # Middle finger
    if landmarks[12].y < landmarks[10].y:
        fingers.append(1)
    else:
        fingers.append(0)

    # Ring finger
    if landmarks[16].y < landmarks[14].y:
        fingers.append(1)
    else:
        fingers.append(0)

    # Pinky
    if landmarks[20].y < landmarks[18].y:
        fingers.append(1)
    else:
        fingers.append(0)

    return fingers


# -----------------------------
# Function: Detect gesture
# -----------------------------
def get_gesture(fingers):

    # PEACE: index + middle open, baaki closed
    if (
        fingers[0] == 0
        and fingers[1] == 1
        and fingers[2] == 1
        and fingers[3] == 0
        and fingers[4] == 0
    ):
        return "PEACE"

    finger_count = sum(fingers)

    if finger_count == 0:
        return "FIST"

    elif finger_count == 1:
        if fingers[0] == 1:
            return "THUMBS UP"
        else:
            return "ONE"

    elif finger_count == 2:
        return "PEACE"

    elif finger_count == 3:
        return "THREE"

    elif finger_count == 4:
        return "FOUR"

    elif finger_count == 5:
        return "OPEN PALM"

    else:
        return "UNKNOWN"

# -----------------------------
# Main loop
# -----------------------------
while True:

    success, frame = cap.read()

    if not success:
        print("Camera frame nahi mil raha!")
        break

    # Mirror effect
    frame = cv2.flip(frame, 1)

    # Convert BGR -> RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hand
    results = hands.process(rgb_frame)

    # Default values
    gesture = "No Hand"
    finger_count = 0

    # -----------------------------
    # Hand detected
    # -----------------------------
    if results.multi_hand_landmarks:

        hand_landmarks = results.multi_hand_landmarks[0]

        # Draw landmarks
        mp_draw.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )

        # Get handedness
        handedness = results.multi_handedness[0].classification[0].label

        # Count fingers
        fingers = count_fingers(
            hand_landmarks,
            handedness
        )

        finger_count = sum(fingers)

        # Detect gesture
        gesture = get_gesture(fingers)


    # -----------------------------
    # Gesture stabilization
    # -----------------------------

    if gesture == candidate_gesture:

        gesture_frames += 1

    else:

        candidate_gesture = gesture
        gesture_frames = 1


    # Confirm gesture only after 5 frames
    if gesture_frames >= required_frames:

        stable_gesture = candidate_gesture


    # -----------------------------
    # Computer control
    # -----------------------------

    current_time = time.time()

    if (
        stable_gesture != "No Hand"
        and stable_gesture != "UNKNOWN"
        and current_time - last_action_time > cooldown
    ):

        if stable_gesture == "THUMBS UP":

            pyautogui.press("volumeup")
            last_action_time = current_time

        elif stable_gesture == "FIST":

            pyautogui.press("volumedown")
            last_action_time = current_time

        elif stable_gesture == "OPEN PALM":

            pyautogui.press("playpause")
            last_action_time = current_time

        elif stable_gesture == "PEACE":

            pyautogui.press("nexttrack")
            last_action_time = current_time

        elif stable_gesture == "ONE":

            pyautogui.press("prevtrack")
            last_action_time = current_time


        # -----------------------------
    # Display information
    # -----------------------------

    cv2.rectangle(
        frame,
        (10, 10),
        (430, 125),
        (0, 0, 0),
        -1
    )

    cv2.putText(
        frame,
        "AI HAND GESTURE CONTROLLER",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Gesture: {stable_gesture}",
        (20, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Fingers: {finger_count}",
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Q = Exit",
        (20, 115),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    # -----------------------------
    # Controls panel
    # -----------------------------

    cv2.rectangle(
        frame,
        (10, 135),
        (430, 300),
        (0, 0, 0),
        -1
    )

    cv2.putText(
        frame,
        "GESTURE CONTROLS",
        (20, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "THUMBS UP  -> Volume Up",
        (20, 188),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (255, 255, 255),
        1
    )

    cv2.putText(
        frame,
        "FIST        -> Volume Down",
        (20, 214),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (255, 255, 255),
        1
    )

    cv2.putText(
        frame,
        "OPEN PALM   -> Play/Pause",
        (20, 240),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (255, 255, 255),
        1
    )

    cv2.putText(
        frame,
        "PEACE       -> Next Track",
        (20, 266),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (255, 255, 255),
        1
    )

    cv2.putText(
        frame,
        "ONE         -> Previous Track",
        (20, 292),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (255, 255, 255),
        1
    )

    # Show camera
    cv2.imshow(
        "AI Hand Gesture Controller",
        frame
    )

    # Exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# -----------------------------
# Cleanup
# -----------------------------

cap.release()
cv2.destroyAllWindows()
hands.close()