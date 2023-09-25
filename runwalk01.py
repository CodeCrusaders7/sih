
import cv2
import mediapipe as mp
import numpy as np
import os

# Initialize Mediapipe Pose
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture("jj")
 # Use a list to store landmark values
fileIndex = 0
subFolderIndex = 0
flag = 0
folder_path = "Trainingdata/Jumping"
folder_name = str(subFolderIndex)  # Initialize folder_name
position = (50, 50)  # (x, y) coordinates
flag2 = 0
# Define the font and other text properties
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_color = (255, 0, 0)  # BGR color (Blue, Green, Red)
font_thickness = 2
while True:
    success, img = cap.read()

    if not success:
        break
    landmark_list = []
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        landmark_values = []  # Store landmark values for this frame
        for lm in results.pose_landmarks.landmark:
            #landmark_values.extend([lm.x, lm.y, lm.z])
            #improved
            landmark_values.extend([lm.x, lm.y, lm.z, lm.visibility])
        landmark_list.append(landmark_values)
        flag1 = 1
    else :
        flag1 = 0
    # array = np.array(landmark_list).flatten()
    if flag1 == 1 and flag2 == 1:
        # Save the list of landmark values as a numpy array
        array = np.array(landmark_list).flatten()
        file_name = f"{folder_path}/{folder_name}/{fileIndex}.npy"
        array = array.flatten()
        np.save(file_name, array)
        fileIndex += 1
        if fileIndex == 30:
            fileIndex = 0
            subFolderIndex = subFolderIndex + 1
            folder_name = str(subFolderIndex)  # Update folder_name
            folder_path = "Trainingdata/Jumping"  # Update folder_path
            if not os.path.exists(os.path.join(folder_path, folder_name)):
                os.makedirs(os.path.join(folder_path, folder_name))
            print(subFolderIndex)

    cv2.putText(img, str(subFolderIndex), position, font, font_scale, font_color, font_thickness)
    cv2.imshow("LOL", img)
    key = cv2.waitKey(1)

    if key == ord("k"):
        flag2 = 1
        fileIndex = 0
        folder_name = str(subFolderIndex)  # Update folder_name
        folder_path = "Trainingdata/Jumping"  # Update folder_path
        if not os.path.exists(os.path.join(folder_path, folder_name)):
            os.makedirs(os.path.join(folder_path, folder_name))
        print(subFolderIndex)
  #  else:
   # 	flag2 = 0 

    #if key == ord("m"):
     #   flag = 0

    if key == ord("q"):
        break

cv2.destroyAllWindows()
cap.release()
# print(array.shape)
