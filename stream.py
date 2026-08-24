import serial
import cv2
import numpy as np
from time import sleep
from enum import Enum
from enum import IntEnum

UART_PORT = "/dev/ttyS5"
BAUDRATE = 115200

ser = serial.Serial()

command_move = "START"

markers_id = [1, 2, 3]


def send_message(command):
    packet = b"!" + command.encode() + b"*"
    ser.write(packet)
    ser.flush()

    print(f"TX: {packet.hex(' ')}")


def process_id(id, ser):
    match id:
        case 1:
            print("MOVE")
            send_message(command_move)


def open_port():

    ser.port = UART_PORT
    ser.baudrate = BAUDRATE
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE

    ser.timeout = 0.5
    ser.write_timeout = 0.5

    ser.xonxoff = False
    ser.rtscts = False
    ser.dsrdtr = False

    ser.open()

    print(f"Opened: {ser.name}")

    return ser


aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)
# detection
ser = open_port()
t = cv2.VideoCapture("/dev/video1")
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
