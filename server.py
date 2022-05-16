# client.py
import socket
import threading
import time


class Server:

    def __init__(self):

        # Create a socket object
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data = dict()

    def start_server(self):

        host = '0.0.0.0'
        port = 8000
        self.s.bind((host, port))
        self.s.listen()
        c, addr = self.s.accept()
        print(f"{addr} is connected.")
        threading.Thread(target=self.receive_data, args=(c, addr,)).start()

    def receive_data(self, c, addr):
        self.data = c.recv(1024)
        print(self.data)
        c.close()


if __name__ == "__main__":
    server = Server()
    server.start_server()

