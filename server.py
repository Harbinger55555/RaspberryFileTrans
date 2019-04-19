from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import library


LISTENING_PORT = 8080


def sendFile(client_socket, filepath):
    try:
        with open(filepath, 'rb') as f:
            # TODO: Open the file in binary and send it to client.
            client_socket.send(filepath.encode())
    except FileNotFoundError:
        # Send None.
        client_socket.send(b'File not found!\n')

def main():
    server_socket = library.CreateServerSocket(LISTENING_PORT)
    
    # Handle commands indefinitely (^C to exit)
    while True:
        # Wait until a client connects, then get a socket for the  client.
        client_socket, (address, port) = library.ConnectClientToServer(server_socket)
        print('Received connection from %s:%d' % (address, port))
        
        try:
            # Read the request.
            request = library.ReadRequest(client_socket)
            command, filepath = library.ParseRequest(request)
            
            if command == 'GET':
                sendFile(client_socket, filepath)
            else:
                client_socket.send(b'Invalid Command {}'.format(command))
        
        finally:
            client_socket.close()

if __name__ == "__main__":
    main()
