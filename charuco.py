import os
import numpy as np
import cv2
import constants
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

def create_and_save_new_board():
    dictionary = cv2.aruco.getPredefinedDictionary(constants.ARUCO_DICT)
    board = cv2.aruco.CharucoBoard((constants.SQUARES_VERTICALLY, constants.SQUARES_HORIZONTALLY), constants.SQUARE_LENGTH, constants.MARKER_LENGTH, dictionary)
    size_ratio = constants.SQUARES_HORIZONTALLY / constants.SQUARES_VERTICALLY
    img = cv2.aruco.CharucoBoard.generateImage(board, (constants.LENGTH_M, int(constants.LENGTH_M*size_ratio)), marginSize=constants.MARGIN_M)
    cv2.imshow("img", img)
    cv2.waitKey(2000)
    cv2.imwrite(constants.SAVE_NAME, img)

create_and_save_new_board()