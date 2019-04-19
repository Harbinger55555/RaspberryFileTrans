from _thread import *
import library
import socket
import threading
PORT = 8080
lock = threading.Lock()

def threadFunction(connection):
    # Receives/sends data indefinitely. Use ^C to exit the program.
    while True:
        # receive data
        data = connection.recv(1024)
        if not data:
            print('Exiting\n')
            lock.release()
            break
        # do something with data
        connection.send(data)
    connection.close()
            

def main():
    server_socket = library.CreateServerSocket(PORT)
    # Handle commands indefinitely (^C to exit)
    while True:
        client_socket, (address, port) = library.ConnectClientToServer(server_socket)
        print('Received connection from %s:%d' % (address, port))
        lock.acquire()
        print('Connected to : ', address, ':', port, '\n')
        start_new_thread(threadFunction, (client_socket,))
    server_socket.close()

main()