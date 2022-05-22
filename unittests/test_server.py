import sys
from importlib import reload
from unittest import TestCase
from unittest.mock import MagicMock, patch, call, mock_open

from cryptography.fernet import Fernet

from server import METADATA_SEPARATOR


class ServerTestCase(TestCase):
    def test_a_init_calls_create_socket(self):
        self.socket_module_mock.socket.assert_called_once()

    @patch('server.get_input', return_value='test')
    def test_start_server(self, input):
        self.server.start_server()
        self.socket_instance_mock.bind.has_one_call()
        self.socket_instance_mock.listen.has_one_call()
        self.socket_instance_mock.accept.has_one_call()
        self.assertEqual('test', self.server.configuration)

    @patch('cryptography.fernet.Fernet.decrypt', return_value='123')
    @patch('server.print_output')
    def test_print_encrypted_text(self, print_output, fernet):
        self.server.print_encrypted_text('123')
        print_output.assert_called_with('123')

    @patch('builtins.open', mock_open(read_data=Fernet.generate_key()))
    @patch('cryptography.fernet.Fernet.decrypt', return_value='123')
    @patch('server.print_output')
    def test_save_encrypted_text(self, print_output, fernet):
        self.server.save_encrypted_text('123', '123.csv')
        self.assertEqual('s_123.csv', self.server.server_filename)

    @patch('server.print_output')
    def test_print_unencrypted_text(self, print_output):
        recv_function = MagicMock()
        recv_function.decode = MagicMock(return_value=f'Non-Encrypted{METADATA_SEPARATOR}123.csv')

        c_mock = MagicMock()
        c_mock.recv = MagicMock(return_value=recv_function)

        self.server.configuration = 'S'
        self.server.receive_data(c_mock, None)
        print_output.assert_called_with('MESSAGE: Non-Encrypted$$123.csv')

    def setUp(self):
        # Set up mocks for socket module
        socket_module_mock = MagicMock()
        socket_instance_mock = MagicMock()
        socket_instance_mock.accept = MagicMock(return_value=[1, 2])
        socket_module_mock.socket = MagicMock()
        socket_module_mock.socket.return_value = socket_instance_mock

        threading_module_mock = MagicMock()

        # Apply socket patch
        sys.modules['socket'] = socket_module_mock
        sys.modules['threading'] = threading_module_mock

        # Import our client, and re-load it, to ensure a fresh socket mock is used between test runs
        import server
        reload(server)
        from server import Server

        self.server = Server()

        self.socket_module_mock = socket_module_mock
        self.socket_instance_mock = socket_instance_mock
