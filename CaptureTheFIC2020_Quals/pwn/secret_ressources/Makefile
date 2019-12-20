all:
	# g++ heapme.cpp -o heapme -fstack-protector-all -Wl,-z,relro,-z,now
	# g++ heapme.cpp -o heapme # -fstack-protector-all -Wl,-z,relro,-z,now
	# g++ heapme.cpp -o heapme -fno-pie -fno-pic # -fstack-protector-all -Wl,-z,relro,-z,now
	g++ heapme.cpp -o heapme -fstack-protector -g # -Wl,-z,relro,-z,now
	cp heapme ../chall/

patch:
	patchelf --set-interpreter /root/tools/glibc/x64/ld-2.23.so ./heapme

clean:
	rm -rf heapme
