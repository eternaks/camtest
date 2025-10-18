import cv2
import os
import constants


def main():
    # 4 is usb camera
    cap = cv2.VideoCapture(4)

    current_exposure = int(cap.get(cv2.CAP_PROP_EXPOSURE))
    current_brightness = int(cap.get(cv2.CAP_PROP_BRIGHTNESS))
    current_gain = int(cap.get(cv2.CAP_PROP_GAIN))
    autoexposure = cap.get(cv2.CAP_PROP_AUTO_EXPOSURE)

    cap.set(cv2.CAP_PROP_EXPOSURE, constants.DEFAULT_CAM_EXPOSURE)
    print("autoexposure", autoexposure)

    print("brightness", current_brightness)
    print("exposure", current_exposure)
    print("gain", current_gain)

    save_directory = "/home/calvin/projects/camtest/calibration_images"

    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

    aruco_params = cv2.aruco.DetectorParameters()

    i = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("cannot read")
            break
        # detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)
        # corners, ids, rejected = detector.detectMarkers(frame)
        
        # if ids is not None:
        #     cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        #     print("detected!")

        cv2.imshow('Cam feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # toggle auto exposure
        if cv2.waitKey(1) & 0xFF == ord('m'):
            if(autoexposure == 1):
                autoexposure = 3
            else:
                autoexposure = 1
            toggleAutoExposure(cap, autoexposure)
    
        # increase exposure
        if cv2.waitKey(1) & 0xFF == ord('z'):
            current_exposure += 10
            setExposure(cap, current_exposure)
        
        # decrease exposure
        if cv2.waitKey(1) & 0xFF == ord('x'):
            current_exposure -= 10
            setExposure(cap, current_exposure)
            
        # increase brightness
        if cv2.waitKey(1) & 0xFF == ord('v'):
            current_brightness += 10
            setBrightness(cap, current_brightness)
        
        # decrease brightness
        if cv2.waitKey(1) & 0xFF == ord('b'):
            current_brightness -= 10
            setBrightness(cap, current_brightness)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            filename = os.path.join(save_directory, f"picture_{i+1}.jpg")
            cv2.imwrite(filename, frame)
            i+=1
            print(f"Saved {filename}")

# brightness, exposure, gain, autoexposure (toggle)

def setExposure(cap, exposure):
    cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
    print("new exposure", exposure)

def setBrightness(cap, brightness):
    cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
    print("new brightness", brightness)

def toggleAutoExposure(cap, autoexposure):
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, autoexposure)
    print("autoexposure value", autoexposure)
    return autoexposure


if __name__ == "__main__":
    main()