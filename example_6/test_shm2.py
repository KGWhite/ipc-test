from multiprocessing import shared_memory
shm_a = shared_memory.SharedMemory(create=True, size=10)
#type(shm_a.buf)
#<class 'memoryview'>
print(type(shm_a.buf))
buffer = shm_a.buf
#len(buffer)
#10
print(len(buffer))
buffer[:4] = bytearray([22, 33, 44, 55])  # Modify multiple at once
buffer[4] = 100                           # Modify single byte at a time
# Attach to an existing shared memory block
shm_b = shared_memory.SharedMemory(shm_a.name)
import array
a = array.array('b', shm_b.buf[:5])  # Copy the data into a new array.array
#array('b', [22, 33, 44, 55, 100])
print(a)
shm_b.buf[:5] = b'howdy'  # Modify via shm_b using bytes
#bytes(shm_a.buf[:5])      # Access via shm_a
#b'howdy'
print(bytes(shm_a.buf[:5]))
shm_b.close()   # Close each SharedMemory instance
shm_a.close()
shm_a.unlink()  # Call unlink only once to release the shared memory