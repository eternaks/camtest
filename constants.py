import cv2

# constants used across files

# ------------------------------
# ENTER YOUR PARAMETERS HERE:
ARUCO_DICT = cv2.aruco.DICT_4X4_50
SQUARES_VERTICALLY = 7
SQUARES_HORIZONTALLY = 5
SQUARE_LENGTH = 0.032998833333
MARKER_LENGTH = 0.01699974375
LENGTH_M = 0.26643541667   # total length of the page in pixels
MARGIN_M = 0.079375    # size of the margin in pixels
SAVE_NAME = 'ChArUco_Marker1.png'

DEFAULT_CAM_GAIN = 0
DEFAULT_CAM_EXPOSURE = 156
DEFAULT_CAM_BRIGHTNESS = 0
# ------------------------------