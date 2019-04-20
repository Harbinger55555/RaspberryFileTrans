from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from threading import Thread
import aes
import library
import os
import sys

class ClientThread(Thread):

    def __init__(self, sock, filepath):
        Thread.__init__(self)
        self.sock = sock
        self.filepath = filepath

    def run(self):
        try:
            with open(self.filepath, 'rb') as f:
                # Open the file in binary and send it to client.
                filename = os.path.basename(self.filepath)
                # TODO: Send filename.
                # TODO: Send files in chunks if time allows.
                self.sock.send(aes.encrypt(b'f'))
                self.sock.send(aes.encrypt(f.read()))

        except FileNotFoundError:
            # Inform file not found.
            self.sock.send(aes.encrypt(b't'))
            self.sock.send(aes.encrypt(b'File not found!\n'))

        finally:
            self.sock.close()


def main(serverAddr, serverPort):
    server_socket = library.CreateServerSocket(serverAddr, serverPort)
    clientThreads = []
    
    # Handle commands indefinitely (^C to exit)
    while True:
        # Wait until a client connects, then get a socket for the  client.
        client_socket, addr = library.ConnectClientToServer(server_socket)
        
        # Read the request.
        request = library.ReadRequest(client_socket)
        command, filepath = library.ParseRequest(request)
        
        if command == 'GET' and filepath is not None:
            newClientThread = ClientThread(client_socket, filepath)
            newClientThread.start()
            clientThreads.append(newClientThread)

        else:
            client_socket.send(aes.encrypt(b't'))
            client_socket.send(aes.encrypt(b'Invalid request!\n'))
            client_socket.close()

    for t in clientThreads:
        t.join()

    server_socket.close()


if __name__ == "__main__":
    serverAddr = 'localhost'
    serverPort = 8080
    if len(sys.argv) > 1:
        serverAddr = sys.argv[1]
    if len(sys.argv) > 2:
        serverPort = sys.argv[2]
    main(serverAddr, serverPort)
