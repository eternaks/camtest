import cv2
from cv2 import aruco
import numpy as np
import datetime
import os

# Define the number of pictures to take
counter = 0
# Define the directory to save the pictures (create it if it doesn't exist)
image_folder_name = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
save_directory = "./calibration_images" + "/" + image_folder_name

try:
    os.mkdir(save_directory)
    print(f"Directory '{save_directory}' created successfully")
except FileExistsError:
    print(f"Directory '{save_directory}' already exists.")
except Exception as e:
    print(f"An error occurred: {e}")

# Initialize the camera (0 for default webcam)
# If you have multiple cameras, you might need to try other indices (e.g., 1, 2)
cap = cv2.VideoCapture(0)
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
param_markers = aruco.DetectorParameters()


# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

while cap.isOpened():

    success, img = cap.read()
    visual_img = img.copy()

    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )

    if marker_corners:
        for ids, corners in zip(marker_IDs, marker_corners):
            cv2.polylines(
                visual_img, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv2.LINE_AA
            )
            corners = corners.reshape(4, 2)
            corners = corners.astype(int)
            top_right = corners[0].ravel()
            top_left = corners[1].ravel()
            bottom_right = corners[2].ravel()
            bottom_left = corners[3].ravel()
            cv2.putText(
                visual_img,
                f"id: {ids[0]}",
                top_right,
                cv2.FONT_HERSHEY_PLAIN,
                1.3,
                (200, 100, 0),
                2,
                cv2.LINE_AA,
            )

    k = cv2.waitKey(5)

    if k == 27:
        break
    elif k == ord('s'):
        cv2.imwrite(save_directory + "/img" + str(counter) + '.png', img)
        print("image saved!")
        counter += 1

    cv2.imshow('Img', visual_img)

cap.release()

cv2.destroyAllWindows()