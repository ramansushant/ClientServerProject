import sys
from importlib import reload
from unittest import TestCase
from unittest.mock import MagicMock, call, patch, mock_open

from cryptography.fernet import Fernet

from client import METADATA_SEPARATOR


class ClientTestCase(TestCase):
    def test_a_init_calls_create_socket(self):
        self.socket_module_mock.socket.assert_called_once()

    def test_connect_calls_socket_connect(self):
        self.client.connect_to_server()
        self.socket_instance_mock.connect.assert_called_once()

    def test_disconnect_calls_socket_close(self):
        self.client.disconnect_server()
        self.socket_instance_mock.close.assert_called_once()

    @patch('builtins.open', mock_open(read_data='123'))
    @patch('client.get_input', side_effect=['k', 'v', 'JSON'])
    def test_json_dict_create(self, input_mock):
        self.client.dict()
        self.assertEqual(['v'], self.client.data['k'])
        self.assertEqual('output.json', self.client.filename)

    @patch('builtins.open', mock_open(read_data='123'))
    @patch('client.get_input', side_effect=['k', 'v', 'XML'])
    def test_xml_dict_create(self, input_mock):
        self.client.dict()
        self.assertEqual(['v'], self.client.data['k'])
        self.assertEqual('output.xml', self.client.filename)

    @patch('builtins.open', mock_open(read_data='123'))
    @patch('client.get_input', side_effect=['k', 'v', 'BINARY'])
    def test_binary_dict_create(self, input_mock):
        self.client.dict()
        self.assertEqual(['v'], self.client.data['k'])
        self.assertEqual('output.bin', self.client.filename)

    @patch('client.get_input', side_effect=['123.csv', 'P'])
    def test_text_file_unencrypted(self, input):
        self.client.text_file()
        self.assertEqual('', self.client.encrypted_filename)

    @patch('builtins.open', mock_open(read_data=b'data'))
    @patch('client.get_input', side_effect=['123.csv', 'E'])
    @patch('client.Client._get_key', return_value=Fernet.generate_key())
    def test_text_file_encrypted(self, input, key):
        self.client.text_file()
        self.assertEqual('encrypted_123.csv', self.client.encrypted_filename)

    @patch('builtins.open', mock_open(read_data='data'))
    def test_send_unencrypted_data_to_server(self):
        self.client.encrypted = 'Not-E'
        filename = 'my_file.csv'
        self.client.filename = filename
        self.client.send_data_to_server()
        self.socket_instance_mock.send.assert_has_calls([
            call(f'Non-Encrypted{METADATA_SEPARATOR}{filename}'.encode()),
            call('data')
        ])

    @patch('builtins.open', mock_open(read_data='data'))
    def test_send_encrypted_data_to_server(self):
        self.client.encrypted = 'E'
        filename = 'my_file.csv'
        self.client.encrypted_filename = filename
        self.client.send_data_to_server()
        self.socket_instance_mock.send.assert_has_calls([
            call(f'Encrypted{METADATA_SEPARATOR}{filename}'.encode()),
            call('data')
        ])

    @patch('builtins.open', mock_open(read_data='123'))
    @patch('os.path.exists')
    def test_get_existing_key(self, exists_mock):
        exists_mock.return_value = True
        self.client.key_filename = '123.csv'
        self.assertEqual('123', self.client._get_key())

    @patch('builtins.open', mock_open(read_data='123'))
    @patch('cryptography.fernet.Fernet.generate_key')
    @patch('os.path.exists')
    def test_get_new_key(self, exists_mock, fernet_mock):
        exists_mock.return_value = False
        fernet_mock.return_value = '123'
        self.client.key_filename = '123.csv'
        self.assertEqual('123', self.client._get_key())

    def setUp(self):
        # Set up mocks for socket module
        socket_module_mock = MagicMock()
        socket_instance_mock = MagicMock()
        socket_module_mock.socket = MagicMock()
        socket_module_mock.socket.return_value = socket_instance_mock

        # Apply socket patch
        sys.modules['socket'] = socket_module_mock

        # Import our client, and re-load it, to ensure a fresh socket mock is used between test runs
        import client
        reload(client)
        from client import Client

        self.client = Client()

        self.socket_module_mock = socket_module_mock
        self.socket_instance_mock = socket_instance_mock
