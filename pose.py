import json
import cv2
import numpy as np
import constants
import datetime

json_file_path = './calibration_images/2025-10-26_13-42-03/2025-10-26_13-42-03_calibration_constants.json'

# ------------------------------
# ENTER YOUR PARAMETERS HERE:
# ARUCO_DICT = cv2.aruco.DICT_4X4_50
# SQUARES_VERTICALLY = 7
# SQUARES_HORIZONTALLY = 5
# SQUARE_LENGTH = 124.72
# MARKER_LENGTH = 64.251
# LENGTH_PX = 1007   # total length of the page in pixels
# MARGIN_PX = 30    # size of the margin in pixels
# SAVE_NAME = 'ChArUco_Marker1.png'
# ------------------------------

measure_distance = input("Z distance from camera (cm): ")

with open(json_file_path, 'r') as file: # Read the JSON file
    json_data = json.load(file)

mtx = np.array(json_data['mtx'])
dst = np.array(json_data['dist'])

dictionary = cv2.aruco.getPredefinedDictionary(constants.ARUCO_DICT)
board = cv2.aruco.CharucoBoard((constants.SQUARES_VERTICALLY, constants.SQUARES_HORIZONTALLY), constants.SQUARE_LENGTH, constants.MARKER_LENGTH, dictionary)
params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, params)

cap = cv2.VideoCapture(4)


x_vals = []
y_vals = []
z_vals = []
roll_vals = []
pitch_vals = []
yaw_vals = []

cntr = 1000
start_measuring = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("cannot read")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect markers
    corners, ids, rejected = detector.detectMarkers(gray)

    k = cv2.waitKey(5)
    if k == ord('f'):
        start_measuring = True
        print("measuring starting")

    if ids is not None:
        # Estimate pose of each marker
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners, constants.MARKER_LENGTH, mtx, dst
        )

        for i in range(len(ids)):
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            cv2.drawFrameAxes(frame, mtx, dst, rvecs[i], tvecs[i], constants.MARKER_LENGTH * 0.5)

            # Print pose data
            # print(f"Marker ID {ids[i][0]}:")
            # print(f"  Rotation Vector (rvec): {rvecs[i].ravel()}")

            # --- Convert rvec to roll, pitch, yaw ---
            rotation_matrix, _ = cv2.Rodrigues(rvecs[i])

            sy = np.sqrt(rotation_matrix[0, 0] ** 2 + rotation_matrix[1, 0] ** 2)
            singular = sy < 1e-6

            if not singular:
                x = np.arctan2(rotation_matrix[2, 1], rotation_matrix[2, 2])  # roll
                y = np.arctan2(-rotation_matrix[2, 0], sy)                    # pitch
                z = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0])  # yaw
            else:
                x = np.arctan2(-rotation_matrix[1, 2], rotation_matrix[1, 1])
                y = np.arctan2(-rotation_matrix[2, 0], sy)
                z = 0

            roll = np.degrees(x)
            pitch = np.degrees(y)
            yaw = np.degrees(z)

            print(f"  Roll: {roll:.2f}°, Pitch: {pitch:.2f}°, Yaw: {yaw:.2f}°")
            # print(f"  Translation Vector (tvec): {tvecs[i].ravel()}")

            if start_measuring:
                roll_vals.append(roll)
                pitch_vals.append(pitch)
                yaw_vals.append(yaw)
                x,y,z = tvecs[i].ravel()
                x_vals.append(x)
                y_vals.append(y)
                z_vals.append(z)
                cntr-=1
                print("value captured!", cntr)
                

            # print("Top left corner", corners[0])
            # print("Bottom right corner", corners[2])
            # print("-" * 30)

    else:
        cv2.putText(frame, "No markers detected", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Get image dimensions
    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2

    # Draw horizontal line
    cv2.line(frame, (center_x - 20, center_y), (center_x + 20, center_y), (0, 255, 0), 1)
    # Draw vertical line
    cv2.line(frame, (center_x, center_y - 20), (center_x, center_y + 20), (0, 255, 0), 1)

    cv2.imshow("Pose Estimation", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break
    if cntr == 0:
        break

output = {
    "x": x_vals,
    "y": y_vals,
    "z": z_vals,
    "roll": roll_vals,
    "pitch": pitch_vals,
    "yaw": yaw_vals
}

time_stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

with open("./plot_data/" + time_stamp + "_" + "(" + measure_distance + "cm).json", "w") as f:
    json.dump(output, f, indent=4)

cap.release()
cv2.destroyAllWindows()