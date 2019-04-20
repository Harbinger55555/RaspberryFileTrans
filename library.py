from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import aes
import socket
import time

COMMAND_BUFFER_SIZE = 256

def GetIPv6Addr(addr, port):
    # Try to detect whether IPv6 is supported at the present system and
    # fetch the IPv6 address.
    if not socket.has_ipv6:
        raise Exception("the local machine has no IPv6 support enabled")

    addrs = socket.getaddrinfo(addr, port, socket.AF_INET6, 0, socket.SOL_TCP)

    if len(addrs) == 0:
        raise Exception("there is no IPv6 address configured for the address")

    return addrs[0][-1]


def CreateServerSocket(addr, port):
    """Creates a socket that listens on a specified port.

    Args:
        addr: ip address or "localhost" which will be used as a listening
                socket for the server.
        port: int from 0 to 2^16. Low numbered ports have defined purposes. Almost
                all predefined ports represent insecure protocols that have died out.
    Returns:
        An socket that implements TCP/IP.
    """
    sockaddr = GetIPv6Addr(addr, port)

    server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(sockaddr)
    server.listen()
    return server


def ConnectClientToServer(server_sock):
	return server_sock.accept()


def CreateClientSocket(server_addr, port):
    sockaddr = GetIPv6Addr(server_addr, port)
    client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    client.connect(sockaddr)
    return client


def ReadRequest(sock):
    """Read the request line from a socket. The request must end in newline."""
    return aes.decrypt(sock.recv(COMMAND_BUFFER_SIZE)).decode()


def ParseRequest(request):
    """Parses the request and returns the command name and filepath."""
    args = request.strip().split(' ')
    command = None
    if args:
        command = args[0]
    filepath = None
    if len(args) > 1:
        filepath = ' '.join(args[1:])
    return command, filepath

