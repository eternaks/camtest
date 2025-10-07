import cv2
import os

# 4 is usb camera
cap = cv2.VideoCapture(4)
save_directory = "/home/calvin/projects/camtest/calibration_images" 

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

aruco_params = cv2.aruco.DetectorParameters()

i = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("cannot read")
        break
    # detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)
    # corners, ids, rejected = detector.detectMarkers(frame)
    
    # if ids is not None:
    #     cv2.aruco.drawDetectedMarkers(frame, corners, ids)
    #     print("detected!")

    cv2.imshow('Cam feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cv2.waitKey(1) & 0xFF == ord('c'):
        filename = os.path.join(save_directory, f"picture_{i+1}.jpg")
        cv2.imwrite(filename, frame)
        i+=1
        print(f"Saved {filename}")