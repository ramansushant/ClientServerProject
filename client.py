#client.py
import socket

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 8000  # Port to listen on (non-privileged ports are > 1023)

s.connect((HOST, PORT))
tm = s.recv(1024)
s.close()