from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import aes
import library
import os
import socket
import sys
import time

# Macro to indicate the max length of server's text response.
MAX_SVR_RESP_TXT_LEN = 256

# The block size determined by AES (Must be consistent with aes.py).
BLOCK_SIZE = 16

# Variable to store the start time of a request.
RTT_START = 0

def createFile(addr, sock, filename):
    with open(str(addr) + '_' + filename, 'wb') as f:
        while True:
            # The loop gets empty padLen and data before breaking out.
            padLen = aes.decrypt(sock.recv(BLOCK_SIZE)).decode()
            
            if padLen:
                data = aes.decrypt(sock.recv(BLOCK_SIZE), int(padLen))
            else:
                data = aes.decrypt(sock.recv(BLOCK_SIZE))

            if not data:
                break
            # Write data to the file
            f.write(data)
        

def processResponse(addr, sock, filename):
    restype = aes.decrypt(sock.recv(BLOCK_SIZE))

    # Round Trip time for the request is calculated when a response is obtained from the server.
    RTT = time.time() - RTT_START

    # Simply print the error if response is a text, else make a file using the
    # bytes.
    if restype == b't':
        print(aes.decrypt(sock.recv(MAX_SVR_RESP_TXT_LEN)).decode().strip('\n'))
    
    elif restype == b'f':
        createFile(addr, sock, filename)
        print("File received and successfully created!")
    else:
        print("Unknown response type...")

    print("Rount trip time =", RTT)


def main(serverAddr, serverPort):
    clientSock = library.CreateClientSocket(serverAddr, serverPort)
    cmdLine = input()
    command, filepath = library.ParseRequest(cmdLine)
    filename = ''
    if filepath:
        filename = os.path.basename(filepath)
    
    try:
        # Send the command line request to server and return the response.
        RTT_START = time.time()
        clientSock.send(aes.encrypt(cmdLine.encode()))
        processResponse(serverAddr, clientSock, filename)
    
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

