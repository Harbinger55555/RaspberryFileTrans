from _thread import *
import library
import socket
import threading
PORT = 8080
lock = threading.Lock()

def parseData(data):
    """
    Parses a command and returns the command name and filename.

    All commands are of the form:
        COMMAND filename

    Args:
        data: string command and filename.
    Returns:
        command, filename. Each of these can be None.
    """
    args = data.strip().split(' ')
    command = None
    if args:
        command = args[0]
    else:
        return None, None
    data = None
    if len(args) > 1:
        data = ' '.join(args[2:])
    else:
        return command, None
    return command, data

def fileTransfer(filename, connection):
    """
    Transfers a file over a connection.

    Args:
        filename: string filename.
        connection: socket being communicated over.
    Returns:
        N/A
    """
    file = open(filename, 'rb')
    info = file.read(1024)
    while (info):
        connection.send(info)
        info = file.read(1024)
    file.close()

def threadFunction(connection):
    """
    Thread handles a request over a connection.

    Args:
        connection: socket being communicated over.
    Returns:
        N/A
    """
    # Receives/sends data indefinitely. Use ^C to exit the program.
    while True:
        data = connection.recv(1024)
        if not data:
            print('Exiting\n')
            lock.release()
            break
        command, filename = parseData(data)
        if not (command or filename):
            print('Invalid request\n')
            lock.release()
            break
        fileTransfer(filename, connection)
        connection.send(data)
    connection.close()
            

def main():
    """
    Server driver creates a server socket that listens on a specified port
    and creates threads to handle client requests when a connection is received.

    Args:
        N/A
    Returns:
        N/A
    """
    server_socket = library.CreateServerSocket(PORT)
    # Handle commands indefinitely (^C to exit)
    while True:
        client_socket, (address, port) = library.ConnectClientToServer(server_socket)
        print('Received connection from %s:%d\n' % (address, port))
        lock.acquire()
        start_new_thread(threadFunction, (client_socket,))
    server_socket.close()

main()
