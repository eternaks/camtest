import cv2

# Initialize the camera (0 for default webcam)
# If you have multiple cameras, you might need to try other indices (e.g., 1, 2)
cap = cv2.VideoCapture(4)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Define the number of pictures to take
num = 17
# Define the directory to save the pictures (create it if it doesn't exist)
save_directory = "/home/calvin/projects/camtest/calibration_images" 

while cap.isOpened():

    success, img = cap.read()

    k = cv2.waitKey(5)

    if k == 27:
        break
    elif k == ord('s'):
        cv2.imwrite(save_directory + "/img" + str(num) + '.png', img)
        print("image saved!")
        num += 1

    cv2.imshow('Img', img)

cap.release()

cv2.destroyAllWindows()