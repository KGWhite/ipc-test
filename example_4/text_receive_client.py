# text_receive_client.py

import socket
import select
import time

HOST = 'localhost'
PORT = 65439

ACK_TEXT = 'text_received'


def main():
    # instantiate a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('socket instantiated')

    # connect the socket
    connectionSuccessful = False
    while not connectionSuccessful:
        try:
            sock.connect((HOST, PORT))    # Note: if execution gets here before the server starts up, this line will cause an error, hence the try-except
            print('socket connected')
            connectionSuccessful = True
        except:
            pass
        # end try
    # end while

    socks = [sock]
    while True:
        readySocks, _, _ = select.select(socks, [], [], 5)
        for sock in readySocks:
            message = receiveTextViaSocket(sock)
            print('received: ' + str(message))
        # end for
    # end while
# end function

def receiveTextViaSocket(sock):
    # get the text via the scoket
    encodedMessage = sock.recv(1024)

