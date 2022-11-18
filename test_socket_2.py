import multiprocessing as mp
import socket

def worker2():
    print('456')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('', 9092))
        data = s.recv(1024)
        s.close()
    print('Received', repr(data))

if __name__ == '__main__':
    # input intergers
    #print("You can type intergers and then click [ENTER].")
    #input = input()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 9092))
        s.listen(1)
        
        p = mp.Process(target=worker2, args=())
        p.daemon = True
        p.start()

        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            conn.sendall(b'Hello, world')
        
        s.close()

