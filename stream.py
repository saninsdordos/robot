import cv2
import numpy as np
from time import sleep

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

t = cv2.VideoCapture("/dev/video1")
while True:
    ret, frame = t.read()

    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        corners, ids, rejected = detector.detectMarkers(gray)

        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
    if ids is not None:
        print(ids)
    else:
        print("Error")
        break

    if cv2.waitKey(25) == ord("q"):
        break

sleep(0.1)
t.release()
cv2.destroyAllWindows()
