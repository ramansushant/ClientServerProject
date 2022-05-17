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

        serialize_format = input("Enter the Format: ")

        if serialize_format == 'BINARY':
            serialized_data_byte = pickle.dumps(self.data)
            print(serialized_data_byte)

        if serialize_format == 'JSON':
            serialized_data_json = json.dumps(self.data)
            print(serialized_data_json)

        if serialize_format == 'XML':
            serialized_data_json = json.dumps(self.data)
            print(serialized_data_json)

    def text_file(self):
        file_name = input("Enter Filename to be sent: ")
        encrypted = input("Enter E to send Encrypted Version else P: ")

    def send_data_to_server(self):
        self.s.send(self.data)


if __name__ == "__main__":
    client = Client()
    client.connect_to_server()
    user_input = input("Enter D to create Dictionary or Enter T to send the Text File: ")
    if user_input == 'D':
        client.dict()
    if user_input == 'T':
        client.text_file()
    client.disconnect_server()


