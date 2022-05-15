# client.py
import socket
import time

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Local Machine Address
HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 8000  # Port to listen on (non-privileged ports are > 1023)

s.bind((HOST, PORT))
s.listen()

clientsocket,addr = s.accept()
print(f"{addr} is connected.")
