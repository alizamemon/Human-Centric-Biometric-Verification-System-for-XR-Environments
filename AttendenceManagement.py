import os
import sys
import numpy as np
import cv2
from datetime import datetime
import face_recognition

# Models path setup
os.environ['FACE_RECOGNITION_MODELS_PATH'] = r'F:\Web development\python\.venv\Lib\site-packages\face_recognition_models\models'

# Settings
PATH = 'known_faces'
ATTENDANCE_FILE = 'Attendance.csv'
FIXED_TIME = "09:00:00" 
THRESHOLD = 0.45 
BLINK_COOLDOWN_FRAMES = 10 # To prevent multiple triggers in one blink

# Load Known Faces
images = []
classNames = []
myList = os.listdir(PATH)
for cl in myList:
    curImg = cv2.imread(f'{PATH}/{cl}')
    if curImg is not None:
        images.append(curImg)
        raw_name = os.path.splitext(cl)[0]
        clean_name = raw_name.split('_')[0] 
        classNames.append(clean_name)

def get_ear(eye_points):
    A = np.linalg.norm(np.array(eye_points[1]) - np.array(eye_points[5]))
    B = np.linalg.norm(np.array(eye_points[2]) - np.array(eye_points[4]))
    C = np.linalg.norm(np.array(eye_points[0]) - np.array(eye_points[3]))
    return (A + B) / (2.0 * C)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if len(encodes) > 0: encodeList.append(encodes[0])
    return encodeList

def markAttendance(name):
    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, 'w') as f:
            f.writelines('Name,Time,Status')
    
    with open(ATTENDANCE_FILE, 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.split(',')[0] for line in myDataList]
        if name not in nameList:
            now = datetime.now()
            currentTime = now.strftime('%H:%M:%S')
            status = "Present" if currentTime <= FIXED_TIME else "Late"
            f.writelines(f'\n{name},{currentTime},{status}')
            print(f"!!! Intentional Verification Marked: {name} !!!")
            return True
    return False

print('Encoding... Please wait.')
encodeListKnown = findEncodings(images)
print('System Ready. BLINK to verify identity!')

cap = cv2.VideoCapture(0)
blink_counter = 0 # Cooldown counter

while True:
    success, img = cap.read()
    if not success: break
    
    if blink_counter > 0:
        blink_counter -= 1

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    face_landmarks_list = face_recognition.face_landmarks(imgS)

    for encodeFace, faceLoc, landmarks in zip(encodesCurFrame, facesCurFrame, face_landmarks_list):
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        
        # Improvement 1: Safety Check for empty distances
        if len(faceDis) == 0:
            continue

        matchIndex = np.argmin(faceDis)

        if faceDis[matchIndex] < THRESHOLD:
            name = classNames[matchIndex].upper()
            
            # Eye Tracking Logic
            left_ear = get_ear(landmarks['left_eye'])
            right_ear = get_ear(landmarks['right_eye'])
            ear = (left_ear + right_ear) / 2.0
            
            is_already_marked = False
            if os.path.exists(ATTENDANCE_FILE):
                with open(ATTENDANCE_FILE, 'r') as f:
                    marked_names = [line.split(',')[0] for line in f.readlines()]
                is_already_marked = name in marked_names

            # Improvement 2: Debounced Blink Trigger
            if ear < 0.21 and not is_already_marked and blink_counter == 0:
                markAttendance(name)
                is_already_marked = True
                blink_counter = BLINK_COOLDOWN_FRAMES

            now_time = datetime.now().strftime('%H:%M:%S')
            color = (0, 255, 0) if now_time <= FIXED_TIME else (0, 0, 255)
            status_text = "VERIFIED" if is_already_marked else "BLINK TO VERIFY"
            display_label = f"{name}: {status_text}"
        else:
            display_label = "UNKNOWN IDENTITY"
            color = (0, 165, 255) 

        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), color, cv2.FILLED)
        cv2.putText(img, display_label, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow('Human-Centric Biometric Verification', img)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()