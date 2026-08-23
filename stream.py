import serial
import cv2
import numpy as np
from time import sleep
from enum import Enum
from enum import IntEnum

START_BYTE = 0x5A
UART_PORT = "/dev/ttyS5"
BAUDRATE = 115200


class commands(IntEnum):
    MOVE = 0x1


markers_id = [1, 2, 3]


def send_command(command, serial):
    packet = bytes([90, command])  # START  # example CRC

    serial.write(packet)


def process_id(id, ser):
    match id:
        case 1:
            print("MOVE")
            send_command(commands.MOVE, ser)


def open_serial():

    print(f"Opening UART5: {port}")

    ser = serial.Serial(
        port=UART_PORT,
        baudrate=BAUDRATE,
        # 8N1
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        # Prevent reads/writes from blocking forever
        timeout=0.5,
        write_timeout=0.5,
        # UART5 pins only provide TX/RX,
        # so disable all flow control.
        xonxoff=False,
        rtscts=False,
        dsrdtr=False,
    )
    return ser

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)
# detection
temp = open_serial()
t = cv2.VideoCapture("/dev/video1")
while True:
    ret, frame = t.read()

    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        corners, ids, rejected = detector.detectMarkers(gray)
        if ids is not None:
            process_id(ids, temp)
    else:
        print("Error")
        break


t.release()
