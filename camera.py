import cv2
import mediapipe as mp

# Initialize MediaPipe hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

def get_gesture(landmarks):
    """A basic rule-based gesture recognizer.
    Returns: string representing gesture name."""
    # Example: Index and middle finger up, others down == 'Peace'
    if not landmarks:
        return "No Hand Detected"
    tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky tips
    finger_up = []
    for tip in tips:
        # Finger is up if tip is above pip joint (y coordinate is less in image coordinates)
        finger_up.append(landmarks[tip].y < landmarks[tip - 2].y)
    thumb_up = landmarks[4].x < landmarks[3].x  # Right hand only

    # Interpret gestures:
    if all(finger_up):
        return "Open Palm"
    elif not any(finger_up):
        return "Fist"
    elif finger_up[0] and finger_up[1] and not finger_up[2] and not finger_up[3]:
        return "Peace"
    elif finger_up[0] and not any(finger_up[1:]):
        return "Pointing (Index)"
    elif thumb_up and not any(finger_up):
        return "Thumbs Up"
    else:
        return "Unknown Gesture"

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    gesture = "No Hand Detected"
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture = get_gesture(hand_landmarks.landmark)
    # Display detected gesture as text on the image
    cv2.putText(img, f'Gesture: {gesture}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3)
    cv2.imshow("Hand Gesture to Text", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()