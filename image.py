import cv2

# Initialize the camera (0 for default webcam)
# If you have multiple cameras, you might need to try other indices (e.g., 1, 2)
cap = cv2.VideoCapture(4, cv2.CAP_V4L2)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Define the number of pictures to take
num_pictures = 10
# Define the directory to save the pictures (create it if it doesn't exist)
save_directory = "/home/calvin/projects/camtest/calibration_images" 

# Create the directory if it doesn't exist
import os
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

for i in range(num_pictures):
    # Read a frame from the camera
    ret, frame = cap.read()

    # Check if the frame was read successfully
    if not ret:
        print(f"Error: Failed to capture image {i+1}.")
        break

    # Construct the filename for the saved image
    filename = os.path.join(save_directory, f"picture_{i+1}.jpg")

    # Save the frame as an image
    cv2.imwrite(filename, frame)
    print(f"Saved {filename}")

    # Optional: Display the captured frame (for visual feedback)
    cv2.imshow("Capturing...", frame)
    
    # Wait for a short period (e.g., 500 milliseconds) before capturing the next image
    # This also allows you to press 'q' to quit early if the imshow window is active
    if cv2.waitKey(2000) & 0xFF == ord('q'):
        break

# Release the camera and destroy all OpenCV windows
cap.release()
cv2.destroyAllWindows()