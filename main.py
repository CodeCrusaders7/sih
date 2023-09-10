import cv2
import mediapipe as mp
import time
import numpy as np

def isCrawl(array) :
    return True

def isJump(array) :
    return True

def isRun(array) :
    return True
def classifyAction(array) :
    if isCrawl(array) :
        return "Crawl"
    if isJump(array) :
        return "Jump"
    if isRun(array) :
        return "Run"
    return "still"


mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
size = 10
array = np.zeros((size, 33, 3))
cap = cv2.VideoCapture('track_runner.mp4')
arrayIndex = 0
pTime = 0
while True:
    success, img = cap.read()

    if not success:
        break
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    # print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            array[arrayIndex, id] = [cx, cy, lm.z]

    action = classifyAction(array)
    cv2.putText(img, action, (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
    arrayIndex = (arrayIndex+1) % size

cv2.destroyAllWindows()

# Release the video capture object
cap.release()
