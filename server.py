from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from threading import Thread
import library

LISTENING_PORT = 8080

class ClientThread(Thread):

    def __init__(self, ip, port, sock, filepath):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        self.filepath = filepath

    def run(self):
        try:
            with open(self.filepath, 'rb') as f:
                # Open the file in binary and send it to client.
                self.sock.send(f.read())

        except FileNotFoundError:
            # Inform file not found.
            self.sock.send(b'File not found!\n')

        finally:
            self.sock.close()


def main():
    server_socket = library.CreateServerSocket(LISTENING_PORT)
    clientThreads = []
    
    # Handle commands indefinitely (^C to exit)
    while True:
        # Wait until a client connects, then get a socket for the  client.
        client_socket, (address, port) = library.ConnectClientToServer(server_socket)
        print('Received connection from %s:%d' % (address, port))
        
        # Read the request.
        request = library.ReadRequest(client_socket)
        command, filepath = library.ParseRequest(request)
        
        if command == 'GET':
            newClientThread = ClientThread(address, 
                                           port, 
                                           client_socket,
                                           filepath)
            newClientThread.start()
            clientThreads.append(newClientThread)

        else:
            client_socket.send(('Invalid Command {}\n'.format(command)).encode())
            client_socket.close()

    for t in clientThreads:
        t.join()

    server_socket.close()

if __name__ == "__main__":
    main()
