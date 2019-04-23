from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import aes
import library
import os
import socket
import sys
import time
import threading

# Macro to indicate the max length of server's text response.
MAX_SVR_RESP_TXT_LEN = 256

# The block size determined by AES (Must be consistent with aes.py).
BLOCK_SIZE = aes.BLOCK_SIZE

# Dictionary of server addresses and ports to multi-thread request from.
SERVER_ADDRS_AND_PORTS = {'localhost': 8080,
                          '127.0.0.1': 9900,}

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
        

def processResponse(addr, sock, filename, rttStart):
    restype = aes.decrypt(sock.recv(BLOCK_SIZE))

    # Round Trip time for the request is calculated when a response is obtained from the server.
    RTT = time.time() - rttStart

    # Simply print the error if response is a text, else make a file using the
    # bytes.
    if restype == b't':
        print(aes.decrypt(sock.recv(MAX_SVR_RESP_TXT_LEN)).decode().strip('\n'))
    
    elif restype == b'f':
        createFile(addr, sock, filename)
        print("File received from ({}) and successfully created!".format(addr))
    else:
        print("Unknown response type...")

    print("Rount trip time =", RTT)


def getFileRequest():
    cmdLine = input()
    command, filepath = library.ParseRequest(cmdLine)
    filename = ''
    if filepath:
        filename = os.path.basename(filepath)

    return cmdLine, filename


def requestFromServer(serverAddr, serverPort, cmdLine, filename):
    clientSock = library.CreateClientSocket(serverAddr, serverPort)
    
    try:
        # Send the command line request to server and return the response.
        rttStart = time.time()
        clientSock.send(aes.encrypt(cmdLine.encode()))
        processResponse(serverAddr, clientSock, filename, rttStart)
    
    finally:
        clientSock.close()


def multiRequest(serverAddrsAndPorts, cmdLine, filename):
    ts = []
    for addr, port in serverAddrsAndPorts.items():
        t = threading.Thread(target=requestFromServer, 
                             args=(addr, port, cmdLine, filename))
        t.start()
    
    for t in ts:
        t.join()


def main():
    serverAddr = 'localhost'
    serverPort = 8080
    cmdLine, filename = getFileRequest()
    if len(sys.argv) > 1:
        if sys.argv[1] == '-m':
            multiRequest(SERVER_ADDRS_AND_PORTS, cmdLine, filename)
            return
        serverAddr = sys.argv[1]
    if len(sys.argv) > 2:
        serverPort = sys.argv[2]
    requestFromServer(serverAddr, serverPort, cmdLine, filename)


if __name__=="__main__":
    main()

