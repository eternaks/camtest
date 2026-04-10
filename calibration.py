import os
import cv2
import numpy as np
import json
import constants

# Constants setup from your file
PATH_TO_YOUR_IMAGES = 'calibration_images/wide_angle' # Updated folder name suggestion
subpix_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# ------------------------------

def get_calibration_parameters(img_dir):
    # Define the aruco dictionary, charuco board and detector
    dictionary = cv2.aruco.getPredefinedDictionary(constants.ARUCO_DICT)
    board = cv2.aruco.CharucoBoard((constants.SQUARES_VERTICALLY, constants.SQUARES_HORIZONTALLY), 
                                   constants.SQUARE_LENGTH, constants.MARKER_LENGTH, dictionary)
    params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, params)
    
    # Robust file searching (handles uppercase/lowercase and multiple formats)
    valid_extensions = ('.png', '.jpg', '.jpeg')
    image_files = [os.path.join(img_dir, f) for f in os.listdir(img_dir) if f.lower().endswith(valid_extensions)]
    
    if not image_files:
        print(f"Error: No images found in '{img_dir}'.")
        exit(1)
        
    print(f"Found {len(image_files)} images. Starting detection...")
    
    all_charuco_ids = []
    all_charuco_corners = []
    img_shape = None

    # Loop over images and extraction of corners
    for image_file in image_files:
        image = cv2.imread(image_file)
        if image is None:
            print(f"Warning: Could not read {image_file}. Skipping.")
            continue
            
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Dynamically grab the resolution for the current camera (Width, Height)
        if img_shape is None:
            img_shape = (gray.shape[1], gray.shape[0]) 

        marker_corners, marker_ids, rejectedCandidates = detector.detectMarkers(gray)
        
        # Safely check for None types
        if marker_ids is not None and len(marker_ids) > 0: 
            ret, charucoCorners, charucoIds = cv2.aruco.interpolateCornersCharuco(marker_corners, marker_ids, gray, board)

            # Filter out "poison pill" frames by demanding at least 12 corners
            if charucoIds is not None and charucoCorners is not None and len(charucoCorners) >= 12:
                # subpixel refinement again on charuco corners
                cv2.cornerSubPix(gray, charucoCorners, winSize=(5,5), zeroZone=(-1, -1), criteria=subpix_criteria)

                all_charuco_corners.append(charucoCorners)
                all_charuco_ids.append(charucoIds)

    if not all_charuco_corners:
        print("Error: No valid ChArUco corners were detected in any of the images. Check your constants.")
        exit(1)

    print(f"Successfully extracted robust corners from {len(all_charuco_corners)} / {len(image_files)} images.")
    print("Calibrating using standard PINHOLE mathematical model...")

    # Revert to standard pinhole calibration (outputs the 5-parameter distortion array)
    rms, mtx, dist, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(
        all_charuco_corners, 
        all_charuco_ids, 
        board, 
        img_shape, 
        None, 
        None
    )
    
    print(f"Calibration successful! RMS Reprojection Error: {rms:.4f}")
    return mtx, dist

# --- Main Script Execution ---
if __name__ == '__main__':
    SENSOR = 'monochrome'
    LENS = 'standard' # Updated from 'fisheye' to reflect reality
    user_input = input('Enter calibration image folder name: ').strip()
    FOLDER_NAME = os.path.join('./calibration_images', user_input)

    if not os.path.isdir(FOLDER_NAME):
        print(f"Error: Folder '{FOLDER_NAME}' does not exist.")
        exit(1)

    mtx, dist = get_calibration_parameters(img_dir=FOLDER_NAME)
    
    data = {
        "sensor": SENSOR, 
        "lens": LENS, 
        "mtx": mtx.tolist(), 
        "dist": dist.tolist()
    }

    filename = f'{user_input}_calibration_constants.json'
    output_path = os.path.join(FOLDER_NAME, filename)
        
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f'Data has been saved to: {output_path}')