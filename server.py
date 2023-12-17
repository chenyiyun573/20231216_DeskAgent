import socket
import cv2
import numpy as np
import threading

# Function to send commands to the client
def send_commands(command_conn):
    while True:
        cmd = input("Enter command: ")
        command_conn.sendall(cmd.encode())

# Function to handle video streaming
def handle_video_stream(video_conn):
    while True:
        length = int.from_bytes(video_conn.recv(4), byteorder='big')
        buffer = b''
        while len(buffer) < length:
            buffer += video_conn.recv(length - len(buffer))
        img = cv2.imdecode(np.frombuffer(buffer, dtype='uint8'), cv2.IMREAD_COLOR)
        print(img.shape)
        cv2.imshow('Screen', img)
        if cv2.waitKey(1) == ord('q'):
            break

# Set up command socket
command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
command_socket.bind(('0.0.0.0', 4000))  # Port for commands
command_socket.listen(1)
command_conn, _ = command_socket.accept()

# Set up video socket
video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_socket.bind(('0.0.0.0', 4001))  # Port for video
video_socket.listen(1)
video_conn, _ = video_socket.accept()

# Start threads for commands and video streaming
threading.Thread(target=send_commands, args=(command_conn,)).start()
threading.Thread(target=handle_video_stream, args=(video_conn,)).start()
