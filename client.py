import socket
import cv2
import numpy as np
import mss
import ctypes
from ctypes import wintypes

# Function to move the mouse
def move_mouse(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)

# Function to perform a mouse click
def click_mouse(left=True):
    if left:
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # Left click down
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # Left click up
    else:
        ctypes.windll.user32.mouse_event(8, 0, 0, 0, 0)  # Right click down
        ctypes.windll.user32.mouse_event(16, 0, 0, 0, 0)  # Right click up

import ctypes
from ctypes import wintypes

# Define necessary structures for SendInput
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR)]

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [("ki", KEYBDINPUT)]
    _anonymous_ = ("_input",)
    _fields_ = [("type", wintypes.DWORD), ("_input", _INPUT)]

# Constants for input type
INPUT_KEYBOARD = 1

# Function to simulate a key press
def PressKey(hexKeyCode):
    input_struct = INPUT(type=INPUT_KEYBOARD,
                         ki=KEYBDINPUT(wVk=hexKeyCode,
                                       dwFlags=0))
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_struct), ctypes.sizeof(input_struct))

# Function to simulate a key release
def ReleaseKey(hexKeyCode):
    input_struct = INPUT(type=INPUT_KEYBOARD,
                         ki=KEYBDINPUT(wVk=hexKeyCode,
                                       dwFlags=2))  # KEYEVENTF_KEYUP = 0x0002
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_struct), ctypes.sizeof(input_struct))



# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('SERVER_IP_ADDRESS', PORT_NUMBER))  # Replace with server IP and port

with mss.mss() as sct:
    monitor = sct.monitors[1]

    while True:
        # Capture the screen
        img = np.array(sct.grab(monitor))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # Compress the image
        ret, buffer = cv2.imencode('.jpg', img)

        # Send the size of the buffer
        client_socket.sendall(len(buffer).to_bytes(4, byteorder='big'))

        # Send the buffer
        client_socket.sendall(buffer)

        # Non-blocking receive for commands
        try:
            client_socket.settimeout(0.01)
            command = client_socket.recv(1024).decode()
            if command:
                action = command.split(',')

                # Mouse command processing
                if action[0] == 'mouse':
                    if action[1] == 'move':
                        x, y = int(action[2]), int(action[3])
                        move_mouse(x, y)
                    elif action[1] == 'click':
                        left_click = action[2] == 'left'
                        click_mouse(left_click)

                # Keyboard command processing
                elif action[0] == 'keyboard':
                    if action[1] == 'press':
                        keycode = int(action[2], 16)  # Convert hex string to integer
                        PressKey(keycode)
                    elif action[1] == 'release':
                        keycode = int(action[2], 16)  # Convert hex string to integer
                        ReleaseKey(keycode)

        except socket.timeout:
            continue
