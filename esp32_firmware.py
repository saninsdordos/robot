from machine import UART
from machine import Pin, PWM

pwm = PWM(Pin(15), freq=50)

uart0 = UART(1, baudrate=115200, tx=8, rx=3)

def parsing_message():
    received_message = []
    while True:
        if uart0.any():
            message_byte = uart0.read(1)
        if message_byte == b"*":
            received_message = b""
            continue
        if message_byte == b"!":
            break

        received_message += message_byte
        print(received_message)
  if b"START" in received_message:
    pwm.duty_ns(1500000)  # 1.5 ms pulse
return true     



def move() 
  

