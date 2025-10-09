import json
import cv2
import numpy as np

json_file_path = './calibration.json'

# ------------------------------
# ENTER YOUR PARAMETERS HERE:
ARUCO_DICT = cv2.aruco.DICT_4X4_50
SQUARES_VERTICALLY = 7
SQUARES_HORIZONTALLY = 5
SQUARE_LENGTH = 124.72
MARKER_LENGTH = 64.251
LENGTH_PX = 1007   # total length of the page in pixels
MARGIN_PX = 30    # size of the margin in pixels
SAVE_NAME = 'ChArUco_Marker1.png'
# ------------------------------

with open(json_file_path, 'r') as file: # Read the JSON file
    json_data = json.load(file)

mtx = np.array(json_data['mtx'])
dst = np.array(json_data['dist'])

dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
board = cv2.aruco.CharucoBoard((SQUARES_VERTICALLY, SQUARES_HORIZONTALLY), SQUARE_LENGTH, MARKER_LENGTH, dictionary)
params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, params)

cap = cv2.VideoCapture(4)

while True:
    ret, frame = cap.read()
    if not ret:
        print("cannot read")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect markers
    corners, ids, rejected = detector.detectMarkers(gray)

    if ids is not None:
        # Estimate pose of each marker
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners, MARKER_LENGTH, mtx, dst
        )

        for i in range(len(ids)):
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            cv2.drawFrameAxes(frame, mtx, dst, rvecs[i], tvecs[i], MARKER_LENGTH * 0.5)

            # Print pose data
            print(f"Marker ID {ids[i][0]}:")
            print(f"  Rotation Vector (rvec): {rvecs[i].ravel()}")
            print(f"  Translation Vector (tvec): {tvecs[i].ravel()}")
            print("-" * 30)

    else:
        cv2.putText(frame, "No markers detected", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Pose Estimation", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()

    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # h,  w = image.shape[:2]
    # newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dst, (w,h), 1, (w,h))
    # image = cv2.undistort(image, mtx, dst, None, newcameramtx)

    # all_charuco_ids = []
    # all_charuco_corners = []


    # if marker_ids is not None and len(marker_ids) > 0: # If at least one marker is detected
    #     image = cv2.aruco.drawDetectedMarkers(image, marker_corners, marker_ids)
    #     ret, charucoCorners, charucoIds = cv2.aruco.interpolateCornersCharuco(marker_corners, marker_ids, image, board)
    #     if charucoCorners is not None and charucoIds is not None and len(charucoCorners) > 3:
    #         all_charuco_corners.append(charucoCorners)
    #         all_charuco_ids.append(charucoIds)

    #     retval, rvec, tvec = cv2.aruco.estimatePoseCharucoBoard(np.array(all_charuco_corners)[0], np.array(all_charuco_ids)[0], board, np.array(mtx), np.array(dst), np.empty(1), np.empty(1))

    #     Zx, Zy, Zz = tvec[0][0], tvec[1][0], tvec[2][0]
    #     fx, fy = mtx[0][0], mtx[1][1]

    #     print(f'Zz = {Zz}\nfx = {fx}')
        
    # cv2.imshow("feed", image)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
