from multiprocessing import Process, Pipe, shared_memory
import socket
import os
import time
import numpy as np
import statistics
import random
import pickle

def target_mean(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('', port))
        data = s.recv(1024)
        print(f'Mean: {statistics.mean(pickle.loads(data))}')

def target_median(conn):
    print(f'Median: {statistics.median(conn.recv())}')
    conn.close()

def target_mode(shm_name, np_array_shape, np_array_dtype):
    existing_shm = shared_memory.SharedMemory(name=shm_name)
    c = np.ndarray(np_array_shape, dtype=np_array_dtype, buffer=existing_shm.buf)
    print(f'Mode: {statistics.mode(c)}')

if __name__ == '__main__':
    ##############################
    # input intergers
    ##############################
    print("Server is ready. You can type intergers and then click [ENTER].  Clients will show the mean, median, and mode of the input values.")
    input_int_array = [int(x) for x in input().split()]

    ##############################
    # Socket
    ##############################
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        PORT = random.randint(50000,60000) #50007
        s.bind(('', PORT))
        s.listen(1)

        p = Process(target=target_mean, args=(PORT,))
        p.daemon = True
        p.start()

        conn, addr = s.accept()
        with conn:
            data = pickle.dumps(input_int_array)
            conn.sendall(data)
        p.join()

    ##############################
    # Pipe
    ##############################
    parent_conn, child_conn = Pipe()

    p = Process(target=target_median, args=(child_conn,))
    p.start()

    parent_conn.send(input_int_array)

    p.join()

    ##############################
    # Shared Memory
    ##############################
    a = np.array(input_int_array)
    shm = shared_memory.SharedMemory(create=True, size=a.nbytes)

    b = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf)
    b[:] = a[:]  # Copy the original data into shared memory

    p = Process(target=target_mode, args=(shm.name, a.shape, a.dtype))
    p.start()

    p.join()
    shm.close()
    shm.unlink()
