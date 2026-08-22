import serial
import cv2
import numpy as np
from time import sleep
from enum import Enum


class commands(Enum):
    MOVE = 0x1


markers_id = [1, 2, 3]


def send_command(command):
    packet = bytes([ST, command])  # START  # example CRC

    ser.write(packet)


def process_id(id):
    match id:
        case 1:
            print("MOVE")
            send_command(MOVE)


def detect_object(id):
    if id in markers_id:
        send_command()


aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)
# detection
t = cv2.VideoCapture("/dev/video1/")
while True:
    ret, frame = t.read()

    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        corners, ids, rejected = detector.detectMarkers(gray)
        if ids is not None:
            process_id(ids)
    else:
        print("Error")
        break


t.release()
