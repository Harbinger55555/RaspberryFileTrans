from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from threading import Thread
import library
import os

LISTENING_PORT = 8080

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
                # TODO: attach filename.
                self.sock.send(b'f' + f.read())

        except FileNotFoundError:
            # Inform file not found.
            self.sock.send(b'tFile not found!\n')

        finally:
            self.sock.close()


def main():
    server_socket = library.CreateServerSocket(LISTENING_PORT)
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
            client_socket.send(('tInvalid request!\n').encode())
            client_socket.close()

    for t in clientThreads:
        t.join()

    server_socket.close()

if __name__ == "__main__":
    main()
