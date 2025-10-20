import os
import cv2
import numpy as np
import json
import constants

# ARUCO_DICT = cv2.aruco.DICT_4X4_50
# SQUARES_VERTICALLY = 7
# SQUARES_HORIZONTALLY = 5
# SQUARE_LENGTH = 124.72
# MARKER_LENGTH = 64.251
# LENGTH_PX = 1007   # total length of the page in pixels
# MARGIN_PX = 30    # size of the margin in pixels
# ...
PATH_TO_YOUR_IMAGES = 'calibration_images/2025-10-16 19:42:33'
# ------------------------------

def get_calibration_parameters(img_dir):
    # Define the aruco dictionary, charuco board and detector
    dictionary = cv2.aruco.getPredefinedDictionary(constants.ARUCO_DICT)
    board = cv2.aruco.CharucoBoard((constants.SQUARES_VERTICALLY, constants.SQUARES_HORIZONTALLY), constants.SQUARE_LENGTH, constants.MARKER_LENGTH, dictionary)
    params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, params)
    
    # Load images from directory
    image_files = [os.path.join(img_dir, f) for f in os.listdir(img_dir) if f.endswith(".png")]
    all_charuco_ids = []
    all_charuco_corners = []

    # Loop over images and extraction of corners
    for image_file in image_files:
        image = cv2.imread(image_file)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        imgSize = image.shape
        image_copy = image.copy()
        marker_corners, marker_ids, rejectedCandidates = detector.detectMarkers(image)
        
        if len(marker_ids) > 0: # If at least one marker is detected
            # cv2.aruco.drawDetectedMarkers(image_copy, marker_corners, marker_ids)
            ret, charucoCorners, charucoIds = cv2.aruco.interpolateCornersCharuco(marker_corners, marker_ids, image, board)

            if charucoIds is not None and len(charucoCorners) > 3:
                all_charuco_corners.append(charucoCorners)
                all_charuco_ids.append(charucoIds)

    # Calibrate camera with extracted information
    result, mtx, dist, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(all_charuco_corners, all_charuco_ids, board, (640, 480), None, None)
    return mtx, dist

SENSOR = 'monochrome'
LENS = 'usbcam'
FOLDER_NAME = './calibration_images/' + input('Enter calibration image folder name: ')
OUTPUT_JSON = 'Calibration of' + FOLDER_NAME

mtx, dist = get_calibration_parameters(img_dir=FOLDER_NAME)
data = {"sensor": SENSOR, "lens": LENS, "mtx": mtx.tolist(), "dist": dist.tolist()}

with open(OUTPUT_JSON, 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(f'Data has been saved to {OUTPUT_JSON}')