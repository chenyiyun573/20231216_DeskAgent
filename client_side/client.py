import socket
import cv2
import numpy as np
import mss
import commands
from config import COMMAND_PORT, VIDEO_PORT, SERVER_IP_ADDRESS

# Connect to the server for commands
command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
command_socket.connect((SERVER_IP_ADDRESS, COMMAND_PORT))

# Connect to the server for video
video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_socket.connect((SERVER_IP_ADDRESS, VIDEO_PORT))


def process_command(command):
    action = command.split(',')

    # Mouse command processing
    if action[0] == 'mouse':
        if action[1] == 'move':
            x, y = int(action[2]), int(action[3])
            commands.move_mouse(x, y)
        elif action[1] == 'click':
            left_click = action[2] == 'left'
            commands.click_mouse(left_click)

    # Keyboard command processing
    elif action[0] == 'keyboard':
        if action[1] == 'press':
            keycode = int(action[2], 16)  # Convert hex string to integer
            commands.press_key(keycode)
        elif action[1] == 'release':
            keycode = int(action[2], 16)  # Convert hex string to integer
            commands.release_key(keycode)
        elif action[1] == 'type':
            text = ','.join(action[2:])  # Rejoin the rest of the action list as a string
            commands.type_string(text)



with mss.mss() as sct:
    monitor = sct.monitors[1]

    while True:
        # Capture and send screen
        img = np.array(sct.grab(monitor))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        ret, buffer = cv2.imencode('.jpg', img)
        video_socket.sendall(len(buffer).to_bytes(4, byteorder='big'))
        video_socket.sendall(buffer)

        # Non-blocking receive for commands
        try:
            command_socket.settimeout(0.01)
            command = command_socket.recv(1024).decode()
            if command:
                process_command(command)
        except socket.timeout:
            continue
