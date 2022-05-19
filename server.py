# client.py
import socket
import threading
import time
import os
from cryptography.fernet import Fernet

METADATA_SEPARATOR = "$$"

class Server:

    def __init__(self):

        # Create a socket object
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.configuration = ''
        self.server_filename = ""
        self.key_filename = 'key.key'
        self.decrypted_text = ""

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
        metadata = c.recv(4096).decode()
        encryption, filename = metadata.split(METADATA_SEPARATOR)
        data = c.recv(4096)

        if self.configuration == 'S':

            if encryption == 'Non-Encrypted':
                print('MESSAGE: ' + data.decode())

            else:
                if os.path.exists(self.key_filename):
                    with open(self.key_filename, "rb") as key_file:
                        key = key_file.read()
                f = Fernet(key)
                self.decrypted_text = f.decrypt(data)
                print(self.decrypted_text)

        elif self.configuration == 'F':
            if encryption == 'Non-Encrypted':
                self.server_filename = 's_' + filename
                with open(self.server_filename, "wb") as received_file:
                    received_file.write(data)
            else:
                if os.path.exists(self.key_filename):
                    with open(self.key_filename, "rb") as key_file:
                        key = key_file.read()
                f = Fernet(key)
                self.decrypted_text = f.decrypt(data)
                self.server_filename = 's_' + filename
                print(self.server_filename)
                with open(self.server_filename, "wb") as received_file:
                    received_file.write(self.decrypted_text)
                    print("File Saved as:" + self.server_filename)

        c.close()


if __name__ == "__main__":
    server = Server()
    server.start_server()

