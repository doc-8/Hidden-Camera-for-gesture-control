
@author: dietr
"""
import cv2
import mediapipe as mp
import urllib.request
import time
import threading
import requests
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

# Initialize MediaPipe Drawing Utility
mp_drawing = mp.solutions.drawing_utils

# Define the function to detect the gesture
def detect_gesture(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    if abs(thumb_tip.x - index_finger_tip.x) < 0.05 and abs(thumb_tip.y - index_finger_tip.y) < 0.05:
        return 'Okay'
    elif thumb_tip.y < index_finger_tip.y and thumb_tip.y < middle_finger_tip.y and thumb_tip.y < ring_finger_tip.y and thumb_tip.y < pinky_tip.y:
        return 'Thumbs Up'
    else:
        return 'Unknown'

# Define the response functions; Add your raspberry pi pico host adress
def okay_response():
    def task():
        with urllib.request.urlopen('http://XXX.XXX.XXX.XX/light/on') as response:
            html = response.read()
        print('Okay gesture detected')
    threading.Thread(target=task).start()

def thumbs_up_response():
    def task():
        with urllib.request.urlopen('http://XXX.XXX.XXX.XX/light/off') as response:
            html = response.read()
        print('Thumbs Up gesture detected')
    threading.Thread(target=task).start()

# Initialize the time of last activation
last_activation_time = time.time() - 10

# Initialize the session and counter; Add your camera IP and password
s = requests.Session()
c = 0

while True:
    r = s.get('http://XXX.XXX.XXX.XX/PASSWORD', stream=True)
    if r.status_code == 200:
        bytes = b''
        for chunk in r.iter_content(chunk_size=1024):
            bytes += chunk
            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')
            if a != -1 and b != -1:
                c += 1
                jpg = bytes[a:b+2]
                bytes = bytes[b+2:]
                if len(jpg) > 0:
                    # Assuming 'jpg' is a bytes object containing the MJPEG data
                    buf_np = np.frombuffer(jpg, dtype=np.uint8)
                    # Decode the MJPEG data to a cv::Mat
                    img = cv2.imdecode(buf_np, cv2.IMREAD_COLOR)

                    # Convert the BGR image to RGB and process it with MediaPipe Hands
                    results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

                    # Convert the image color back so it can be displayed
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                    if results.multi_hand_landmarks is not None:
                        for hand_landmarks in results.multi_hand_landmarks:
                            # Draw hand landmarks
                            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                            # Detect gesture
                            gesture = detect_gesture(hand_landmarks)
                            # Check if 10 seconds have passed since the last activation
                            if time.time() - last_activation_time >= 10:
                                if gesture == 'Okay':
                                    okay_response()
                                    last_activation_time = time.time()
                                elif gesture == 'Thumbs Up':
                                    thumbs_up_response()
                                    last_activation_time = time.time()

                    # Display the frame
                    cv2.imshow('MediaPipe Hands', img)

                    if cv2.waitKey(5) & 0xFF == 27:
                        break

cv2.destroyAllWindows()

