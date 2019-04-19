from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import library
import socket
import sys

MAX_SERVER_RESPONSE_LEN = 256

def createFile(sock):
    with open('received_file', 'wb') as f:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            # Write data to the file
            f.write(data)


def processResponse(sock):
    restype = sock.recv(1)

    # Simply print the error if response is a text, else make a file using the
    # bytes.
    if restype == b't':
        print(sock.recv(MAX_SERVER_RESPONSE_LEN).decode().strip('\n'))
    elif restype == b'f':
        createFile(sock)
        print("File received and successfully created!")
    else:
        print("Unknown response type...")


def main(serverAddr, serverPort):
    clientSock = library.CreateClientSocket(serverAddr, serverPort)
    cmdLine = input()
    
    try:
        # Send the command line request to server and return the response.
        clientSock.sendall(cmdLine.encode())
        processResponse(clientSock)
    
    finally:
        clientSock.close()


if __name__=="__main__":
    serverAddr = 'localhost'
    serverPort = 8080
    if len(sys.argv) > 1:
        serverAddr = sys.argv[1]
    if len(sys.argv) > 2:
        serverPort = sys.argv[2]
    main(serverAddr, serverPort)
