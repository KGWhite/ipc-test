# client.py
import socket

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
try:
    while True:
        host = socket.gethostname()
        port = 8088
        send_data = input('please input msg:')
        s.sendto(send_data.encode('utf-8'),(host,port))
        msg,addr = s.recvfrom(1024)
        print('Message from server: ' + str(addr))
        print(msg.decode('utf-8'))
except:
    s.close()
