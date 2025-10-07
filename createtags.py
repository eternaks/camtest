import cv2
import numpy as np

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
marker_id = 23 # arbitrary?
marker_size = 75 # 2 x 2 cm

marker_image = np.zeros((marker_size, marker_size), dtype=np.uint8)

marker_image = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size, marker_image, 1)

cv2.imwrite(f"aruco_marker_id_{marker_id}.png", marker_image)