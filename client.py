import socket
import pickle
import json
from dict2xml import dict2xml
import threading

class Client:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data = dict()
        self.filename = ""

    def connect_to_server(self):

        host = '0.0.0.0'  # Standard loopback interface address (localhost)
        port = 8000  # Port to listen on (non-privileged ports are > 1023)
        self.s.connect((host, port))

    def disconnect_server(self):
        self.s.close()

    def dict(self):
        key = input("Enter Key: ")
        value = input("Enter Value: ")
        self.data[key] = [value]
        print(self.data)


        serialize_format = input("Enter the Format: ")

        if serialize_format == 'BINARY':
            with open('output.bin', 'wb') as f:
                pickle.dump(self.data, f)
                self.filename = 'output.bin'
                print("Serialization in BINARY format done")

        elif serialize_format == 'JSON':
            with open('output.json', 'w') as f:
                json.dump(self.data, f)
                self.filename = 'output.json'
                print("Serialization in JSON format done")

        elif serialize_format == 'XML':
            with open('output.xml', 'w') as f:
                f.write(dict2xml(self.data))
                self.filename = 'output.xml'
                print("Serialization in XML format done")


    def text_file(self):
        self.filename = input("Enter Filename to be sent: ")
        encrypted = input("Enter E to send Encrypted Version else P: ")

    def send_data_to_server(self):
        self.s.send(self.filename.encode())


if __name__ == "__main__":
    client = Client()
    client.connect_to_server()
    user_input = input("Enter D to create Dictionary or Enter T to send the Text File: ")
    if user_input == 'D':
        client.dict()
        client.send_data_to_server()

    if user_input == 'T':
        client.text_file()
        client.send_data_to_server()

    client.disconnect_server()


