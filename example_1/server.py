# server.py
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = socket.gethostname()
port = 8088
s.bind((host,port))
try:
    while True:
        receive_data,addr = s.recvfrom(1024)
        print("Message from server: " + str(addr))
        print(receive_data.decode('utf-8'))
        msg = input('please input send to msg:')
        s.sendto(msg.encode('utf-8'),addr)
except:
    s.close()
