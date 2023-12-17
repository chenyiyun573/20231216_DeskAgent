import socket
import cv2
import numpy as np
import threading

# Function to send commands to the client
def send_commands(conn):
    while True:
        cmd = input("Enter command: ")  # Command input from the terminal
        conn.sendall(cmd.encode())

# Set up the socket for listening
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 4000))
server_socket.listen(5)

# Accept a client connection
conn, addr = server_socket.accept()

# Start a thread to send commands to the client
threading.Thread(target=send_commands, args=(conn,)).start()

while True:
    # Read the size of the image data
    length = int.from_bytes(conn.recv(4), byteorder='big')
    
    # Read the image data
    buffer = b''
    while len(buffer) < length:
        buffer += conn.recv(length - len(buffer))
    
    # Convert the data to an image
    img = cv2.imdecode(np.frombuffer(buffer, dtype='uint8'), cv2.IMREAD_COLOR)

    # Display the image
    cv2.imshow('Screen', img)
    if cv2.waitKey(1) == ord('q'):
        break

conn.close()
server_socket.close()
cv2.destroyAllWindows()
