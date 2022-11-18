from multiprocessing import Process,Pipe
import os

def func(conn):
    conn.send("Hi I'm your subprocess. My ID is %d"%os.getpid())
    print("ID %d receive main_process message: "%os.getpid(),conn.recv())
    conn.close()
       
if __name__ == "__main__":
    main_conn , sub_conn = Pipe()   # 使用Pipe()函數同時建立主進程及自進程兩個通信的物件
    processlist=[]
    for i in range(2):
        proc = Process(target=func,args=(sub_conn,))
        processlist.append(proc)
        proc.start()
        print("I'm mainprocess, I receive my sub_process message: ",main_conn.recv())
        main_conn.send("Remember I'm your Master")
    for each_process in processlist:
        each_process.join()
