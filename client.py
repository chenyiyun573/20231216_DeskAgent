import socket
import cv2
import numpy as np
import mss

# Set up the socket connection to the server
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
