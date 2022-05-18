# client.py
import socket
import threading
import time
import os


class Server:

    def __init__(self):

        # Create a socket object
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.configuration = ''
        self.filename = "s_test"

    def start_server(self):

        host = '0.0.0.0'
        port = 8000
        print("CONFIGURE: PRINT CONTENT")
        self.configuration = input("Enter S for SCREEN or Enter F for FILE: ")
        print(f"Server Configured in Mode: {self.configuration}")
        self.s.bind((host, port))
        self.s.listen()
        c, addr = self.s.accept()
        print(f"{addr} is connected.")
        threading.Thread(target=self.receive_data, args=(c, addr)).start()

    def receive_data(self, c, addr):
        data = c.recv(1024)
        encryption = c.recv(1024).decode()
        print(encryption)
        filename = c.recv(1024).decode()
        print(filename)

        if self.configuration == 'S':
            if encryption == 'Non-Encrypted':
                print('MESSAGE: ' + data)
            else:
                print("To be Decided")

        elif self.configuration == 'F':
            if encryption == 'Non-Encrypted':
                self.filename = 's_' + filename
                with open(self.filename, "wb") as received_file:
                    received_file.write(data)
            else:
                print("To be Decided")

        c.close()


if __name__ == "__main__":
    server = Server()
    server.start_server()

