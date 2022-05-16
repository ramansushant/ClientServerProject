#client.py
import socket
import pickle
import json

class Client:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data = dict()

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

        serialized_data_byte = pickle.dumps(self.data)
        print(serialized_data_byte)

        serialized_data_json = json.dumps(self.data)
        print(serialized_data_json)

    def send_data_to_server(self):
        self.s.send(self.data)


if __name__ == "__main__":
    client = Client()
    client.connect_to_server()
    client.dict()
    client.disconnect_server()


