import cv2
import mediapipe as mp
import numpy as np
import os

# Initialize Mediapipe Pose
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
landmark_list = []  # Use a list to store landmark values
fileIndex = 0
subFolderIndex = 0
flag = 0
folder_path = "Trainingdata/Running"
folder_name = str(subFolderIndex)  # Initialize folder_name

while True:
    success, img = cap.read()

    if not success:
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        landmark_values = []  # Store landmark values for this frame
        for lm in results.pose_landmarks.landmark:
            landmark_values.extend([lm.x, lm.y, lm.z])
        landmark_list.append(landmark_values)

    if flag == 1:
        # Save the list of landmark values as a numpy array
        array = np.array(landmark_list)
        file_name = f"{folder_path}/{folder_name}/{fileIndex}.npy"
        np.save(file_name, array)
        fileIndex += 1

    cv2.imshow("LOL", img)
    key = cv2.waitKey(1)

    if key == ord("k"):
        flag = 1
        fileIndex = 0
        subFolderIndex += 1
        folder_name = str(subFolderIndex)  # Update folder_name
        folder_path = "Trainingdata/Walking"  # Update folder_path
        if not os.path.exists(os.path.join(folder_path, folder_name)):
            os.makedirs(os.path.join(folder_path, folder_name))

    if key == ord("l"):
        flag = 0

    if key == ord("q"):
        break

cv2.destroyAllWindows()
cap.release()
