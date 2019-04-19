from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import socket
import time
COMMAND_BUFFER_SIZE = 256

def CreateServerSocket(port):
    """Creates a socket that listens on a specified port.

    Args:
        port: int from 0 to 2^16. Low numbered ports have defined purposes. Almost
                all predefined ports represent insecure protocols that have died out.
    Returns:
        An socket that implements TCP/IP.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', port))
    server.listen()
    return server

def ConnectClientToServer(server_socket):
    """Creates a socket that listens on a specified port.

    Args:
        server_socket: a socket that implements TCP/IP
    Returns:
        A socket and an address that is bound to that socket
    """
    return server_sock.accept()

def CreateClientSocket(server_addr, port):
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((server_addr, port))
	return client
