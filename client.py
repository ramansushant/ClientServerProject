import socket
import pickle
import json
from dict2xml import dict2xml
from cryptography.fernet import Fernet
import os

# Metadata seperator is used so that Filename and Content Type can be split on Server
METADATA_SEPARATOR = "$$"


class Client:
    # This class connects the Client to Server and send the files both in Encrypted and Decrypted Form

    def __init__(self):
        # Socket to connect to Server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Global Variables that are accessed across functions
        self.data = dict()
        self.filename = ""
        self.key_filename = 'key.key'
        self.encrypted_filename = ""
        self.encrypted = ""
        self.encrypted_text = ""

    def connect_to_server(self):
        # Standard loopback interface address (localhost)
        host = '0.0.0.0'
        # Port to listen
        port = 8000
        try:
            # To connect client to server on specified Host and Port
            self.s.connect((host, port))
        except ConnectionRefusedError:
            print("Connection failed")

    def disconnect_server(self):
        self.s.close()  # To disconnect client from server

    def dict(self):
        # User Input in the Dictionary Data Type
        key = input("Enter Key: ")
        value = input("Enter Value: ")
        self.data[key] = [value]
        print(self.data)

        # Input to Serialize the Dictionary in the user chosen format

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

        else:
            print("Incorrect Format. Try Again")

    def text_file(self):
        try:
            # User Input on the File that client wants to send to the server
            self.filename = input("Enter Filename to be sent: ")
            self.encrypted = input("Enter E to send Encrypted Version else P: ")

            # User Input on the File that client wants to send to the server
            if self.encrypted == "E":
                if os.path.exists(self.key_filename):
                    with open(self.key_filename, "rb") as key_file:
                        key = key_file.read()
                else:
                    # Generate Key for Encryption
                    key = Fernet.generate_key()
                    with open(self.key_filename, "wb") as key_file:
                        key_file.write(key)

                f = Fernet(key)
                with open(self.filename, 'rb') as file:
                    text_in_file = file.read()

                # Encrypt Content of the Text File
                self.encrypted_text = f.encrypt(text_in_file)
                self.encrypted_filename = 'encrypted_' + self.filename

                # Write Encrypted content into a new file
                with open(self.encrypted_filename, 'wb') as encrypted_file:
                    encrypted_file.write(self.encrypted_text)

                print("Encrypted file saved as: ", self.encrypted_filename)

        except Exception as ex:
            print("Error Reading the File " + str(ex))

    def send_data_to_server(self):
        try:
            if self.encrypted == "E":
                e = "Encrypted"
                self.s.send(f"{e}{METADATA_SEPARATOR}{self.encrypted_filename}".encode())
                with open(self.encrypted_filename, "rb") as file:
                    data = file.read(4096)
                    while data:
                        self.s.send(data)
                        data = file.read(4096)
                print("Encrypted Data Sent Successfully")


            else:
                self.s.send(f"Non-Encrypted{METADATA_SEPARATOR}{self.filename}".encode())
                with open(self.filename, "rb") as file:
                    data = file.read(4096)
                    while data:
                        self.s.send(data)
                        data = file.read(4096)
                print("Non-Encrypted Data Sent Successfully")

        except Exception as ex:
            print("Error Sending the File " + str(ex))


if __name__ == "__main__":

    client = Client()
    # To Connect Client with Server
    client.connect_to_server()

    # User Input to create a dictionary or send the text file
    user_input = input("Enter D to create Dictionary or Enter T to send the Text File: ")

    if user_input == 'D':
        client.dict()
        client.send_data_to_server()

    elif user_input == 'T':
        client.text_file()
        client.send_data_to_server()

    else:
        print("Incorrect Input")

    # Disconnect Server
    client.disconnect_server()
