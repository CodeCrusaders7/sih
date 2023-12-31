import cv2
import mediapipe as mp
import time
import numpy as np

def isCrawl(array) :
    return True
def isRun(array) :
    return True
def classifyAction(array, mini) :
    if isCrawl(array) :
        return "Crawl"

    if isRun(array) :
        return "Run"
    return "still"

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
size = 10
array = np.zeros((size, 33, 3))
cap = cv2.VideoCapture(0)
arrayIndex = 0
pTime = 0
miniY = 0
shoulderLevel = 0
t = 1
jumpThreshold = 7
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
            array[arrayIndex, id] = [cx, cy, lm.z*w]

        t = t + 1

    if 2 == t:
        shoulderLevel = (array[arrayIndex, 11, 1] + array[arrayIndex, 12, 1]) / 2
        t = t + 1
        action = "start"

    if -(array[arrayIndex, 12, 1] + array[arrayIndex, 11, 1]) / 2 + shoulderLevel > jumpThreshold:
        action = "Jumping"
        shoulderLevel = (array[arrayIndex, 11, 1] + array[arrayIndex, 12, 1]) / 2

    elif shoulderLevel - jumpThreshold < (
            array[arrayIndex, 11, 1] + array[arrayIndex, 12, 1]) / 2 < shoulderLevel + jumpThreshold:
        # print((array[arrayIndex, 12, 1] + array[arrayIndex, 11, 1]) / 2 - shoulderLevel)
        shoulderLevel = (array[arrayIndex, 11, 1] + array[arrayIndex, 12, 1]) / 2
        action = "Walking"

    else:
        shoulderLevel = (array[arrayIndex, 11, 1] + array[arrayIndex, 12, 1]) / 2
        action = "Walkkuhuuhing"
    pixel = array[arrayIndex, 24, 1] + array[arrayIndex, 23, 1] - array[arrayIndex, 12, 1] - array[arrayIndex, 11, 1]
    pixel = pixel / 2
    print(340.73 * 95 / pixel)

    # Jumping logic : keep track of minimum shoulder level (y coordinate) then if current shoulder level is more than
    # min shoulder level by jumpThreshold the assign action to jumping

    # else:
    #     action = classifyAction(array, miniY)

    #print(array[arrayIndex, 23, 2])

    cv2.putText(img, action, (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    #cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                #(255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
    arrayIndex = (arrayIndex+1) % size


cv2.destroyAllWindows()

# Release the video capture object
cap.release()
