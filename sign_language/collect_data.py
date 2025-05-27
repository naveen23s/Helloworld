import cv2
import mediapipe as mp
import numpy as np
import pandas as pd

# List your target gestures (expand as needed)
GESTURES = ['A', 'B', 'C']  # Change/add more as required
SAMPLES_PER_GESTURE = 100

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

all_data = []

cap = cv2.VideoCapture(0)

for gesture in GESTURES:
    print(f"Show gesture '{gesture}'")
    count = 0
    while count < SAMPLES_PER_GESTURE:
        ret, frame = cap.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            landmarks = []
            for lm in hand.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])
            all_data.append(landmarks + [gesture])
            count += 1
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            cv2.putText(frame, f'{gesture}: {count}/{SAMPLES_PER_GESTURE}', (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        else:
            cv2.putText(frame, 'No hand detected', (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        cv2.imshow("Collecting Data", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC to skip gesture
            break

cap.release()
cv2.destroyAllWindows()

# Save to CSV
df = pd.DataFrame(all_data)
cols = [f'lm{i}' for i in range(len(all_data[0])-1)] + ['label']
df.columns = cols
df.to_csv('asl_data.csv', index=False)
print("Data collection complete and asl_data.csv file")