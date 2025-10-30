import json
import cv2
import numpy as np
import constants
from collections import deque
import datetime

measure_distance = input("Z distance from camera (cm): ")
json_file_path = './calibration_images/2025-10-21_19-28-33/2025-10-21_19-28-33_calibration_constants.json'

with open(json_file_path, 'r') as file:
    json_data = json.load(file)

mtx = np.array(json_data['mtx'])
dst = np.array(json_data['dist'])

dictionary = cv2.aruco.getPredefinedDictionary(constants.ARUCO_DICT)
board = cv2.aruco.CharucoBoard(
    (constants.SQUARES_VERTICALLY, constants.SQUARES_HORIZONTALLY),
    constants.SQUARE_LENGTH,
    constants.MARKER_LENGTH,
    dictionary
)
params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, params)

cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

x_vals, y_vals, z_vals = [], [], []
roll_vals, pitch_vals, yaw_vals = [], [], []

cntr = 1000
start_measuring = False

### --- KALMAN FILTER SECTION --- ###
kf = cv2.KalmanFilter(6, 3)  # 6 states (x, y, z, dx, dy, dz), 3 measurements (x, y, z)
dt = 1.0  # time step (can be tuned)

kf.transitionMatrix = np.array([
    [1, 0, 0, dt, 0, 0],
    [0, 1, 0, 0, dt, 0],
    [0, 0, 1, 0, 0, dt],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1]
], np.float32)

kf.measurementMatrix = np.array([
    [1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0]
], np.float32)
# change processNoiseCov and MeasurementNoiseCov to tune filter
kf.processNoiseCov = np.eye(6, dtype=np.float32) * 1e-6
kf.measurementNoiseCov = np.eye(3, dtype=np.float32) * 1e-2
kf.statePost = np.zeros((6, 1), np.float32)
### --- END KALMAN FILTER SECTION --- ###

### --- VISUALIZATION TRAILS --- ###
# Deques (fixed-length lists) to store recent positions
raw_trail = deque(maxlen=50)
filtered_trail = deque(maxlen=50)
### --- END VISUALIZATION TRAILS --- ###


while True:
    ret, frame = cap.read()
    if not ret:
        print("cannot read")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = detector.detectMarkers(gray)

    k = cv2.waitKey(5)
    if k == ord('f'):
        start_measuring = True
        print("measuring starting")

    if ids is not None:
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners, constants.MARKER_LENGTH, mtx, dst
        )

        for i in range(len(ids)):
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            cv2.drawFrameAxes(frame, mtx, dst, rvecs[i], tvecs[i], constants.MARKER_LENGTH * 0.5)

            # --- Convert rvec to roll, pitch, yaw ---
            rotation_matrix, _ = cv2.Rodrigues(rvecs[i])
            sy = np.sqrt(rotation_matrix[0, 0] ** 2 + rotation_matrix[1, 0] ** 2)
            singular = sy < 1e-6

            if not singular:
                x_angle = np.arctan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
                y_angle = np.arctan2(-rotation_matrix[2, 0], sy)
                z_angle = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
            else:
                x_angle = np.arctan2(-rotation_matrix[1, 2], rotation_matrix[1, 1])
                y_angle = np.arctan2(-rotation_matrix[2, 0], sy)
                z_angle = 0

            # --- Convert to degrees ---
            roll = np.degrees(x_angle)
            pitch = np.degrees(y_angle)
            yaw = np.degrees(z_angle)

            # --- Convert to 0–360° for roll/yaw to avoid wraparound ---
            roll = (roll + 360) % 360
            yaw = (yaw + 360) % 360
            # Keep pitch as -90 to +90 for clarity

            # --- Smooth unwrapping (frame-to-frame continuity) ---
            if roll_vals:
                prev_roll = roll_vals[-1]
                prev_yaw = yaw_vals[-1]

                # Handle roll wraparound
                if roll - prev_roll > 180:
                    roll -= 360
                elif roll - prev_roll < -180:
                    roll += 360

                # Handle yaw wraparound
                if yaw - prev_yaw > 180:
                    yaw -= 360
                elif yaw - prev_yaw < -180:
                    yaw += 360

            # --- Get raw translation ---
            x, y, z = tvecs[i].ravel()

            ### --- APPLY KALMAN FILTER --- ###
            measurement = np.array([[np.float32(x)], [np.float32(y)], [np.float32(z)]])
            kf.predict()
            estimated = kf.correct(measurement)
            x_f, y_f, z_f = float(estimated[0]), float(estimated[1]), float(estimated[2])
            ### --- END KALMAN FILTER --- ###

            if start_measuring:
                x_vals.append(x_f)
                y_vals.append(y_f)
                z_vals.append(z_f)
                roll_vals.append(roll)
                pitch_vals.append(pitch)
                yaw_vals.append(yaw)
                cntr -= 1
                print(f"value captured! Remaining: {cntr}")


            ### --- VISUALIZATION UPDATE --- ###
            # Map 3D coordinates to 2D visualization (x, y)
            # You can adjust scaling to make movement visible
            scale = 400  # pixels per meter
            raw_px = int(50 + x * scale)
            raw_py = int(300 - y * scale)
            filt_px = int(50 + x_f * scale)
            filt_py = int(300 - y_f * scale)

            raw_trail.append((raw_px, raw_py))
            filtered_trail.append((filt_px, filt_py))
            ### --- END VISUALIZATION UPDATE --- ###

    else:
        cv2.putText(frame, "No markers detected", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # --- Draw center cross ---
    h, w = frame.shape[:2]
    cx, cy = w // 2, h // 2
    cv2.line(frame, (cx - 20, cy), (cx + 20, cy), (0, 255, 0), 1)
    cv2.line(frame, (cx, cy - 20), (cx, cy + 20), (0, 255, 0), 1)

    ### --- DRAW OVERLAY --- ###
    overlay = frame.copy()

    # Draw raw position trail (red)
    for pt in range(1, len(raw_trail)):
        cv2.line(overlay, raw_trail[pt - 1], raw_trail[pt], (0, 0, 255), 2)
    if raw_trail:
        cv2.circle(overlay, raw_trail[-1], 5, (0, 0, 255), -1)

    # Draw filtered position trail (green)
    for pt in range(1, len(filtered_trail)):
        cv2.line(overlay, filtered_trail[pt - 1], filtered_trail[pt], (0, 255, 0), 2)
    if filtered_trail:
        cv2.circle(overlay, filtered_trail[-1], 5, (0, 255, 0), -1)

    # Add legend
    cv2.rectangle(overlay, (20, 20), (270, 80), (0, 0, 0), -1)
    cv2.putText(overlay, "Red: Raw  |  Green: Kalman", (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    frame = cv2.addWeighted(overlay, 0.7, frame, 0.3, 0)
    ### --- END OVERLAY --- ###

    cv2.imshow("Pose Estimation (Kalman Filter vs Raw)", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break
    if cntr == 0:
        break

# --- Save smoothed data ---
output = {
    "x": x_vals,
    "y": y_vals,
    "z": z_vals,
    "roll": roll_vals,
    "pitch": pitch_vals,
    "yaw": yaw_vals
}

time_stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

with open("./plot_data/" + time_stamp + "_kalman_" + "(" + measure_distance + "cm).json", "w") as f:
    json.dump(output, f, indent=4)

cap.release()
cv2.destroyAllWindows()
